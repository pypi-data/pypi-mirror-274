from datetime import datetime, timezone
from hashlib import sha256
from hmac import new as hmac_new
from io import BytesIO, IOBase, SEEK_END, SEEK_SET
from pathlib import Path
from typing import Dict, Literal
from urllib.parse import urlencode, urlparse

from bs4 import BeautifulSoup
from bs4.element import Tag
from requests import Session
from requests.structures import CaseInsensitiveDict
from requests.utils import default_user_agent as requests_user_agent
from requests_toolbelt import MultipartEncoder

from .model._model import StreamableVideo, CatboxVideo


class _StreamableClient:
    api_url = "https://ajax.streamable.com"
    aws_bucket_url = "https://streamables-upload.s3.amazonaws.com"
    base_url = "https://streamable.com"
    frontend_react_version = "5a6120a04b6db864113d706cc6a6131cb8ca3587"

    @staticmethod
    def __hmac_sha256_sign(key: bytes, msg: str):
        return hmac_new(key, msg.encode("utf8"), digestmod=sha256).digest()

    @staticmethod
    def __aws_api_signing_key(
        key_secret: str,
        datestamp: str,
        region: str,
        service: str,
    ):
        key_date = _StreamableClient.__hmac_sha256_sign(
            f"AWS4{key_secret}".encode("utf8"),
            datestamp,
        )
        key_region = _StreamableClient.__hmac_sha256_sign(key_date, region)
        key_service = _StreamableClient.__hmac_sha256_sign(key_region, service)
        key_signing = _StreamableClient.__hmac_sha256_sign(
            key_service,
            "aws4_request",
        )
        return key_signing

    @staticmethod
    def __aws_authorization(
        method: str,
        headers: CaseInsensitiveDict,
        req_time: datetime,
        access_key_id: str,
        secret_access_key: str,
        uri: str,
        query: Dict[str, str],
        region: str,
        service: str = "s3",
    ):
        method = method.upper()
        assert method in (
            "CONNECT",
            "DELETE",
            "GET",
            "HEAD",
            "OPTIONS",
            "PATCH",
            "POST",
            "PUT",
            "TRACE",
        ), "Invalid HTTP method specified!"

        headers_dict = CaseInsensitiveDict()
        query_dict = {}

        for hk, hv in dict(sorted(headers.items())).items():
            headers_dict[hk.lower()] = hv.strip()

        assert "x-amz-content-sha256" in headers_dict, "Must specify Content SHA256 for AWS request"

        algorithm = "AWS4-HMAC-SHA256"
        credential_scope = "/".join(
            [
                req_time.strftime("%Y%m%d"),
                region,
                service,
                "aws4_request",
            ]
        )
        signed_headers = ";".join(headers_dict.keys())

        for qk, qv in dict(sorted(query.items())).items():
            query_dict[urlencode(qk)] = urlencode(qv)

        signature = hmac_new(
            _StreamableClient.__aws_api_signing_key(
                secret_access_key,
                req_time.strftime("%Y%m%d"),
                region,
                service,
            ),
            "\n".join(
                (
                    algorithm,
                    req_time.strftime("%Y%m%dT%H%M%SZ"),
                    credential_scope,
                    sha256(
                        "\n".join(
                            (
                                method,
                                uri,
                                "&".join([f"{qk}:{qv}" for qk, qv in query_dict.items()]),
                                "".join([f"{hk}:{hv}\n" for hk, hv in headers_dict.items()]),
                                signed_headers,
                                headers_dict["x-amz-content-sha256"],
                            )
                        ).encode("utf8")
                    ).hexdigest(),
                )
            ).encode("utf8"),
            digestmod=sha256,
        ).hexdigest()

        return (
            f"{algorithm} Credential={access_key_id}/"
            + f"{credential_scope}, SignedHeaders={signed_headers}, Signature="
            + signature
        )

    def __init__(self, session: Session) -> None:
        self.__session = session

    def __generate_clip_shortcode(
        self,
        video_id: str,
        video_source: str,
        title: str | None = None,
    ):
        res = self.__session.post(
            f"{_StreamableClient.api_url}/videos",
            json={
                "extract_id": video_id,
                "extractor": "streamable",
                "source": video_source,
                "status": 1,
                "title": title,
                "upload_source": "clip",
            },
        )
        res.raise_for_status()
        res_json = res.json()

        assert "error" not in res_json or res_json["error"] is None, (
            "Error occurred while trying to generate clip shortcode!\n" + res_json["error"]
        )

        shortcode = res_json["shortcode"]
        assert isinstance(shortcode, str)

        return shortcode

    def __generate_upload_shortcode(self, video_sz: int):
        res = self.__session.get(
            f"{_StreamableClient.api_url}/shortcode",
            params={
                "version": _StreamableClient.frontend_react_version,
                "size": video_sz,
            },
        )
        res.raise_for_status()
        res_json = res.json()

        return (
            res_json["shortcode"],
            res_json["credentials"]["accessKeyId"],
            res_json["credentials"]["secretAccessKey"],
            res_json["credentials"]["sessionToken"],
            res_json["transcoder_options"]["token"],
        )

    def __transcode_clipped_video(
        self,
        shortcode: str,
        video_headers: Dict[str, str],
        video_url: str,
        extractor: Literal["streamable", "generic"] = "generic",
        mute: bool = False,
        title: str | None = None,
    ):
        res = self.__session.post(
            f"{_StreamableClient.api_url}/transcode/{shortcode}",
            json={
                "extractor": extractor,
                "headers": video_headers,
                "mute": mute,
                "shortcode": shortcode,
                "thumb_offset": None,
                "title": title,
                "upload_source": "clip",
                "url": video_url,
            },
        )
        res.raise_for_status()

        res_json = res.json()
        assert "error" not in res_json or res_json["error"] is None, (
            "Error occurred while trying to transcode clip shortcode!\n" + res_json["error"]
        )

    def __transcode_uploaded_video(self, shortcode: str, transcoder_token: str, video_sz: int):
        return self.__session.post(
            "/".join(
                (
                    _StreamableClient.api_url,
                    "transcode/{shortcode}".format(shortcode=shortcode),
                )
            ),
            json={
                "shortcode": shortcode,
                "size": video_sz,
                "token": transcoder_token,
                "upload_source": "web",
                "url": "/".join(
                    (
                        _StreamableClient.aws_bucket_url,
                        "upload/{shortcode}".format(shortcode=shortcode),
                    )
                ),
            },
        )

    def __update_upload_metadata(
        self,
        shortcode: str,
        filename: str,
        video_sz: int,
        title: str | None = None,
    ):
        res = self.__session.put(
            "/".join(
                (
                    _StreamableClient.api_url,
                    "videos/{shortcode}".format(shortcode=shortcode),
                )
            ),
            json={
                "original_name": filename,
                "original_size": video_sz,
                "title": title or Path(filename).stem,
                "upload_source": "web",
            },
            params={"purge": ""},
        )
        res.raise_for_status()

    def __video_extractor(self, url: str):
        res = self.__session.get(
            f"{_StreamableClient.api_url}/extract",
            params={"url": url},
        )
        res.raise_for_status()
        res_json = res.json()

        assert "error" not in res_json or res_json["error"] is None, (
            "Error occurred while trying to extract video URL!\n" + res_json["error"]
        )

        return res_json["url"], res_json["headers"]

    def clear_cookies(self):
        self.__session.cookies.clear(domain=".streamable.com")

    def get_video_content(self, video_id: str):
        video_url = self.get_video_url(video_id)
        res = self.__session.get(video_url)
        res.raise_for_status()
        return BytesIO(res.content)

    def get_video_url(self, video_id: str):
        res = self.__session.get(f"{_StreamableClient.base_url}/{video_id}")
        res.raise_for_status()

        vid_source_tag = BeautifulSoup(
            res.text,
            features="html.parser",
        ).find(
            "meta",
            attrs={"property": "og:video:secure_url"},
        )

        assert isinstance(vid_source_tag, Tag)

        video_source_url = vid_source_tag["content"]
        assert isinstance(video_source_url, str)

        return video_source_url

    def is_video_available(self, video_id: str):
        return self.__session.get(f"{_StreamableClient.base_url}/{video_id}").ok

    def is_video_processing(self, video_id: str):
        res = self.__session.get(f"{_StreamableClient.base_url}/{video_id}")
        res.raise_for_status()

        return (
            BeautifulSoup(
                res.text,
                features="html.parser",
            ).find("div", attrs={"id": "player-content"})
            is None
        )

    def mirror_video(
        self,
        video: StreamableVideo | CatboxVideo,
        title: str | None = None,
        
    ):
        if isinstance(video, StreamableVideo):
            url, headers = self.__video_extractor(str(video.url))

            return None #StreamableVideo(shortcode=mirror_shortcode, host="streamable", url=f"{_StreamableClient.base_url}/{mirror_shortcode}", filename=title or video.shortcode, clip_title=title)

    def upload_video(
        self,
        video_io: IOBase,
        filename: str,
        title: str  = "",
        creator: str = "",
        upload_region: str = "us-east-1",
    ):
        video_io.seek(0, SEEK_END)
        video_sz = video_io.tell()
        video_io.seek(0, SEEK_SET)

        (
            shortcode,
            access_key_id,
            secret_access_key,
            session_token,
            transcoder_token,
        ) = self.__generate_upload_shortcode(video_sz)

        self.__update_upload_metadata(
            shortcode,
            filename,
            video_sz,
            title=title,
        )

        hash = sha256()
        video_io.seek(0, SEEK_SET)

        while len(chunk := video_io.read(4096)) > 0:
            if len(chunk) > 4096:
                raise IOError("Got more data than expected!")

            hash.update(chunk)

        video_io.seek(0, SEEK_SET)
        video_hash = hash.hexdigest()

        req_datetime = datetime.now(tz=timezone.utc)

        aws_headers = CaseInsensitiveDict()
        aws_headers["Host"] = urlparse(_StreamableClient.aws_bucket_url).netloc
        aws_headers["Content-Type"] = "application/octet-stream"
        aws_headers["X-AMZ-ACL"] = "public-read"
        aws_headers["X-AMZ-Content-SHA256"] = video_hash
        aws_headers["X-AMZ-Security-Token"] = session_token
        aws_headers["X-AMZ-Date"] = req_datetime.strftime("%Y%m%dT%H%M%SZ")
        aws_headers["Authorization"] = _StreamableClient.__aws_authorization(
            "PUT",
            aws_headers,
            req_datetime,
            access_key_id,
            secret_access_key,
            "/upload/{shortcode}".format(shortcode=shortcode),
            {},
            upload_region,
            service="s3",
        )

        res = self.__session.put(
            "/".join(
                (
                    _StreamableClient.aws_bucket_url,
                    "upload/{shortcode}".format(shortcode=shortcode),
                )
            ),
            data=video_io,
            headers=aws_headers,
        )
        res.raise_for_status()

        res = self.__transcode_uploaded_video(
            shortcode,
            transcoder_token,
            video_sz,
        )
        res.raise_for_status()

        return StreamableVideo(url=f"{_StreamableClient.base_url}/{shortcode}", shortcode=shortcode, host="streamable", filename=filename, clip_title=title, streamer=creator)


class _CatboxClient:
    api_url = "https://catbox.moe/user/api.php"
    file_base_url = "https://files.catbox.moe"

    def __init__(self, session: Session) -> None:
        self.__session = session

    def clear_cookies(self):
        self.__session.cookies.clear(domain=".catbox.moe")

    def get_video_content(self, link_id: str):
        video_url = self.get_video_url(link_id)
        res = self.__session.get(video_url)
        res.raise_for_status()
        return BytesIO(res.content)

    def get_video_url(self, link_id: str):
        res = self.__session.get(f"{_CatboxClient.api_url}?action=info&key={link_id}")
        res.raise_for_status()

        res_json = res.json()
        assert "error" not in res_json or res_json["error"] is None, (
            "Error occurred while trying to get video URL!\n" + res_json["error"]
        )

        return res_json["url"]

    def is_video_available(self, filename: str):
        return self.__session.get(f"{self.file_base_url}/{filename}").ok

    def mirror_video(
        self,
        video: CatboxVideo,
    ):
        pass

    def upload_video(
        self,
        video_io: IOBase,
        filename: str,
        title: str = "",
        creator: str = "",
    ):
        
        data = {
            "reqtype": "fileupload",
            "userhash": "",
            "fileToUpload": (filename, video_io, "video/mp4"),
        }
        m = MultipartEncoder(
            fields=data,
        )
        headers = {"Content-Type": m.content_type}
        res = self.__session.post(
            f"{_CatboxClient.api_url}",
            data=m,
            headers=headers,
        )
        url = res.text
        shortcode = url.split("/")[-1][:-4]
        catbox_vid = CatboxVideo(url=f"{_CatboxClient.file_base_url}/{shortcode}.mp4", shortcode=shortcode, host="catbox", filename=filename, clip_title=title, streamer=creator)
        return catbox_vid


class Client:
    def __init__(
        self,
        session: Session | None = None,
        user_agent: str | None = None,
    ) -> None:
        if session is None:
            session = Session()

        if user_agent:
            assert session.headers["User-Agent"] == requests_user_agent(), (
                "Custom User-Agent specified both in session headers and " + "in class constructor"
            )

            session.headers["User-Agent"] = user_agent

        # elif session.headers["User-Agent"] == requests_user_agent():
        #     session.headers["User-Agent"] = f"test"

        self.__streamable = _StreamableClient(session)
        self.__catbox = _CatboxClient(session)

    @property
    def streamable(self):
        return self.__streamable

    @property
    def catbox(self):
        return self.__catbox


from abc import ABC


class VideoClient(ABC):
    def __init__(self, url: str, shortcode: str, host: str, filename: str, clip_title: str, streamer: str = "", direct_url: str = "") -> None:
        self.url: str = url
        self.shortcode: str = shortcode
        self.host: str = host
        self.filename: str = filename
        self.clip_title: str = clip_title
        self.streamer: str = streamer
        self.direct_url: str = direct_url

    def get_video(self):
        pass


class StreamableVideo(VideoClient):
    host: str = "streamable"
    shortcode: str
    url: str = ""
    filename: str = ""

    def __str__(self):
        return f"StreamableVideo(url={self.url}, shortcode={self.shortcode}, host={self.host}, filename={self.filename}, clip_title={self.clip_title}, streamer={self.streamer})"


class CatboxVideo(VideoClient):
    host: str = "catbox"
    shortcode: str
    url: str
    filename: str

    def __str__(self):
        return f"CatboxVideo(url={self.url}, shortcode={self.shortcode}, host={self.host}, filename={self.filename}, clip_title={self.clip_title}, streamer={self.streamer})"
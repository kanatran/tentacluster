import time
from threading import Thread
from typing import Optional

from bs4 import BeautifulSoup

from autoselenium import chrome

yt = "https://www.youtube.com"
ChromeDriver = chrome.webdriver.Chrome


class YTLiveService(Thread):
    """
    Usage:

    >>> ytl = YTLiveService("UCHsx4Hqa-1ORjQTh9TYDhww")
    >>> assert ytl.live_link is None, "Kiara is not live"
    >>> assert ytl.live_link == "yt/watch?v=id", "Kiara is live"
    """

    refresh_interval = 30

    def __init__(self, channel_id: str):
        super().__init__(daemon=True)
        self._channel_link = f"{yt}/channel/{channel_id}"
        self._web: Optional[ChromeDriver] = None
        self.live_link: Optional[str] = None
        self.start()

    def run(self):
        self._web = self.__get_selenium()
        while 1:
            self.__update_live_link()
            time.sleep(self.refresh_interval)

    def __update_live_link(self) -> None:
        self._web.get(self._channel_link)
        soup = BeautifulSoup(self._web.page_source, "html.parser")
        try:
            if soup.find("span", {"aria-label": "LIVE"}):
                yt_endpoint = soup.find("div", {"id": "dismissable"}).find(
                    "a", {"id": "video-title"}
                )["href"]
                self.live_link = f"{yt}{yt_endpoint}"
            else:
                self.live_link = None
        except AttributeError:
            self.live_link = None

    @staticmethod
    def __get_selenium() -> ChromeDriver:
        chrome.setup_driver()
        web = chrome.get_selenium(False)
        return web

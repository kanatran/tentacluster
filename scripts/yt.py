import time
from threading import Event, Thread
from typing import List, Optional

from autoselenium import chrome
from bs4 import BeautifulSoup

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
        self._subscribers: List[Event] = []
        self.live_link: Optional[str] = None
        self.start()

    def listen(self) -> Event:
        e = Event()
        self._subscribers.append(e)
        return e

    def run(self):
        self._web = self.__get_selenium()
        while 1:
            old_link = self.live_link
            self.__update_live_link()
            if self.live_link != old_link:
                self.__publish_on_change()
            time.sleep(self.refresh_interval)

    def __publish_on_change(self) -> None:
        for sub in self._subscribers:
            sub.set()

    def __update_live_link(self) -> None:
        self._web.get(self._channel_link)
        time.sleep(2)
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

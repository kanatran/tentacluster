import gc
import os
import time
from threading import Event, Thread

from autoselenium import chrome

class WebSpeechSlave(Thread):
    """
    Opens up web speech in the browser

    export REFRESH_CHROME="1" to enable refreshing
    """
    refresh_interval = 60 * 15

    def __init__(self, host: str):
        super().__init__(daemon=True)
        self._host = host
        chrome.setup_driver()

    def run(self):
        chrome.setup_driver()
        web = None
        while 1:
            newweb = chrome.get_selenium(True)
            newweb.get(f"{self._host}/static/index.html")
            del web
            gc.collect()
            web = newweb
            time.sleep(self.refresh_interval)

    def __wait_for_refresh(self):
        if int(os.environ.get("REFRESH_CHROME", 0)):
            time.sleep(self.refresh_interval)
        else:
            Event().wait()

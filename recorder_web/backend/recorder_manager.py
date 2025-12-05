import json
import time
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from salesforce_autotest.recorder.event_listener import SalesforceEventListener
from salesforce_autotest.recorder.locator_engine import SalesforceLocatorEngine
from schemas import RecorderEvent
import asyncio

CHROME_DEBUG_PORT = 9222

class RecorderManager:

    def __init__(self, hub):
        self.hub = hub
        self.steps = []
        self.driver = None
        self.listener = None

    def _connect_to_chrome(self):
        opts = Options()
        opts.add_experimental_option("debuggerAddress", f"localhost:{CHROME_DEBUG_PORT}")
        return webdriver.Chrome(options=opts)

    def start(self):
        self.driver = self._connect_to_chrome()

        locator_engine = SalesforceLocatorEngine(self.driver)
        self.listener = SalesforceEventListener(
            driver=self.driver,
            locator_engine=locator_engine,
            callback=self._on_event
        )
        self.listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()
        return True

    def _on_event(self, event_dict):
        evt = RecorderEvent(**event_dict)
        self.steps.append(evt.dict())
        asyncio.run(self.hub.broadcast(json.dumps(evt.dict())))

    def get_steps(self):
        return self.steps

    def export_yaml(self):
        filename = f"recording_{int(time.time())}.yaml"
        with open(filename, "w") as f:
            yaml.dump({"steps": self.steps}, f)
        return filename
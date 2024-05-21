import time
import atexit
import requests
import os
import logging
from threading import Thread
import jsonpickle
from .config import get_config

logger = logging.getLogger(__name__)

DEFAULT_API_URL = "https://api.lunary.ai"


class Consumer(Thread):
    def __init__(self, event_queue, app_id=None):
        self.running = True
        self.event_queue = event_queue
        self.app_id = app_id

        Thread.__init__(self, daemon=True)
        atexit.register(self.stop)

    def run(self):
        while self.running:
            self.send_batch()
            time.sleep(0.5)

        self.send_batch()

    def send_batch(self):
        config = get_config()
        batch = self.event_queue.get_batch()

        verbose = config.verbose
        api_url = config.api_url

        token = self.app_id or config.app_id

        if len(batch) > 0:
            if verbose:
                logging.info(f"[Lunary] Sending {len(batch)} events.")

            try:
                if verbose:
                    logging.info("[Lunary] Sending events to ", api_url)

                headers = {
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json'
                }
            
                data = jsonpickle.encode({"events": batch}, unpicklable=False)
                response = requests.post(
                    api_url + "/v1/runs/ingest",
                    data=data,
                    headers=headers,
                    verify=config.disable_ssl_verify)

                if verbose:
                    logging.info("[Lunary] Events sent.", response.status_code)

                if response.status_code != 200:
                    logging.exception("[Lunary] Error sending events")
            except Exception as e:
                if verbose:
                    logging.exception(f"[Lunary] Error sending events: {e}")

                self.event_queue.append(batch)

    def stop(self):
        self.running = False
        self.join()

import random
import threading
import requests


class HttpClient:

    def __init__(self, proxy_enabled=False, proxies=None, timeout=0.5):
        if proxies is None:
            proxies = []

        if proxy_enabled and not proxies:
            raise ValueError("Empty proxies")

        self.proxy_enabled = proxy_enabled
        self.proxies = proxies
        self.thread_local = threading.local()
        self.timeout = timeout

    def get_client(self):
        if not hasattr(self.thread_local, "session"):
            self.thread_local.session = requests.Session()
        return self.thread_local.session

    def get_proxies(self, url):
        if not self.proxy_enabled:
            return {}

        if url and ('10.30.' in url or "-clusterip-svc" in url):
            return {}

        proxy = random.choice(self.proxies)
        return {"http": proxy, "https": proxy}

    def get(self, url, **kwargs):
        return self.get_client().get(
            url,
            proxies=self.get_proxies(url),
            timeout=self.timeout,
            **kwargs
        )

    def post(self, url, data=None, json=None, **kwargs):
        return self.get_client().post(
            url,
            data=data,
            json=json,
            proxies=self.get_proxies(url),
            timeout=self.timeout,
            **kwargs
        )

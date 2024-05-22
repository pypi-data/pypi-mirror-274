from functools import cached_property
import requests
import logging
from scriptonite.configuration import Configuration
from scriptonite.logging import Logger
from typing import Union


log = Logger(level=logging.DEBUG)


class BuzzClient:

    def __init__(self, api_url: str, token: str) -> None:
        self.api = api_url
        self.token = token
        self.headers = {'x-auth-token': self.token}

    def get(self, endpoint: str):
        response = requests.get(f"{self.api}{endpoint}",
                                headers=self.headers)
        return response

    def check(self):
        try:
            api_info = self.get('/')
        except BaseException as e:
            print(e)
            return dict(api_ok=False, token_ok=False)
        if api_info.ok:
            api_path = api_info.json().get('api_path')
            token_check = self.get(f"{api_path}/check")

            if token_check.ok:
                return dict(api_ok=True, token_ok=True)
            else:
                return dict(api_ok=True, token_ok=False)
        return dict(api_ok=False, token_ok=False)

    @cached_property
    def api_info(self) -> dict:
        return self.get('/').json()

    @cached_property
    def api_path(self) -> str | None:
        return self.api_info.get('api_path')

    @cached_property
    def api_version(self) -> str | None:
        return self.api_info.get('app_version')

    @cached_property
    def notifiers(self):
        response = self.get(f'{self.api_path}/notifiers')
        if response.ok:
            return response.json().get(
                'notifiers')
        else:
            return []

    def send(self, notifier: str,
             recipient: str,
             body: str,
             title: Union[str, None] = "You got a buzz",
             severity: Union[str, None] = "info",
             attach: Union[str, None] = '',
             format_: Union[str, None] = 'text'):

        data = dict(recipient=recipient,
                    body=body,
                    title=title,
                    severity=severity,
                    format_=format_)
        files = {}
        if attach:
            log.debug(f"attaching {attach}...")
            files = {'attach': open(attach, 'rb')}

        response = requests.post(
            f"{self.api}{self.api_path}/send/{notifier}",
            data=data,
            files=files,
            headers=self.headers)

        # response.raise_for_status()
        return response


if __name__ == "__main__":
    c = Configuration()
    c.from_environ(prefix="BUZZ")
    bc = BuzzClient(c)
    bc.check()

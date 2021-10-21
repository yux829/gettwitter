import re
import time

import requests
import logging as logme

class TokenExpiryException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

        
class RefreshTokenException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        

class Token:
    def __init__(self, config):
        self._session = requests.Session()
        self._session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'})
        self.config = config
        self._retries = 5
        self._timeout = 10
        self.url = 'https://twitter.com'

    def _request(self):
        for attempt in range(self._retries + 1):
            # The request is newly prepared on each retry because of potential cookie updates.
            req = self._session.prepare_request(requests.Request('GET', self.url))
            logme.debug(f'Retrieving {req.url}')
            try:
                #r = self._session.send(req, allow_redirects=True, timeout=self._timeout)
                # by xqar 2021-10-19 start
                import urllib3
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                if self.config.Proxy_type.lower() == "http":
                    httpproxystr = "http://" + self.config.Proxy_host + ":" + str(self.config.Proxy_port)
                    proxies = {"http": httpproxystr, "https": httpproxystr}
                    r = self._session.send(req, allow_redirects=True, timeout=self._timeout, proxies=proxies, verify=False)
                else:
                    r = self._session.send(req, allow_redirects=True, timeout=self._timeout)
                '''
                if Twint.config.Proxy_type.lower() == "http":
                    proxystr="http://" + Twint.config.Proxy_host + ":" + str(Twint.config.Proxy_port)
                    proxies = {"http": proxystr, "https": proxystr}
                    r = self._session.send(req, allow_redirects=True, timeout=self._timeout, proxies=proxies, verify=False)
                else :
                    r = self._session.send(req, allow_redirects=True, timeout=self._timeout)
                '''

                # by xqar 2021-10-19 end
            except requests.exceptions.RequestException as exc:
                if attempt < self._retries:
                    retrying = ', retrying'
                    level = logme.WARNING
                else:
                    retrying = ''
                    level = logme.ERROR
                logme.log(level, f'Error retrieving {req.url}: {exc!r}{retrying}')
            else:
                success, msg = (True, None)
                msg = f': {msg}' if msg else ''

                if success:
                    logme.debug(f'{req.url} retrieved successfully{msg}')
                    return r
            if attempt < self._retries:
                # TODO : might wanna tweak this back-off timer
                sleep_time = 2.0 * 2 ** attempt
                logme.info(f'Waiting {sleep_time:.0f} seconds')
                time.sleep(sleep_time)
        else:
            msg = f'{self._retries + 1} requests to {self.url} failed, giving up.'
            logme.fatal(msg)
            self.config.Guest_token = None
            raise RefreshTokenException(msg)

    def refresh(self):
        logme.debug('Retrieving guest token')
        res = self._request()
        match = re.search(r'\("gt=(\d+);', res.text)
        if match:
            logme.debug('Found guest token in HTML')
            self.config.Guest_token = str(match.group(1))
        else:
            self.config.Guest_token = None
            raise RefreshTokenException('Could not find the Guest token in HTML')

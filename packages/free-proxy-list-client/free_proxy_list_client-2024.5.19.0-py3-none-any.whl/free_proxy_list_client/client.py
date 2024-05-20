"""
Copyright 2024 by Sergei Belousov

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import random
from typing import List, Dict, Optional, Any
import requests
from bs4 import BeautifulSoup


class FreeProxyListClient:
    """ A client to fetch and filter proxies from free-proxy-list.net. """

    def __init__(self):
        """ Initialize the FreeProxyListClient with the default URL and an empty list of proxies. """
        self.url: str = 'https://free-proxy-list.net/'
        self.proxies: List[Dict[str, str]] = []
        self.update_proxies()

    def update_proxies(self) -> None:
        """ Fetch the latest proxy list from the URL and update the internal list of proxies. """
        response: requests.Response = requests.get(self.url)
        soup: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')
        table: Optional[BeautifulSoup] = soup.find('table', {'class': 'table table-striped table-bordered'})
        if not table:
            raise ValueError("Could not find the proxy list table on the webpage.")

        rows: List[BeautifulSoup] = table.find_all('tr')[1:]  # Skip header row

        self.proxies = []
        for row in rows:
            cols: List[BeautifulSoup] = row.find_all('td')
            proxy: Dict[str, str] = {
                'ip_addr': cols[0].text,
                'port': cols[1].text,
                'code': cols[2].text,
                'country': cols[3].text,
                'anonymity': cols[4].text,
                'google': cols[5].text,
                'https': cols[6].text,
                'last_checked': cols[7].text
            }
            self.proxies.append(proxy)

    def search(
            self,
            code: Optional[str] = None,
            country: Optional[str] = None,
            anonymity: Optional[str] = None,
            google: Optional[str] = None,
            https: Optional[str] = None,
            last_checked: Optional[str] = None,
            get_random_proxy: Optional[bool] = False,
            update_proxies: Optional[bool] = False
    ) -> List[Dict[str, str]]:
        """ Search for proxies based on the given criteria.

        Args:
            code (str): The country code of the proxy.
            country (str): The country name of the proxy.
            anonymity (str): The anonymity level of the proxy.
            google (str): The Google support status of the proxy.
            https (str): The HTTPS support status of the proxy.
            last_checked (str): The last checked timestamp of the proxy.
            get_random_proxy (bool): Whether to return a random proxy from the filtered list.
            update_proxies (bool): Whether to update the proxy list before searching.

        Returns:
            List[Dict[str, str]]: A list of proxies that match the search criteria.
        """
        # update proxies if needed
        if update_proxies or not self.proxies:
            self.update_proxies()
        # check if proxies list is empty
        assert self.proxies, "Proxy list is empty."
        # filter proxies based on search criteria
        results: List[Dict[str, str]] = self.proxies
        if code:
            results = [proxy for proxy in results if proxy['code'] == code]
        if country:
            results = [proxy for proxy in results if proxy['country'] == country]
        if anonymity:
            results = [proxy for proxy in results if proxy['anonymity'] == anonymity]
        if google:
            results = [proxy for proxy in results if proxy['google'] == google]
        if https:
            results = [proxy for proxy in results if proxy['https'] == https]
        if last_checked:
            results = [proxy for proxy in results if proxy['last_checked'] == last_checked]
        if get_random_proxy:
            return [random.choice(results)]
        else:
            return results

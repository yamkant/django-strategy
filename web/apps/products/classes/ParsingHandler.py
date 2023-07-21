from typing import Any
import requests
from bs4 import BeautifulSoup
from enum import Enum

class OgDataParser:
    def __init__(self, html_text) -> None:
        self._soup = BeautifulSoup(html_text, 'html.parser')

    # FIXME: og_data가 NoneType인 경우, og_data가 'content' 키를 갖지 않는 경우 처리
    def get_og_data_from_soup(self, property):
        og_data = self._soup.select_one(f'meta[property="og:{property}"]')
        return og_data['content']


class ParsingHandler:
    """URL로부터 정보를 파싱하는 클래스입니다."""
    def __init__(self, url) -> None:
        self._url = url

    @property
    def url(self):
        return self._url

    def get_info(self):
        headers = {'Accept': 'application/json'}
        response = requests.get(self._url, headers=headers)
        response.raise_for_status()

        og_data_parser = OgDataParser(response.text)
        return {
            "title": og_data_parser.get_og_data_from_soup('title'),
            "image": og_data_parser.get_og_data_from_soup('image'),
        } 





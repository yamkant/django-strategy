from typing import Any
import requests
from bs4 import BeautifulSoup
from enum import Enum

class OgDataParserException(Exception):
    pass


class OgDataParser:
    def __init__(self, html_text) -> None:
        self._soup = BeautifulSoup(html_text, 'html.parser')
    
    # NOTE: validation 영역 추가하기
    def _get_valid_soup(self):
        if self._soup.head == None:
            raise OgDataParserException("head 태그가 없습니다.")
        return self._soup.head


    # FIXME: head가 없는 경우, og_data가 NoneType인 경우, og_data가 'content' 키를 갖지 않는 경우 처리
    def get_og_data_from_soup(self, property):
        valid_soup = self._get_valid_soup() 
        og_data = valid_soup.select_one(f'meta[property="og:{property}"]')

        if og_data.get("content") == None:
            raise OgDataParserException("og data에 content가 없습니다.")
        return og_data.get("content")

class ProductInfoParser:
    def __init__(self, title):
        self._title = title

    def parse_brand(self):
        self._title


class ParsingHandler:
    """URL로부터 정보를 파싱하는 클래스입니다."""
    def __init__(self, endpoint="") -> None:
        self._endpoint = endpoint
        self._html_text = ""

    @property
    def endpoint(self):
        return self._endpoint
    
    @endpoint.setter
    def endpoint(self, value):
        self._endpoint = value

    @property
    def html_text(self):
        return self._html_text
    
    def set_info_from_url(self):
        headers = {'Accept': '*/*'}
        response = requests.get(self._endpoint, headers=headers)
        self._html_text = response.text
    
    def get_info_by_property(self, property):
        og_data_parser = OgDataParser(self.html_text)
        return og_data_parser.get_og_data_from_soup(property)
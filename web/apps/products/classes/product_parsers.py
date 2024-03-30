from typing import Any
import requests
from bs4 import BeautifulSoup
from enum import Enum
import os
from abc import ABC, abstractmethod

class OgDataParserException(Exception):
    pass

class StoreDataParser:
    @abstractmethod
    def set_soup(self, html_text):
        pass
    @abstractmethod
    def get_data_from_soup(self, property):
        pass


class OgDataParser(StoreDataParser):
    def set_soup(self, html_text):
        self._soup = BeautifulSoup(html_text, 'html.parser')
    
    # NOTE: validation 영역 추가하기
    def _get_valid_soup(self):
        if self._soup.head == None:
            raise OgDataParserException("head 태그가 없습니다.")
        return self._soup.head


    # FIXME: head가 없는 경우, og_data가 NoneType인 경우, og_data가 'content' 키를 갖지 않는 경우 처리
    def get_data_from_soup(self, property):
        valid_soup = self._get_valid_soup() 
        og_data = valid_soup.select_one(f'meta[property="og:{property}"]')

        if not og_data:
            raise OgDataParserException("og data가 존재하지 않습니다.")
        if og_data.get("content") == None:
            raise OgDataParserException("og data에 content가 없습니다.")
        return og_data.get("content")

class SongzioDataParser(StoreDataParser):
    def set_soup(self, html_text):
        self._soup = BeautifulSoup(html_text, 'html.parser')

    def get_data_from_soup(self, property):
        print(self._soup.select_one('div'))


class ProductInfoParser:
    def __init__(self, title):
        self._title = title

    def parse_brand(self):
        self._title


class ParsingHandler:
    """URL로부터 정보를 파싱하는 클래스입니다."""
    def __init__(self, store_data_parser, endpoint="") -> None:
        self._endpoint = endpoint
        self._store_data_parser = store_data_parser
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
        headers = {
            "User-Agent": os.environ.get("HTTP_USER_AGENT"),
        }
        response = requests.get(self._endpoint, headers=headers, verify=False)
        response.raise_for_status()
        self._html_text = response.text
    
    def get_info(self, property):
        self._store_data_parser.set_soup(self._html_text)
        return self._store_data_parser.get_data_from_soup(property)
import logging
import unittest
from unittest.mock import Mock
from enum import Enum

from products.classes.ParsingHandler import ParsingHandler, OgDataParser

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
# logger.addHandler(logging.FileHandler('./test.log'))
logger.setLevel(logging.INFO)

class OgDataPraserTest(unittest.TestCase):
    def test_get_og_data_from_soup(self):
        expected_og_title = "[TIME HOMME] 와이드 데님 팬츠"
        expected_og_image = "https://cdn-img.thehandsome.com/studio/goods/TH/2C/FW/TH2C8NPC677N_DN_W01.jpg?rs=684X1032"
        html_text = f'''
            <meta data-n-head="ssr" data-hid="og:title" property="og:title" content="{expected_og_title}">
            <meta data-n-head="ssr" data-hid="og:description" property="og:description" content="&amp;nbsp;">
            <meta data-n-head="ssr" data-hid="og:image" property="og:image" content="{expected_og_image}">
            <meta data-n-head="ssr" data-hid="og:type" property="og:type" content="product">
            <meta data-n-head="ssr" data-hid="og:url" property="og:url" content="">
        '''
        og_data_parser = OgDataParser(html_text)
        self.assertEqual(og_data_parser.get_og_data_from_soup('title'), expected_og_title)
        self.assertEqual(og_data_parser.get_og_data_from_soup('image'), expected_og_image)


class ParsingHandlerTest(unittest.TestCase):
    def test_get_info(self):
        endPoint = 'https://www.thehandsome.com/ko/PM/productDetail/TH2C8NPC677N?itmNo=001'
        parse_handler = ParsingHandler(endPoint)
        expected_og_title = "[TIME HOMME] 와이드 데님 팬츠"
        expected_og_image = "https://cdn-img.thehandsome.com/studio/goods/TH/2C/FW/TH2C8NPC677N_DN_W01.jpg?rs=684X1032"
        self.assertEqual(parse_handler.get_info(), {
            "title": expected_og_title,
            "image": expected_og_image,
        })
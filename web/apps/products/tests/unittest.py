import logging
import unittest
from unittest import skip
from unittest.mock import Mock
from enum import Enum

from products.classes.product_parsers import ParsingHandler, OgDataParser, OgDataParserException

logger = logging.getLogger(__name__)
# logger.addHandler(logging.StreamHandler())
logger.addHandler(logging.FileHandler('./test.log'))
logger.setLevel(logging.INFO)

# NOTE: fixture 사용해서 테스트 전처리값 변경
class OgDataPraserTest(unittest.TestCase):
    def test_get_og_data_from_soup(self):
        expected_og_title = "[TIME HOMME] 와이드 데님 팬츠"
        expected_og_image = "https://cdn-img.thehandsome.com/studio/goods/TH/2C/FW/TH2C8NPC677N_DN_W01.jpg?rs=684X1032"
        html_text = f'''
        <head>
            <meta data-n-head="ssr" data-hid="og:title" property="og:title" content="{expected_og_title}">
            <meta data-n-head="ssr" data-hid="og:description" property="og:description" content="&amp;nbsp;">
            <meta data-n-head="ssr" data-hid="og:image" property="og:image" content="{expected_og_image}">
            <meta data-n-head="ssr" data-hid="og:type" property="og:type" content="product">
            <meta data-n-head="ssr" data-hid="og:url" property="og:url" content="">
        </head>
        '''
        og_data_parser = OgDataParser(html_text)
        self.assertEqual(og_data_parser.get_og_data_from_soup('title'), expected_og_title)
        self.assertEqual(og_data_parser.get_og_data_from_soup('image'), expected_og_image)

    def test_get_og_data_without_content(self):
        expected_og_title = "[TIME HOMME] 와이드 데님 팬츠"
        expected_og_image = "https://cdn-img.thehandsome.com/studio/goods/TH/2C/FW/TH2C8NPC677N_DN_W01.jpg?rs=684X1032"
        html_text = f'''
        <head>
            <meta data-n-head="ssr" data-hid="og:title" property="og:title"">
            <meta data-n-head="ssr" data-hid="og:description" property="og:description" content="&amp;nbsp;">
            <meta data-n-head="ssr" data-hid="og:image" property="og:image" content="{expected_og_image}">
            <meta data-n-head="ssr" data-hid="og:type" property="og:type" content="product">
            <meta data-n-head="ssr" data-hid="og:url" property="og:url" content="">
        </head>
        '''
        og_data_parser = OgDataParser(html_text)
        self.assertRaisesRegex(
            OgDataParserException,
            "og data에 content가 없습니다.",
            og_data_parser.get_og_data_from_soup,
            'title',
        )


class ParsingHandlerTest(unittest.TestCase):
    def test_get_info(self):
        endPoint = 'https://www.thehandsome.com/ko/PM/productDetail/TH2C8NPC677N?itmNo=001'
        parse_handler = ParsingHandler(endPoint)
        expected_og_title = "[TIME HOMME] 와이드 데님 팬츠"
        expected_og_image = "https://cdn-img.thehandsome.com/studio/goods/TH/2C/FW/TH2C8NPC677N_DN_W01.jpg?rs=684X1032"

        parse_handler.set_info_from_url()
        self.assertEqual(parse_handler.get_info_by_property('title'), expected_og_title)
        self.assertEqual(parse_handler.get_info_by_property('image'), expected_og_image)

    @skip
    def test_get_info_ssg(self):
        endPoint = 'https://www.ssg.com/item/itemView.ssg?itemId=1000483217140&siteNo=7008&salestrNo=6005'
        parse_handler = ParsingHandler(endPoint)
        parse_handler.set_info_from_url()
        print(parse_handler.html_text)
        # logger.info(parse_handler.get_info_by_property('title'))
        # expected_og_title = "[TIME HOMME] 와이드 데님 팬츠"
        # expected_og_image = "https://cdn-img.thehandsome.com/studio/goods/TH/2C/FW/TH2C8NPC677N_DN_W01.jpg?rs=684X1032"
        # self.assertEqual(parse_handler.get_info_from_url(), {
        #     "title": expected_og_title,
        #     "image": expected_og_image,
        # })
    
    def test_get_info_lemaire(self):
        endPoint = 'https://us.lemaire.fr/products/belted-easy-pants-bk999-black-m-23s-1'
        parse_handler = ParsingHandler(endPoint)
        parse_handler.set_info_from_url()

        expect_og_title = "BELTED EASY PANTS"
        expect_og_image = "https://us.lemaire.fr/cdn/shop/products/PA1021_LF1019_BK999_4_600x.webp?v=1673372650"

        self.assertEqual(parse_handler.get_info_by_property('title'), expect_og_title)
        self.assertEqual(parse_handler.get_info_by_property('image'), expect_og_image)

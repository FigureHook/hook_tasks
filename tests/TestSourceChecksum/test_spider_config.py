from hook_tasks.SourceChecksum.spider_config import (
    GSCProductSpiderConfig,
    AlterProductSpiderConfig,
    NativeProductSpiderConfig
)
from figure_parser.constants import GSCCategory, GSCLang, AlterCategory, NativeCategory


class TestSpiderConfig:
    def test_gsc_product_config(self):
        sample_config = {
            'force_update': False,
            'is_announcement_spider': False,
            'begin_year': 2012,
            'end_year': 2016,
            'lang': 'ja',
            'category': 'scale',
        }

        gsc_config = GSCProductSpiderConfig(
            begin_year=2012,
            end_year=2016,
            lang=GSCLang.JAPANESE,
            category=GSCCategory.SCALE
        )

        assert gsc_config.asdict() == sample_config

    def test_alter_product_config(self):
        sample_config = {
            'force_update': False,
            'is_announcement_spider': False,
            'begin_year': 2017,
            'end_year': 2020,
            'category': 'altair',
        }

        alter_config = AlterProductSpiderConfig(
            begin_year=2017,
            end_year=2020,
            category=AlterCategory.ALTAIR
        )

        assert alter_config.asdict() == sample_config

    def test_native_product_config(self):
        sample_config = {
            'force_update': False,
            'is_announcement_spider': False,
            'begin_page': 2,
            'end_page': None,
            'category': 'creators',
        }

        native_config = NativeProductSpiderConfig(
            begin_page=2,
            category=NativeCategory.CREATORS
        )

        assert native_config.asdict() == sample_config

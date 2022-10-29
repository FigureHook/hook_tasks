import re

from hook_tasks.domains.sns_post.plurk.helpers import PlurkFormatHelper


def test_bold():
    pattern = r"\*\*.+\*\*"
    assert re.match(pattern, PlurkFormatHelper.bold("kappa"))


def test_link():
    pattern = r"^\S+ \(.+\)"
    assert re.match(pattern, PlurkFormatHelper.link("kappa", "http://foo.bar"))


def test_italic():
    pattern = r"\*.+\*"
    assert re.match(pattern, PlurkFormatHelper.italic("kappa"))

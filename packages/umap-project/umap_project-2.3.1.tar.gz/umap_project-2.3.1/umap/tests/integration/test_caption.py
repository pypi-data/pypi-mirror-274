import re

import pytest
from playwright.sync_api import expect

from ..base import DataLayerFactory

pytestmark = pytest.mark.django_db


def test_caption(live_server, page, map):
    map.settings["properties"]["onLoadPanel"] = "caption"
    map.save()
    basic = DataLayerFactory(map=map, name="Basic layer")
    non_loaded = DataLayerFactory(
        map=map, name="Non loaded", settings={"displayOnLoad": False}
    )
    hidden = DataLayerFactory(map=map, name="Hidden", settings={"inCaption": False})
    page.goto(f"{live_server.url}{map.get_absolute_url()}")
    panel = page.locator(".panel.left.on")
    expect(panel).to_have_class(re.compile(".*condensed.*"))
    expect(panel.locator(".umap-caption")).to_be_visible()
    expect(panel.locator(".datalayer-legend").get_by_text(basic.name)).to_be_visible()
    expect(
        panel.locator(".datalayer-legend .off").get_by_text(non_loaded.name)
    ).to_be_visible()
    expect(panel.locator(".datalayer-legend").get_by_text(hidden.name)).to_be_hidden()

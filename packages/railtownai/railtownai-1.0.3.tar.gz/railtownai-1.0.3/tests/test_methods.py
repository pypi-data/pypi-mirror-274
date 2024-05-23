#   ---------------------------------------------------------------------------------
#   Copyright (c) Railtown AI. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
from __future__ import annotations

import requests_mock
from railtownai import log, get_config


def test_get_config():
    assert get_config()["u"] == "tst3978dadf9a1e49b3822276df158786e6.railtownlogs.com"


def test_log():
    with requests_mock.Mocker() as m:
        m.post("https://tst3978dadf9a1e49b3822276df158786e6.railtownlogs.com", json={"status": "success"})
        log("Test error", foo="bar")
        assert m.call_count == 1

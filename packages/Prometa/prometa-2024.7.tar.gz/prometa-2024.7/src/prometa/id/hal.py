#!/usr/bin/env python
"""
HAL open science functions.

https://api.archives-ouvertes.fr/docs/search
"""

import logging
from urllib.parse import quote as urlquote

import requests


LOGGER = logging.getLogger(__name__)


def get_hal_url_by_origin(origin):
    """
    Get the HAL ID by origin.
    """
    cache = get_hal_url_by_origin.cache
    try:
        return cache[origin]
    except KeyError:
        pass

    timeout = 5
    query = origin.split("://", 1)[1]
    search_url = f"https://api.archives-ouvertes.fr/search/?q={urlquote(query)}"
    LOGGER.debug("Querying %s", search_url)
    resp = requests.get(search_url, timeout=timeout).json()
    for doc in resp["response"]["docs"]:
        label = doc["label_s"]
        if f"origin={origin};" in label:
            url = doc["uri_s"]
            cache[origin] = url
            return url
    return None


get_hal_url_by_origin.cache = {}


def get_hal_id_from_url(url):
    """
    Extract the HAL ID from a HAL URL.
    """
    return url.rsplit("/", 1)[1]

#!/usr/bin/env python
"""
Software Heritage functions.
"""

import logging
from urllib.parse import quote as urlquote

import requests


LOGGER = logging.getLogger(__name__)


def get_swhid_by_origin(origin):
    """
    Get a Software Heritage ID from an origin URL. This only includes the origin
    and repository ID.

    Args:
        origin:
            The origin URL of the software project.

    Returns:
        A Software Heritage ID string.
    """
    cache = get_swhid_by_origin.cache
    try:
        return cache[origin]
    except KeyError:
        pass

    timeout = 5
    url = f"https://archive.softwareheritage.org/api/1/origin/{origin}/get/"
    LOGGER.debug("Querying %s", url)
    resp = requests.get(url, timeout=timeout).json()
    try:
        resp = requests.get(resp["origin_visits_url"], timeout=timeout).json()
        resp = requests.get(resp[0]["snapshot_url"], timeout=timeout).json()
        resp = requests.get(
            resp["branches"]["HEAD"]["target_url"], timeout=timeout
        ).json()
        swhid = f'swh:1:dir:{resp["directory"]};origin={urlquote(origin)}'
        cache[origin] = swhid
        return swhid
    except KeyError:
        return None


get_swhid_by_origin.cache = {}


def get_swh_url_by_origin(origin):
    """
    Get a Software Heritage link for an origin URL.

    Args:
        origin:
            The origin URL of the software project.

    Returns:
        A Software Heritage URL. The page may not exist.
    """
    return f"https://archive.softwareheritage.org/browse/origin/?origin_url={urlquote(origin)}"


def swh_project_exists(origin):
    """
    Check if the project exists on Software Heritage.

    Args:
        origin:
            The origin URL of the software project.

    Returns:
        True if the project exists, False otherwise.
    """
    return get_swhid_by_origin(origin) is not None

"""Raindrop.io API client for bookmark discovery."""

import json
import re
import sys
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

from . import http


def _log_error(msg: str):
    """Log error to stderr."""
    sys.stderr.write(f"[RAINDROPS ERROR] {msg}\n")
    sys.stderr.flush()


RAINDROPS_API_URL = "https://api.raindrop.io/rest/v1/raindrops"

# Depth configurations: perpage and number of pages
DEPTH_CONFIG = {
    "quick": {"perpage": 15, "pages": 1},      # 15 results
    "default": {"perpage": 30, "pages": 1},    # 30 results
    "deep": {"perpage": 50, "pages": 2},       # 100 results max
}


def search_raindrops(
    api_key: str,
    topic: str,
    from_date: str,
    to_date: str,
    collection_id: str = "0",
    depth: str = "default",
    mock_response: Optional[Dict] = None,
) -> Dict[str, Any]:
    """Search Raindrop.io for bookmarks matching topic and date range.

    Args:
        api_key: Raindrop.io API token
        topic: Search query
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        collection_id: Collection to search ("0" for all, "-1" for unsorted, or specific ID)
        depth: Search depth (quick, default, deep)
        mock_response: Mock response for testing

    Returns:
        Dict with "items" list containing matching raindrops
    """
    if mock_response is not None:
        return mock_response

    config = DEPTH_CONFIG.get(depth, DEPTH_CONFIG["default"])

    # Build search query with date filter
    # Use created:> for date range filtering
    search_query = f'{topic} created:>{from_date}'

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # Timeout based on depth
    timeout = 30 if depth == "quick" else 45 if depth == "default" else 60

    url = f"{RAINDROPS_API_URL}/{collection_id}"

    # Fetch pages
    all_items = []
    for page in range(config["pages"]):
        params = {
            "search": search_query,
            "perpage": config["perpage"],
            "page": page,
            "sort": "-created",  # Most recent first
        }

        # Build URL with query params
        url_with_params = f"{url}?{urlencode(params)}"

        try:
            response = http.get(url_with_params, headers=headers, timeout=timeout)

            if response.get("result") and response.get("items"):
                items = response["items"]
                all_items.extend(items)

                # Stop if we got fewer items than requested (last page)
                if len(items) < config["perpage"]:
                    break
            else:
                # No more results
                break
        except http.HTTPError as e:
            _log_error(f"API request failed: {e}")
            if http.DEBUG and e.body:
                _log_error(f"Response body: {e.body[:500]}")
            break

    return {"result": True, "items": all_items}


def parse_raindrops_response(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Parse Raindrop.io response to extract bookmark items.

    Args:
        response: Raw API response

    Returns:
        List of item dicts
    """
    items = []

    # Check for API errors
    if "error" in response and response["error"]:
        error = response["error"]
        err_msg = error.get("message", str(error)) if isinstance(error, dict) else str(error)
        _log_error(f"Raindrop.io API error: {err_msg}")
        if http.DEBUG:
            _log_error(f"Full error response: {json.dumps(response, indent=2)[:1000]}")
        return items

    if not response.get("result"):
        _log_error("API returned result=false")
        return items

    raw_items = response.get("items", [])
    if not raw_items:
        return items

    # Validate and clean items
    clean_items = []
    for i, item in enumerate(raw_items):
        if not isinstance(item, dict):
            continue

        # Required fields
        link = item.get("link", "")
        if not link:
            continue

        # Extract collection info if present
        collection_info = item.get("collection", {})
        collection_id = None
        if isinstance(collection_info, dict):
            # Handle both $id and _id formats
            collection_id = collection_info.get("$id") or collection_info.get("_id")

        # Build clean item
        clean_item = {
            "id": str(item.get("_id", f"RD{i+1}")),
            "title": str(item.get("title", "Untitled")).strip(),
            "link": link,
            "domain": str(item.get("domain", "")).strip(),
            "excerpt": item.get("excerpt", ""),
            "note": item.get("note", ""),
            "tags": item.get("tags", []),
            "type": str(item.get("type", "link")),
            "created": item.get("created", ""),
            "last_update": item.get("lastUpdate", ""),
            "cover": item.get("cover", ""),
            "important": bool(item.get("important", False)),
            "collection_id": collection_id,
        }

        # Validate date format (should be ISO 8601)
        if clean_item["created"]:
            # Accept both YYYY-MM-DD and ISO 8601 formats
            if not (re.match(r'^\d{4}-\d{2}-\d{2}', str(clean_item["created"]))):
                clean_item["created"] = None

        # Ensure tags is a list
        if not isinstance(clean_item["tags"], list):
            clean_item["tags"] = []

        clean_items.append(clean_item)

    return clean_items

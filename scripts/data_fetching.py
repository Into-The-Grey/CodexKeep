# CodexKeep/scripts/data_fetching.py

import os
import sys
import requests
from error_handling import log_error, handle_critical_error


def fetch_manifest():
    """
    Fetch the Bungie API manifest.
    """
    api_key = os.getenv("API_KEY")
    headers = {"X-API-Key": api_key}
    manifest_url = "https://www.bungie.net/Platform/Destiny2/Manifest/"
    try:
        response = requests.get(manifest_url, headers=headers, timeout=10)
        if response.status_code == 200:
            print("[INFO] Successfully fetched the manifest.")
            return response.json()
        else:
            log_error(f"Manifest fetch failed: {response.status_code} {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        handle_critical_error(f"Failed to fetch manifest: {e}")


def get_manifest_component_url(manifest_data, component_name):
    """
    Extract URLs for specific manifest components.
    """
    try:
        path = manifest_data["Response"]["jsonWorldComponentContentPaths"]["en"].get(
            component_name
        )
        return f"https://www.bungie.net{path}" if path else None
    except KeyError as e:
        log_error(f"Failed to parse manifest for {component_name}: {e}")
        return None


if __name__ == "__main__":
    manifest = fetch_manifest()
    if not manifest:
        sys.exit(1)

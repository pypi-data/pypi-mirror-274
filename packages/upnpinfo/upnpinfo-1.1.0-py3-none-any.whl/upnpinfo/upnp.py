from __future__ import annotations
import logging
from urllib.parse import urlparse

from upnpclient import Device, discover


def discover_upnp_devices(timeout: int) -> list[Device]:
    """Perform a UPnP discovery of all devices on the local network."""
    # Hide the default ssdp logging. Main motivation is to hide the following:
    #   "Error 'Document is empty, line 1, column 1 ...'"
    ssdp_logger = logging.getLogger("ssdp")
    ssdp_logger.setLevel(logging.CRITICAL)

    all_devices = discover(timeout=timeout)

    # Filter out duplicate devices (by UDN)
    unique_devices = []
    device_udns = []

    for device in all_devices:
        if device.udn not in device_udns:
            device_udns.append(device.udn)
            unique_devices.append(device)

    return unique_devices


def get_upnp_device(location) -> Device:
    """Get a UPnP Device instance for the device at the given location."""
    return Device(location=location)


def device_service_details(device: Device) -> dict:
    """Get service-related details for a Device.

    Per-service details includes:
        - URL to retrieve the full Service Control Protocol Description (scpd)
        - List of supported action names.

    Response shape:

    {
        "service1": {
            "scpd_url": "http://...",
            "actions": ["action1", ...],
        },
        "service2": {
            "scpd_url": "http://...",
            "actions": ["action1", ...],
        },
        ...
    }
    """
    service_names = []

    try:
        service_names = sorted(list(device.service_map.keys()))
    except AttributeError:
        pass

    # The Device's base URL is required for determining the per-service SCPD
    location_url = urlparse(device.location)
    device_base_url = None

    if location_url:
        device_base_url = f"{location_url.scheme}://{location_url.netloc}"

    service_details = {}

    for service_name in service_names:
        # Determine this service's SCPD URL
        scpd_url = None

        if device_base_url:
            try:
                service_path = device.service_map[service_name].scpd_url
                scpd_url = f"{device_base_url}{service_path}"
            except (IndexError, AttributeError):
                pass

        # Add this service's details to the result
        service_details[service_name] = {
            "scpd_url": scpd_url,
            "actions": [
                action.name
                for action in sorted(
                    device.service_map[service_name].actions,
                    key=lambda action: action.name,
                )
            ],
        }

    return service_details


def device_summary(device: Device) -> dict:
    """Get a summary of the given UPnP device."""
    return {
        "friendly_name": device.friendly_name or None,
        "udn": device.udn or None,
        "device_type": device.device_type or None,
        "manufacturer": device.manufacturer or None,
        "manufacturer_url": device.manufacturer_url or None,
        "model_name": device.model_name or None,
        "model_number": device.model_number or None,
        "model_description": device.model_description or None,
        "location": device.location or None,
        "services": device_service_details(device) or None,
    }

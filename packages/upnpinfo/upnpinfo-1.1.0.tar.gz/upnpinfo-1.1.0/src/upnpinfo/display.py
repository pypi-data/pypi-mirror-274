from __future__ import annotations

import json
from urllib.parse import urlparse

import click
from rich.columns import Columns
from rich.table import box, Table
from rich.text import Text

from upnpinfo.upnp import (
    device_summary,
    discover_upnp_devices,
    get_upnp_device,
    device_service_details,
)


def display_all_devices(
    console, script_name, wanted_device_types, timeout, plain_output, as_json
):
    """Display a summary of all UPnP devices found on the local network."""
    with console.status("Discovering UPnP devices..."):
        devices = discover_upnp_devices(timeout=timeout)

    if len(devices) <= 0:
        console.print("No UPnP devices found.")

    # Exclude unwanted device types
    filtered_devices = [
        device for device in devices if _device_type_match(device, wanted_device_types)
    ]

    if len(filtered_devices) <= 0:
        console.print("No matching UPnP devices found.")

        return

    # Create a list of unique device information summary dicts
    device_summaries = []

    for device in filtered_devices:
        device_summaries.append(device_summary(device))

    if as_json:
        # Dump the device summaries as JSON
        console.print(json.dumps(device_summaries, indent=4))
    else:
        # Display a table of unique device information summaries
        table = Table(
            show_header=True,
            header_style=None if plain_output else "bold",
            box=box.SIMPLE_HEAD,
            pad_edge=False,
        )

        table.add_column("Name", no_wrap=True)
        table.add_column("Manufacturer")
        table.add_column("Description")
        table.add_column("Model")
        table.add_column("Type")
        table.add_column("Address")

        for device in sorted(
            device_summaries, key=lambda device: device["friendly_name"].lower()
        ):
            # Extract just the hostname from the full location URL
            parsed_location = urlparse(device["location"])
            address = parsed_location.hostname

            # Extract just the device type name from the full device type
            # e.g. urn:schemas-upnp-org:device:MediaRenderer:1 -> MediaRenderer
            found_device_types = device["device_type"]

            try:
                found_device_types = found_device_types.split(":")[3]
            except IndexError:
                pass

            table.add_row(
                device["friendly_name"] or "-",
                device["manufacturer"] or "-",
                device["model_description"] or "-",
                device["model_name"] or "-",
                found_device_types or "-",
                address or "-",
            )

        # Display the table and a footer message showing how to get detailed
        # info on a device

        console.print(
            table,
            Text(f"Run \"{script_name} '<name>'\" to view device details.\n"),
        )


def display_single_device(
    console, device_input, wanted_device_types, timeout, plain_output, as_json
):
    """Display detailed information on a single UPnP device."""
    found_multiple = False

    # Check if the input is a URL. If it's not then we assume it's a device
    # name and attempt to find that name in the list of all discovered devices.
    device_input_as_url = urlparse(device_input)

    if device_input_as_url.hostname is None:
        # See if the device input was a device friendly name or a UDN
        with console.status(f"Finding device: {device_input} ..."):
            all_devices = discover_upnp_devices(timeout=timeout)

        try:
            locations = [
                device
                for device in all_devices
                if (device.friendly_name == device_input or device.udn == device_input)
                and _device_type_match(device, wanted_device_types)
            ]

            found_multiple = len(locations) > 1

            location = locations[0].location
        except (IndexError, AttributeError):
            msg = f"UPnP device not found: {device_input}"

            if len(wanted_device_types) > 0:
                msg += f" (type: {', '.join(wanted_device_types)})"

            console.print(msg)
            console.print(
                "If the device specifier and optional type are valid, try a longer --timeout"
            )

            return
    else:
        # Device input was a URL
        location = device_input

    try:
        # Get device details from the device URL
        with console.status(f"Retrieving details for device: {device_input} ..."):
            device = get_upnp_device(location)
    except Exception as e:
        console.print(e)

        return

    service_details = device_service_details(device)

    if as_json:
        # Dump the device details as JSON
        console.print(json.dumps(device_summary(device), indent=4))
    else:
        # Prepare a table of device details
        details_table = Table(
            show_header=False,
            box=box.SIMPLE_HEAD,
            padding=0,
            pad_edge=False,
        )

        details_table.add_column("Field", justify="right")
        details_table.add_column(
            "Value", justify="left", style=None if plain_output else "bold"
        )

        details_table.add_row("Friendly name:", device.friendly_name or "-")
        details_table.add_row("UDN:", device.udn or "-")
        details_table.add_row("Device type:", device.device_type or "-", style=None)
        details_table.add_row("Manufacturer:", device.manufacturer or "-")
        details_table.add_row("Manufacturer URL:", device.manufacturer_url or "-")
        details_table.add_row("Model name:", device.model_name or "-")
        details_table.add_row("Model number:", device.model_number or "-")
        details_table.add_row("Model description:", device.model_description or "-")
        details_table.add_row("Location:", device.location or "-")
        details_table.add_row(
            "Services:", ", ".join(sorted(service_details.keys())) or "-"
        )

        # Prepare columns showing the actions available for each service
        service_columns = []

        for service_name in service_details.keys():
            service_table = Table(
                show_header=True,
                header_style=None if plain_output else "bold",
                box=box.SIMPLE_HEAD,
                pad_edge=False,
            )

            service_table.add_column(service_name)

            # Add the actions for this service
            actions = service_details[service_name]["actions"]

            if len(actions) > 0:
                for action in actions:
                    service_table.add_row(action)
            else:
                service_table.add_row("No actions")

            # Add the URL to retrieve details for this service
            scpd_url = service_details[service_name]["scpd_url"]

            if scpd_url is not None:
                service_table.add_row()
                service_table.add_row(scpd_url)

            service_columns.append(service_table)

        # Display the details table and (if present) the service action tables
        if len(service_columns) > 0:
            console.print(
                details_table, Text(" Service actions:"), Columns(service_columns)
            )
        else:
            console.print(details_table)

        if found_multiple:
            console.print(
                "Note: Only the first matching device is displayed; "
                + "use --type to display a different device for this host."
            )


def _device_type_match(device, device_types: tuple[click.STRING]) -> bool:
    """Determine whether the given device's type is included in device_types.

    If device_types is an empty tuple, then the device is assumed to match.
    """
    if len(device_types) <= 0:
        return True

    # This isn't strictly checking
    return (
        len(
            [
                device_type
                for device_type in device_types
                if device.device_type.split(":")[3] == device_type
            ]
        )
        > 0
    )

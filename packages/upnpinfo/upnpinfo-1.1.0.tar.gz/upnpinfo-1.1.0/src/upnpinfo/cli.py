import click
from rich.console import Console
from rich.traceback import install

from upnpinfo.display import display_all_devices, display_single_device


install(suppress=[click])


@click.command()
@click.argument(
    "device",
    required=False,
)
@click.option(
    "--type",
    "-t",
    "device_types",
    help="Show just the given UPnP device type (e.g. MediaRenderer).",
    metavar="TYPE",
    type=click.STRING,
    multiple=True,
)
@click.option(
    "--timeout",
    help="UPnP discovery timeout (seconds).",
    metavar="SECS",
    type=click.INT,
    default=2,
    show_default=True,
)
@click.option(
    "--no-color",
    help="Disable color.",
    is_flag=True,
    default=False,
)
@click.option(
    "--json",
    "as_json",
    help="Display results as JSON.",
    is_flag=True,
    default=False,
)
def cli(device, device_types, timeout, no_color, as_json):
    """
    Retrieves UPnP device information from the local network.

    Defaults to showing a summary of all devices found on the local network
    using UPnP discovery. Specify an optional DEVICE (a UPnP friendly name,
    UDN, or location URL) to retrieve detailed information on that device.
    """
    console = Console(no_color=no_color, highlight=not no_color, emoji=False)

    if device is not None:
        display_single_device(console, device, device_types, timeout, no_color, as_json)
    else:
        display_all_devices(
            console,
            click.get_current_context().info_name,
            device_types,
            timeout,
            no_color,
            as_json,
        )


if __name__ == "__main__":
    cli()

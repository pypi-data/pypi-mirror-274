# upnpinfo

`upnpinfo` is a commandline tool for retrieving UPnP device information from the local network.
It's a simple CLI wrapper around [upnpclient](https://github.com/flyte/upnpclient).

## Installation

`upnpinfo` requires Python 3.8 or higher.

```console
❯ pip install upnpinfo
```

## Features

### Discover UPnP devices

By default, `upnpinfo` will perform UPnP discovery on the local network and display a summary
of all discovered devices.

```console
❯ upnpinfo

 Name       Manufacturer      Description   Model   Type            Address
 ───────────────────────────────────────────────────────────────────────────────
 creamy     Hegel             H120          H120    MediaRenderer   10.0.0.11
 streamer   Cambridge Audio   -             CXNv2   MediaRenderer   10.0.0.12

Run "upnpinfo '<name>'" to view device details.
```

### Display detailed information on a single device

Specify an optional `DEVICE` to view detailed information on that device, including the device's
services and actions. The provided `DEVICE` can be a UPnP friendly name, a unique UDN, or a UPnP
location URL.

```console
❯ upnpinfo creamy

     Friendly name: creamy
               UDN: uuid:6cadb326-8b41-423c-b02b-b4eaaaaf0f8d
       Device type: urn:schemas-upnp-org:device:MediaRenderer:1
      Manufacturer: Hegel
  Manufacturer URL: http://www.hegel.com
        Model name: H120
      Model number: 1.0
 Model description: H120
          Location: http://10.0.0.11:38400/description.xml
          Services: AVTransport, ConnectionManager, QPlay, RenderingControl

 Service actions:

 AVTransport                                 ConnectionManager
 ─────────────────────────────────────────   ───────────────────────────────────────────────
 GetCurrentTransportActions                  GetCurrentConnectionIDs
 GetDeviceCapabilities                       GetCurrentConnectionInfo
 GetMediaInfo                                GetProtocolInfo
 GetPositionInfo
 GetTransportInfo                            http://10.0.0.11:38400/ConnectionManager.xml
 GetTransportSettings
 Next
 Pause
 Play
 Previous
 Seek
 SetAVTransportURI
 SetPlayMode
 Stop

 http://10.0.0.11:38400/AVTransport.xml


 QPlay                                       RenderingControl
 ───────────────────────────────────         ──────────────────────────────────────────────
 GetMaxTracks                                GetMute
 GetTracksCount                              GetVolume
 GetTracksInfo                               ListPresets
 InsertTracks                                SelectPreset
 QPlayAuth                                   SetMute
 RemoveTracks                                SetVolume
 SetNetwork
 SetTracksInfo                               http://10.0.0.11:38400/RenderingControl.xml

 http://10.0.0.11:38400/QPlay.xml
```

### JSON output

Output can be optionally generated in JSON format.

```console
❯ upnpinfo creamy --json
{
    "friendly_name": "creamy",
    "udn": "uuid:6cadb326-8b41-423c-b02b-b4eaaaaf0f8d",
    "device_type": "urn:schemas-upnp-org:device:MediaRenderer:1",
    "manufacturer": "Hegel",
    "manufacturer_url": "http://www.hegel.com",
    "model_name": "H120",
    "model_number": "1.0",
    "model_description": "H120",
    "location": "http://10.0.0.11:38400/description.xml",
    "services": {
        "AVTransport": {
            "scpd_url": "http://10.0.0.11:38400/AVTransport.xml",
            "actions": [
                "GetCurrentTransportActions",
                "GetDeviceCapabilities",
                "GetMediaInfo",
                "GetPositionInfo",
                "GetTransportInfo",
                "GetTransportSettings",
                "Next",
                "Pause",
                "Play",
                "Previous",
                "Seek",
                "SetAVTransportURI",
                "SetPlayMode",
                "Stop"
            ]
        },
        "ConnectionManager": {
            "scpd_url": "http://10.0.0.11:38400/ConnectionManager.xml",
            "actions": [
                "GetCurrentConnectionIDs",
                "GetCurrentConnectionInfo",
                "GetProtocolInfo"
            ]
        },
        "QPlay": {
            "scpd_url": "http://10.0.0.11:38400/QPlay.xml",
            "actions": [
                "GetMaxTracks",
                "GetTracksCount",
                "GetTracksInfo",
                "InsertTracks",
                "QPlayAuth",
                "RemoveTracks",
                "SetNetwork",
                "SetTracksInfo"
            ]
        },
        "RenderingControl": {
            "scpd_url": "http://10.0.0.11:38400/RenderingControl.xml",
            "actions": [
                "GetMute",
                "GetVolume",
                "ListPresets",
                "SelectPreset",
                "SetMute",
                "SetVolume"
            ]
        }
    }
}
```

## Usage

The following flags are supported.

```console
❯ upnpinfo --help
Usage: upnpinfo [OPTIONS] [DEVICE]

  Retrieves UPnP device information from the local network.

  Defaults to showing a summary of all devices found on the local network
  using UPnP discovery. Specify an optional DEVICE (a UPnP friendly name, UDN,
  or location URL) to retrieve detailed information on that device.

Options:
  -t, --type TYPE  Show just the given UPnP device type (e.g. MediaRenderer).
  --timeout SECS   UPnP discovery timeout (seconds).  [default: 2]
  --no-color       Disable color.
  --json           Display results as JSON.
  --help           Show this message and exit.
```

## Ideas

It would be cool if `upnpinfo` had an interactive mode, allowing for browsing of devices and
device services, and supporting manual action invocation.
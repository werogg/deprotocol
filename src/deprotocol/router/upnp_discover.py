import upnpclient

from deprotocol.router.upnp_device import UPNPDevice


class UPNPDiscover:

    @staticmethod
    def discover():
        devices = [UPNPDevice(device) for device in upnpclient.discover()]
        return [device for device in devices if device.supports_wanipconnection()]

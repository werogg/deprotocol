class UPNPDevice:
    def __init__(self, device):
        self.device = device
        self.services = {service.serviceType: service for service in device.services}

    def supports_wanipconnection(self):
        return 'urn:schemas-upnp-org:service:WANIPConnection:1' in self.services

    def add_port_mapping(self, external_port, internal_port, protocol, description, duration):
        if not self.supports_wanipconnection():
            raise ValueError('Device does not support WANIPConnection')

        service = self.services['urn:schemas-upnp-org:service:WANIPConnection:1']
        return service.AddPortMapping(
            NewRemoteHost='',
            NewExternalPort=external_port,
            NewProtocol=protocol,
            NewInternalPort=internal_port,
            NewInternalClient=self.device.get_external_ip_address(),
            NewEnabled='1',
            NewPortMappingDescription=description,
            NewLeaseDuration=duration,
        )

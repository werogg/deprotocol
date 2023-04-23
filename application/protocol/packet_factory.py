import importlib


class PacketFactory:
    _packet_classes = {}

    @classmethod
    def register_packet_type(cls, packet_type, module_path, class_name):
        cls._packet_classes[packet_type] = (module_path, class_name)

    @staticmethod
    def create_packet(packet_type, payload=''):
        if packet_type not in PacketFactory._packet_classes:
            raise ValueError('Invalid packet type')
        module_path, class_name = PacketFactory._packet_classes[packet_type]
        module = importlib.import_module(module_path)
        packet_class = getattr(module, class_name)
        return packet_class(payload)

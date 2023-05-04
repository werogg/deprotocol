from deprotocol.network.protocol.packet_decoder import PacketDecoder
from deprotocol.network.protocol.packet_encoder import PacketEncoder
from deprotocol.network.protocol.packets.handshake import HandshakePacket
from deprotocol.network.protocol.packets.message import MessagePacket

if __name__ == "__main__":
    handshake_packet = HandshakePacket("mishuevos")
    message_packet = MessagePacket("test")
    print('Payload:', handshake_packet.payload)
    encoder = PacketEncoder()
    encoded = encoder.encode_packet(handshake_packet)

    print('Encoded data:', encoded)

    decoder = PacketDecoder()
    decoded = decoder.decode_packet(encoded)

    print('Decoded:', decoded)
    print('Paload:', decoded.payload)

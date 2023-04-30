from deprotocol.network.protocol.packet_decoder import PacketDecoder
from deprotocol.network.protocol.packet_encoder import PacketEncoder
from deprotocol.network.protocol.packets.handshake import HandshakePacket

if __name__ == "__main__":
    handshake_packet = HandshakePacket("mishuevos")
    print('Payload:', handshake_packet.payload)
    encoder = PacketEncoder()
    encoded = encoder.encode_packet(handshake_packet)

    print('Encoded data:', encoded)

    decoder = PacketDecoder()
    decoded = decoder.decode_packet(encoded)

    print('Decoded:', decoded)
    print('Paload:', decoded.payload)

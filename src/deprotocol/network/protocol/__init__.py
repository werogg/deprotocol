from deprotocol.network.protocol.packet_decoder import PacketDecoder
from deprotocol.network.protocol.packet_encoder import PacketEncoder
from deprotocol.network.protocol.packets.handshake import HandshakePacket
from deprotocol.network.protocol.packets.message import MessagePacket

if __name__ == "__main__":
    handshake_packet = HandshakePacket("test")
    message_packet = MessagePacket("test")
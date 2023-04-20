Feature: Connect and Handshake with Peer

Scenario: Connect to a peer and send the handshake packet
  Given a connection to p2p network over Tor
  And I know the peer's onion address and port number
  When I initiate a connection with the peer
  Then the connection is successfully established
  And I send a handshake packet to the peer
  And the peer receives and acknowledges the handshake packet with another handshake packet
  And the handshake packet includes a public key
  And both nodes can communicate securely over the p2p network over tor
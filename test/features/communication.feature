Feature: Connect and Handshake with Peer

Scenario: Establish a secure connection and exchange messages with a peer
  Given two clients of DeProtocol
  When the clients are started
  Then wait until both clients are ready to establish a connection
  When a client initiates a connection to the other client
  Then perform a secure handshake with the peer
  When the handshake is successfully completed
  Then validate the authenticity and integrity of the handshake packet
  When a message is sent to the peer
  Then the peer receives the message
  When the message is successfully validated
  Then stop the clients
Feature: Connect and Handshake with Peer

Scenario: Connect to a peer and send the handshake packet
  Given two clients of DeProtocol
  When a client connects to another client
  Then they do a handshake
  Then stop the clients
import datetime
import sys

from PyQt5.QtCore import QMetaObject, pyqtSlot, Qt
from PyQt5.QtCore import Q_ARG
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from pyqt5_plugins.examplebuttonplugin import QtGui

from deprotocol.api.client import Client
from deprotocol.event.event_listener import Listener
from deprotocol.event.events.deprotocol_ready_event import DeProtocolReadyEvent
from deprotocol.event.events.handshake_received_event import HandshakeReceivedEvent
from deprotocol.event.events.message_received_event import MessageReceivedEvent


class DeProtocolReadyListener(Listener):
    def __init__(self, app):
        self.app = app

    def handle_event(self, event: DeProtocolReadyEvent):
        self.app.load_gui()


class MessageReceivedListener(Listener):
    def __init__(self, app):
        self.app = app

    def handle_event(self, event: MessageReceivedEvent):
        timestamp_dt = datetime.datetime.fromtimestamp(event.time)
        formatted_time = timestamp_dt.strftime("%d/%m/%Y - %H:%M")
        self.app.handle_message(formatted_time, "default", event.message, event.node_connection.id)


class HandshakeReceivedListener(Listener):
    def __init__(self, app):
        self.app = app

    def handle_event(self, event: HandshakeReceivedEvent):
        if event.initiator:
            self.app.handle_init_handshake(event.nickname, event.connected_address, event.profile_img)


class ChatWidget(QWidget):
    def __init__(self, parent=None):
        super(ChatWidget, self).__init__(parent)
        self.listView = QListView(self)
        self.listView.setGeometry(0, 0, 780, 460)
        self.model = QtGui.QStandardItemModel(self.listView)
        self.listView.setModel(self.model)


class MainUI(QMainWindow):
    def __init__(self, deprotocol):
        super(MainUI, self).__init__()
        self.deprotocol = deprotocol
        loadUi("ui\main.ui", self)

        self.actionNew.triggered.connect(self.newPressed)
        self.pushButton.clicked.connect(self.sendMessage)

    def newPressed(self):
        dialog = NewDialog()
        result = dialog.exec_()
        if result == QDialog.Accepted:
            onion_address = dialog.lineEdit_2.text()
            new_widget = ChatWidget()
            self.tabWidget.addTab(new_widget, onion_address)
            new_widget.resize(self.size())
            new_widget.show()
            self.deprotocol.connect(onion_address)

    def newMessage(self, time, username, message, connection_id):
        item = QtGui.QStandardItem(f"[{time}] {username}: {message}")
        item.setEditable(False)
        chat_widget = self.tabWidget.widget(connection_id)
        chat_widget.model.appendRow(item)

    def sendMessage(self):
        current_chat = self.tabWidget.currentWidget()
        time = datetime.datetime.now().strftime("%Y:%m:%d - %H:%M")
        dest = self.tabWidget.currentIndex()
        message = self.lineEdit.text()
        self.deprotocol.send_message(dest, message)
        item = QtGui.QStandardItem(f"[{time}] you: {message}")
        item.setEditable(False)
        current_chat.model.appendRow(item)

    @pyqtSlot(str, str, str)
    def _newChat(self, nickname, address, profile_img):
        new_widget = ChatWidget(self)  # Create the widget in the GUI thread
        self.tabWidget.addTab(new_widget, address)
        new_widget.resize(self.size())
        new_widget.show()

    def newChat(self, nickname, address, profile_img):
        # Use QMetaObject.invokeMethod to execute newChat in the GUI thread
        QMetaObject.invokeMethod(self, "_newChat", Qt.QueuedConnection,
                                 Q_ARG(str, nickname),
                                 Q_ARG(str, address),
                                 Q_ARG(str, profile_img))
class NewDialog(QDialog):
    def __init__(self):
        super(NewDialog, self).__init__()
        loadUi("ui\dialognew.ui", self)


class MainApp:

    def __init__(self):
        self.ui = None
        self.app = None
        self.deprotocol = Client()
        self.deprotocol_ready = DeProtocolReadyListener(self)
        self.message_received = MessageReceivedListener(self)
        self.handshake_received = HandshakeReceivedListener(self)
        self.deprotocol.register_listener(self.deprotocol_ready)
        self.deprotocol.register_listener(self.message_received)
        self.deprotocol.register_listener(self.handshake_received)

    def start(self):
        self.deprotocol.start()

    def load_gui(self):
        self.app = QApplication(sys.argv)
        self.ui = MainUI(self.deprotocol)
        self.ui.show()
        sys.exit(self.app.exec_())

    def handle_message(self, time, username, message, connection_id):
        self.ui.newMessage(time, username, message, connection_id)

    def handle_init_handshake(self, nickname, address, profile_img):
        self.ui.newChat(nickname, address, profile_img)



if __name__ == "__main__":
    main = MainApp()
    main.start()

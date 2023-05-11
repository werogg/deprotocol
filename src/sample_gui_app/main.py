import datetime
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from pyqt5_plugins.examplebuttonplugin import QtGui

from deprotocol.api.client import Client
from deprotocol.event.event_listener import Listener
from deprotocol.event.events.deprotocol_ready_event import DeProtocolReadyEvent
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
        formatted_time = timestamp_dt.strftime("%Y:%m:%d - %H:%M")
        self.app.handle_message(formatted_time, "default", ' '.join(event.message))


class MainUI(QMainWindow):
    def __init__(self, deprotocol):
        super(MainUI, self).__init__()
        self.deprotocol = deprotocol
        loadUi("ui\main.ui", self)

        self.actionNew.triggered.connect(self.newPressed)
        self.model = QtGui.QStandardItemModel(self.listView)
        self.listView.setModel(self.model)

    def newPressed(self):
        dialog = NewDialog()
        result = dialog.exec_()
        if result == QDialog.Accepted:
            onion_address = dialog.lineEdit_2.text()
            self.deprotocol.connect(onion_address)

    def newMessage(self, time, username, message):
        item = QtGui.QStandardItem(f"[{time}] {username}: {message}")
        item.setEditable(False)
        self.model.appendRow(item)


class NewDialog(QDialog):
    def __init__(self):
        super(NewDialog, self).__init__()
        loadUi("ui\dialognew.ui", self)


class MainApp:

    def __init__(self):
        self.ui = None
        self.deprotocol = Client()
        self.deprotocol_ready = DeProtocolReadyListener(self)
        self.message_received = MessageReceivedListener(self)
        self.deprotocol.register_listener(self.deprotocol_ready)
        self.deprotocol.register_listener(self.message_received)

    def start(self):
        self.deprotocol.start()

    def load_gui(self):
        app = QApplication(sys.argv)
        self.ui = MainUI(self.deprotocol)
        self.ui.show()
        sys.exit(app.exec_())

    def handle_message(self, time, username, message):
        self.ui.newMessage(time, username, message)


if __name__ == "__main__":
    main = MainApp()
    main.start()

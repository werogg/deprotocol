""" This file contains file transfer logics """

import threading
import socket
import pickle
import time
import struct
import hashlib
import os

from application.logger.logger import Logger  # pylint: disable=import-error


class FileManager:
    """ Handles file transfer logic and internal paths for sharing files """

    def __init__(self):
        self.files = {}
        self.download_path = ""

    @staticmethod
    def hash_data(data):
        """ Hash the data to be uploaded """
        hasher = hashlib.md5()
        hasher.update(data)
        return str(hasher.hexdigest())

    @staticmethod
    def hash_file(filepath):
        """ Hash a file """
        try:
            with open(filepath, 'rb') as file:
                hasher = hashlib.md5()
                for chunk in iter(lambda: file.read(4096), b''):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except FileNotFoundError:
            Logger.get_logger().error(f'File not found: {filepath}')
        except PermissionError:
            Logger.get_logger().error(f'Permission denied: {filepath}')
        except OSError as exc:
            Logger.get_logger().error(f'OS error while hashing file {filepath}: {exc}')
        return None

    def refresh(self):
        """ Refresh current files """
        for i in list(self.files):
            if self.files[i]["path"] is not None:
                if not os.path.exists(self.files[i]["path"]):
                    print(
                        "Removing file that no longer exists: "
                        + str(self.files[i]["path"])
                    )
                    del self.files[i]

    def addfile(self, path):
        """ Add file to the current pool """
        name = os.path.basename(path)
        hashed_file = self.hash_file(path)
        self.files[hashed_file] = {"name": name, "path": path}
        return str(hashed_file)

    def have_file(self, hashed_file):
        """ Check if a file is added to the pool """
        self.refresh()
        if hashed_file in self.files:
            return True
        return None

    def get_all_files(self):
        """ Get all files in the poolk """
        self.refresh()
        return self.files


class FileClientThread(threading.Thread):
    """ This class handles the thread for the file transfer client"""

    def __init__(self, ip, port, conn, file_requested, file_manager):  # pylint: disable=too-many-arguments
        super().__init__()  # CAll Thread.__init__()
        self.terminate_flag = threading.Event()
        self.ip = ip  # pylint: disable=invalid-name
        self.port = port
        self.sock = conn
        self.file_requested = file_requested
        self.file_manager = file_manager

    def send_file(self, filehash):
        """ Send a file trough client """
        content = self.file_manager.get_all_files()
        filehash = str(filehash)
        if not self.file_manager.have_file(filehash):
            print("File requested to download but we do not have: " + filehash)
            self.sock.close()
        else:
            file = content[filehash]["name"]
            file_path = content[filehash]["path"]
            with open(file_path, "rb") as opened_file:
                data = opened_file.read()
            serialized_data = pickle.dumps(data)
            self.sock.sendall(struct.pack(">I", len(serialized_data)))
            time.sleep(0.1)
            print("File: " + file)
            self.sock.send(file.encode("utf-8"))
            time.sleep(0.1)
            self.sock.sendall(serialized_data)

    def stop(self):
        """ Stop file transfer client """
        self.terminate_flag.set()

    def run(self):
        """ Start file transfer client """
        self.send_file(self.file_requested)
        time.sleep(0.05)
        self.sock.close()


class FileServer(threading.Thread):
    """ Handles file server thread for file transfer """

    def __init__(self, parent, port):
        self.terminate_flag = threading.Event()
        super().__init__()  # CAll Thread.__init__()

        self.parent = parent
        self.port = port
        self.file_manager = self.parent.file_manager

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(10.0)
        self.sock.bind(("", self.port))
        self.sock.listen(1)

        self.threads = []

        self.dirname = ""

    def stop(self):
        """ Stops the file server """
        self.terminate_flag.set()

    def run(self):
        """ Starts the file server """
        Logger.get_logger().info("File Server Started")
        while (
                not self.terminate_flag.is_set()
        ):  # Check whether the thread needs to be closed
            try:
                (conn, (ip, port)) = self.sock.accept()  # pylint: disable=invalid-name

                self.parent.debug_print("File Server conection from: " + str(ip))

                file_requested = str(
                    conn.recv(4096).decode("utf-8")
                )

                Logger.get_logger().info("Sending file: " + file_requested)
                new_thread = FileClientThread(
                    ip, port, conn, file_requested, self.file_manager
                )

                self.file_manager.refresh()
                new_thread.start()

                self.threads.append(new_thread)

            except socket.timeout:
                pass

            except Exception as exc:
                raise exc
        time.sleep(0.01)

        for thread in self.threads:
            thread.join()
        Logger.get_logger().info("File Server stopped")


class FileDownloader(threading.Thread): # pylint: disable=too-many-instance-attributes
    """ Object to handle file downloader thread"""

    def __init__(self, ip, port, fhash, dirname, file_manager):  # pylint: disable=too-many-arguments
        super().__init__()
        self.finished = None
        self.filename = None
        self.remaining_payload_size = None
        self.data_size = None
        self.terminate_flag = threading.Event()
        self.fhash = str(fhash)
        self.dirnamme = dirname
        self.file_manager = file_manager
        self.invalid_chars = ["/", "\\", "|", "*", "<", ">", ":", "?", '"']
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.settimeout(10.0)
        try:
            self.conn.connect((ip, port))
        except (ConnectionRefusedError, ConnectionError, ConnectionResetError):
            print("Error connecting")
            self.stop()

    def stop(self):
        """ Stop file downloader thread"""
        self.terminate_flag.set()

    def run(self):
        """ Starts file downloader thread """
        try:
            self.conn.send(self.fhash.encode("utf-8"))
            self.data_size = struct.unpack(">I", self.conn.recv(9))[0]
            time.sleep(0.1)
            print("file size: " + str(self.data_size))
            self.filename = str(
                self.conn.recv(256).decode("utf-8")
            )  # receive file name
            print("file name:" + str(self.filename))
            for i in self.invalid_chars:
                if i in self.filename:
                    print("INVALID FILE NAME. ABORTING.")
                    self.stop()
                    return
            time.sleep(0.1)
            received_payload = b""
            remaining_payload_size = self.data_size
            while remaining_payload_size != 0 and not self.terminate_flag.is_set():
                received_payload += self.conn.recv(remaining_payload_size)
                remaining_payload_size = self.data_size - len(received_payload)
            data = pickle.loads(received_payload)

            self.conn.close()

            with open(self.dirnamme + self.filename, "wb") as file:
                file.write(data)
            if (
                    not self.file_manager.hash_data(self.dirnamme + self.filename)
                        == self.fhash
            ):
                print("Recieved corrupt file, deleting....")
            self.finished = True
            print("File Downlod Finished")
            self.file_manager.addfile(self.dirnamme + self.filename)

        except Exception:  # pylint: disable=broad-exception-caught
            print("File Downloader: Server errored or timed out.")
            # raise(e)
            self.stop()

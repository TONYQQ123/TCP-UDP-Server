import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
import socket
import json
import threading

class UDPClientGUI(QWidget):
    def __init__(self, host, port):
        super().__init__()
        self.data={'num':'0','english':'0'}
        self.host = host
        self.port = port

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.info_label = QLabel("UDP Client is running...")
        self.layout.addWidget(self.info_label)

        self.data_display = QTextEdit()
        self.data_display.setReadOnly(True)
        self.layout.addWidget(self.data_display)

        self.subscribe_num_button = QPushButton("Subscribe/UnSubcribe NUM")
        self.subscribe_num_button.clicked.connect(self.subscribe_num)
        self.layout.addWidget(self.subscribe_num_button)

        self.subscribe_english_button = QPushButton("Subscribe/UnSubcribe ENGLISH")
        self.subscribe_english_button.clicked.connect(self.subscribe_english)
        self.layout.addWidget(self.subscribe_english_button)

        self.stop_button = QPushButton("Stop/ReStart")
        self.stop_button.clicked.connect(self.stop_start)
        self.layout.addWidget(self.stop_button)

        self.start_udp_client()

    def start_udp_client(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.settimeout(300)
        data_bytes = json.dumps(self.data).encode('utf-8')
        self.udp_socket.sendto(data_bytes, (self.host, self.port))

        self.stop = False
        self.client_thread = threading.Thread(target=self.receive_data)
        self.client_thread.start()

    def receive_data(self):
        while not self.stop:
            try:
                data, addr = self.udp_socket.recvfrom(1024)
                message = data.decode()
                self.data_display.append(f"{message}")
            except KeyboardInterrupt:
                self.stop_start()
                break

    def subscribe_num(self):
        if self.data['num']=='1':
            self.data['num'] = '0'
        else:
            self.data['num'] = '1'
        print(self.data)
        data_bytes = json.dumps(self.data).encode('utf-8')
        self.udp_socket.sendto(data_bytes, (self.host, self.port))
        self.info_label.setText("Subscribed to NUM data")

    def subscribe_english(self):
        if self.data['english']=='1':
            self.data['english']='0'
        else:
            self.data['english']='1'
        data_bytes = json.dumps(self.data).encode('utf-8')
        self.udp_socket.sendto(data_bytes, (self.host, self.port))
        self.info_label.setText("Subscribed to ENGLISH data")

    def stop_start(self):
        if not self.stop:
            self.stop = True
            self.udp_socket.close()
            self.info_label.setText("UDP Client is stopped")
        else:
            self.stop=False
            self.start_udp_client()
            self.info_label.setText("UDP Client is running...")

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 9998

    app = QApplication(sys.argv)
    udp_client_window = UDPClientGUI(HOST, PORT)
    udp_client_window.show()
    sys.exit(app.exec_())

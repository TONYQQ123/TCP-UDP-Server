import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
import socket
import json

class EquationSolverWidget(QWidget):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.setWindowTitle("Equation Solver")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.equation_label = QLabel("Enter equation:")
        self.layout.addWidget(self.equation_label)

        self.equation_input = QLineEdit()
        self.layout.addWidget(self.equation_input)

        self.solve_button = QPushButton("Solve")
        self.solve_button.clicked.connect(self.solve_equation)
        self.layout.addWidget(self.solve_button)

        self.result_label = QLabel()
        self.layout.addWidget(self.result_label)

        self.start_tcp()

    def start_tcp(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))

    def solve_equation(self):
        equation = self.equation_input.text()
        result = self.send_equation_to_server(equation)
        result = json.loads(result)
        if result.get('status'):
            self.result_label.setText(f"Result: {result.get('success')}")
        else:
            self.result_label.setText(f"Result: {result.get('error')}")

    def send_equation_to_server(self, equation):
        data = {}
        data['eq'] = equation
        data['mode'] = 'simple'
        bdata = json.dumps(data).encode('utf-8')
        self.s.sendall(bdata)
        result = self.s.recv(1024).decode()

        return result

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 9999

    app = QApplication(sys.argv)
    equation_solver_widget = EquationSolverWidget(HOST, PORT)
    equation_solver_widget.show()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

from udpgui import UDPClientGUI
from Caculate import EquationSolverWidget

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.udp_button = QPushButton("UDP Client")
        self.udp_button.clicked.connect(self.switch_to_udp)
        self.layout.addWidget(self.udp_button)

        self.equation_button = QPushButton("Equation Solver")
        self.equation_button.clicked.connect(self.switch_to_equation)
        self.layout.addWidget(self.equation_button)

        # Initialize UDPClientGUI and EquationSolverWidget
        self.udp_client_widget = UDPClientGUI('127.0.0.1', 9998)
        self.equation_solver_widget = EquationSolverWidget('127.0.0.1', 9999)

        # Hide EquationSolverWidget initially
        self.equation_solver_widget.hide()

    def switch_to_udp(self):
        self.udp_client_widget.show()
        self.equation_solver_widget.hide()

    def switch_to_equation(self):
        self.udp_client_widget.hide()
        self.equation_solver_widget.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_widget = MainWidget()
    main_widget.show()
    sys.exit(app.exec_())

import sys
from time import sleep
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QWidget,
    QVBoxLayout,
    QPushButton,
)


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.click_count = 0
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Freezing GUI")
        self.resize(300, 150)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        # Create and connect widgets
        self.clicksLabel = QLabel("Counting: 0 clicks", self)
        self.clicksLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.stepLabel = QLabel("Long-Running step: 0")
        self.stepLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.countBtn = QPushButton("Click me!", self)
        self.countBtn.clicked.connect(self.countClicks)
        self.longRunningBtn = QPushButton("Long-Running Task!", self)
        self.longRunningBtn.clicked.connect(self.runLongTask)

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.clicksLabel)
        layout.addWidget(self.countBtn)
        layout.addStretch()
        layout.addWidget(self.stepLabel)
        layout.addWidget(self.longRunningBtn)
        self.centralWidget.setLayout(layout)

    def countClicks(self):
        self.click_count += 1
        self.clicksLabel.setText(f"Counting: {self.click_count} clicks")

    def reportProgress(self, n):
        self.stepLabel.setText(f"Long-Running Step: {n}")

    def runLongTask(self):
        """Long-running task in 5 steps."""
        for i in range(5):
            sleep(1)
            self.reportProgress(i + 1)


app = QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec())

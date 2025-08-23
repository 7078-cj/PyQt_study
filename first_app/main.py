from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout
from random import choice

#simple random keyword generator

keywords = ["Python", "PyQt5", "GUI", "Application", "Widget", "Layout"]



#main window class
app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle("My First PyQt5 App")
main_window.resize(300, 200)

#creating app objects
title_text = QLabel("Random Keywords")
text1 = QLabel("?")
text2 = QLabel("?")
text3 = QLabel("?")

#event handler for button click
def on_button_click(text):
    random_keyword = choice(keywords)
    text.setText(f"{random_keyword}")

#button creation
button1 = QPushButton("Click Me")
button2 = QPushButton("Click Me")
button3 = QPushButton("Click Me")

#connecting button click to event handler
button1.clicked.connect(lambda: on_button_click(text1))
button2.clicked.connect(lambda: on_button_click(text2))
button3.clicked.connect(lambda: on_button_click(text3))

#designing layout
master_layout = QVBoxLayout()
row1_layout = QHBoxLayout()
row2_layout = QHBoxLayout()
row3_layout = QHBoxLayout()


row1_layout.addWidget(title_text, alignment=Qt.AlignCenter)

row2_layout.addWidget(text1, alignment=Qt.AlignCenter)
row2_layout.addWidget(text2, alignment=Qt.AlignCenter)
row2_layout.addWidget(text3, alignment=Qt.AlignCenter)

row3_layout.addWidget(button1, alignment=Qt.AlignCenter)  
row3_layout.addWidget(button2, alignment=Qt.AlignCenter)  
row3_layout.addWidget(button3, alignment=Qt.AlignCenter)  

#adding the rows this should be in the order they appear
master_layout.addLayout(row1_layout)
master_layout.addLayout(row2_layout)
master_layout.addLayout(row3_layout)

#setting the main window layout
main_window.setLayout(master_layout)

#show/run app
main_window.show()
app.exec_()
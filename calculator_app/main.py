from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,QGridLayout
from PyQt5.QtGui import QFont

class Calculator(QWidget):
    
    def __init__(self):
        super().__init__()
    
        self.setWindowTitle("Simple Calculator")
        self.resize(250, 300)

        #widgets
        self.text_box = QLineEdit()
        self.text_box.setFont(QFont("Helvetica", 32))
        
        
        self.grid = QGridLayout()

        self.buttons = ['7', '8', '9', '/',
                '4', '5', '6', '*',
                '1', '2', '3', '-',
                '0', '.', '=', '+'
                ]
        
        #adding buttons to grid layout
        row = 0
        col = 0
        for button in self.buttons:
            btn = QPushButton(button)
            btn.clicked.connect(lambda _, b=btn: self.button_click())
            btn.setStyleSheet("QPushButton { font: 25pt Comic Sans MS; padding: 10px; }")
            
            self.grid.addWidget(btn, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        self.clear = QPushButton('C')
        self.clear.setStyleSheet("QPushButton { font: 25pt Comic Sans MS; padding: 10px; }")
        
        self.delete = QPushButton('<-')
        self.delete.setStyleSheet("QPushButton { font: 25pt Comic Sans MS; padding: 10px; }")
        
        #designing layout
        self.master_layout = QVBoxLayout()
        self.master_layout.addWidget(self.text_box)
        self.master_layout.addLayout(self.grid)

        self.button_row = QHBoxLayout()

        self.clear.clicked.connect(lambda _:  self.button_click())
        self.button_row.addWidget( self.clear)

        self.delete.clicked.connect(lambda _:  self.button_click())
        self.button_row.addWidget( self.delete)

        self.master_layout.addLayout(self.button_row)
        self.master_layout.setContentsMargins(25, 25, 25, 25)
        
        self.setLayout(self.master_layout)

    #events
    def button_click(self):
        btn = app.sender()
        current_text = self.text_box.text()
        
        if btn.text() == '=':
            try:
                result = str(eval(current_text))
                
                self.text_box.setText(result)
            except Exception as e:
                self.text_box.setText("Syntax Error")
        
        elif btn.text() != '=':
            if btn.text() == 'C':
                self.text_box.setText("")
            elif btn.text() == '<-':
                self.text_box.setText(current_text[:-1])
            else:
                new_text = current_text + btn.text()
                self.text_box.setText(new_text)
        
        

   

    
if __name__ == "__main__":
    app = QApplication([])
    main_window = Calculator()
    main_window.setStyleSheet("QWidget { background-color: #f0f0f0; }")
    main_window.show()
    app.exec_()
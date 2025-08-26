from PyQt5.QtWidgets import  QDoubleSpinBox, QApplication, QWidget, QLabel, QPushButton, QLineEdit, QLineEdit, QComboBox, QDateEdit, QTableWidget, QVBoxLayout, QHBoxLayout, QTableWidgetItem
import db
from PyQt5.QtCore import QDate

expense = db.ExpenseCRUD()

#app class
class ExpenseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(550, 500)
        self.setWindowTitle("Expense Tracker")
        
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.dropdown = QComboBox()
        
        categories = ["Food", "Utility", "Transport", "Entertainment", "Other"]
        self.dropdown.addItems(categories)
        
        self.amount = QDoubleSpinBox()
        self.amount.setRange(0, 1000000)
        self.amount.setDecimals(2)  
        self.amount.setValue(0.0)
        
        self.description = QLineEdit()
        
        
        self.add_button = QPushButton("Add Expense")
        self.add_button.clicked.connect(self.add_expense)
        
        self.delete_button = QPushButton("Delete Expense")
        self.delete_button.clicked.connect(self.delete_selected_expense)
        
        self.update_button = QPushButton("Update Expense")
        self.update_button.setEnabled(False)
        self.update_button.clicked.connect(self.update_expense)
        
        
        self.table = QTableWidget()
        self.table.setColumnCount(5) # id, date, category, amount, description
        header_names = ["id", "date", "category", "amount", "description"]
        self.table.setHorizontalHeaderLabels(header_names)
        self.populate_table()
        self.table.cellClicked.connect(self.on_row_selected)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        
        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()
        
        self.row1.addWidget(QLabel("Date: "))
        self.row1.addWidget(self.date_box)
        self.row1.addWidget(QLabel("Category: "))
        self.row1.addWidget(self.dropdown)
        
        self.row2.addWidget(QLabel("Amount: "))
        self.row2.addWidget(self.amount)
        self.row2.addWidget(QLabel("Description: "))
        self.row2.addWidget(self.description)
        
        self.row3.addWidget(self.add_button)
        self.row3.addWidget(self.delete_button)
        self.row3.addWidget(self.update_button)
        
        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)
        self.master_layout.addLayout(self.row3)
        
        self.master_layout.addWidget(self.table)
        
        self.setLayout(self.master_layout)
        
    def add_expense(self):
        
        if self.date_box.date().toPyDate() and self.dropdown.currentText() and self.amount.value() and self.description.text().strip():
            
            expense.create(
                date=self.date_box.date().toPyDate(),
                category=self.dropdown.currentText(),
                amount=self.amount.value(),
                description=self.description.text().strip()
            )
            self.date_box.clear()
            self.amount.clear()
            self.description.clear()
            self.populate_table()
        else:
            print("no data")
        
    def get_expenses(self):
        result = expense.get_all()
        return result
    
    def populate_table(self):
        expenses = self.get_expenses()
        self.table.setRowCount(len(expenses))
        for row, expense in enumerate(expenses):
            self.table.setItem(row, 0, QTableWidgetItem(str(expense.id)))
            self.table.setItem(row, 1, QTableWidgetItem(str(expense.date)))
            self.table.setItem(row, 2, QTableWidgetItem(expense.category))
            self.table.setItem(row, 3, QTableWidgetItem(str(expense.amount)))
            self.table.setItem(row, 4, QTableWidgetItem(expense.description))
            
    def delete_selected_expense(self):
        selected_row = self.table.currentRow()  
        if selected_row == -1:
            print("No row selected")
            return

        expense_id_item = self.table.item(selected_row, 0)
        if expense_id_item:
            expense_id = int(expense_id_item.text())
            
            expense.delete(expense_id)
            
            self.table.removeRow(selected_row)
            print(f"Deleted expense ID {expense_id}")
            
    def on_row_selected(self, row, column):
       
        self.selected_id = int(self.table.item(row, 0).text())
        date_str = self.table.item(row, 1).text()
        category = self.table.item(row, 2).text()
        amount = float(self.table.item(row, 3).text())
        description = self.table.item(row, 4).text()

        
        self.date_box.setDate(QDate.fromString(date_str, "yyyy-MM-dd"))
        
        index = self.dropdown.findText(category)
        if index >= 0:
            self.dropdown.setCurrentIndex(index)
        
        self.amount.setValue(amount)
        self.description.setText(description)

        
        self.add_button.setEnabled(False)
        self.update_button.setEnabled(True)
        
    def update_expense(self):
        if not hasattr(self, "selected_id"):
            print("No expense selected")
            return

        # Read current input values
        date_value = self.date_box.date().toPyDate()
        category_value = self.dropdown.currentText()
        amount_value = self.amount.value()
        description_value = self.description.text().strip()

        if not description_value:
            print("Description required")
            return

        # Update in DB
        expense.update(self.selected_id,
                    date=date_value.strftime("%Y-%m-%d"),
                    category=category_value,
                    amount=amount_value,
                    description=description_value)

        self.populate_table()

        # Reset input fields and buttons
        self.date_box.setDate(QDate.currentDate())
        self.amount.setValue(0.0)
        self.description.clear()
        self.dropdown.setCurrentIndex(0)

        self.add_button.setEnabled(True)
        self.update_button.setEnabled(False)
        del self.selected_id
        
    def on_selection_changed(self):
        selected_items = self.table.selectedItems()
        
        if not selected_items:
            # No row is selected → reset to Add mode
            self.add_button.setEnabled(True)
            self.update_button.setEnabled(False)
            
            # Clear input fields
            self.date_box.setDate(QDate.currentDate())
            self.amount.setValue(0.0)
            self.description.clear()
            self.dropdown.setCurrentIndex(0)
            
            # Forget previous selection
            if hasattr(self, "selected_id"):
                del self.selected_id

    
        
        
if __name__ in "__main__":
    app = QApplication([])
    main = ExpenseApp()
    main.show()
    app.exec()
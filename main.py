import sys
import sqlite3
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QTableWidgetItem, QDialog, QMessageBox

class CoffeeApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(CoffeeApp, self).__init__()
        uic.loadUi("main.ui", self)
        self.setWindowTitle("Информация о кофе")
        self.load_coffee_data()

        self.pushButtonAdd.clicked.connect(self.add_coffee)
        self.pushButtonEdit.clicked.connect(self.edit_coffee)

    def load_coffee_data(self):
        conn = sqlite3.connect('coffee.sqlite3')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM coffee")
        rows = cursor.fetchall()

        self.tableWidget.setRowCount(len(rows))

        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        self.tableWidget.resizeColumnsToContents()

        conn.close()

    def add_coffee(self):
        self.addEditForm = AddEditCoffeeForm()
        self.addEditForm.setWindowTitle("Добавить новое кофе")
        self.addEditForm.show()
        self.addEditForm.exec()

        self.load_coffee_data()

    def edit_coffee(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите кофе для редактирования.")
            return

        coffee_id = self.tableWidget.item(selected_row, 0).text()
        name = self.tableWidget.item(selected_row, 1).text()
        roast_level = self.tableWidget.item(selected_row, 2).text()
        ground_or_beans = self.tableWidget.item(selected_row, 3).text()
        taste_description = self.tableWidget.item(selected_row, 4).text()
        price = self.tableWidget.item(selected_row, 5).text()
        packaging_size = self.tableWidget.item(selected_row, 6).text()

        self.addEditForm = AddEditCoffeeForm(coffee_id, name, roast_level, ground_or_beans, taste_description, price, packaging_size)
        self.addEditForm.setWindowTitle("Редактировать кофе")
        self.addEditForm.show()
        self.addEditForm.exec()

        self.load_coffee_data()


class AddEditCoffeeForm(QDialog):
    def __init__(self, coffee_id=None, name="", roast_level="", ground_or_beans="", taste_description="", price="", packaging_size=""):
        super(AddEditCoffeeForm, self).__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)

        self.coffee_id = coffee_id
        self.nameEdit.setText(name)
        self.roastLevelEdit.setText(roast_level)
        self.groundOrBeansEdit.setText(ground_or_beans)
        self.tasteDescriptionEdit.setPlainText(taste_description)
        self.priceEdit.setText(price)
        self.packagingSizeEdit.setText(packaging_size)

        self.saveButton.clicked.connect(self.save_coffee)

    def save_coffee(self):
        name = self.nameEdit.text()
        roast_level = self.roastLevelEdit.text()
        ground_or_beans = self.groundOrBeansEdit.text()
        taste_description = self.tasteDescriptionEdit.toPlainText()
        price = float(self.priceEdit.text())
        packaging_size = float(self.packagingSizeEdit.text())

        if self.coffee_id:
            self.update_coffee(self.coffee_id, name, roast_level, ground_or_beans, taste_description, price, packaging_size)
        else:
            self.add_new_coffee(name, roast_level, ground_or_beans, taste_description, price, packaging_size)

        self.close()

    def add_new_coffee(self, name, roast_level, ground_or_beans, taste_description, price, packaging_size):
        conn = sqlite3.connect('coffee.sqlite3')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO coffee (name, roast_level, ground_or_beans, taste_description, price, packaging_size)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, roast_level, ground_or_beans, taste_description, price, packaging_size))
        conn.commit()
        conn.close()

    def update_coffee(self, coffee_id, name, roast_level, ground_or_beans, taste_description, price, packaging_size):
        conn = sqlite3.connect('coffee.sqlite3')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE coffee
            SET name = ?, roast_level = ?, ground_or_beans = ?, taste_description = ?, price = ?, packaging_size = ?
            WHERE id = ?
        """, (name, roast_level, ground_or_beans, taste_description, price, packaging_size, coffee_id))
        conn.commit()
        conn.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())

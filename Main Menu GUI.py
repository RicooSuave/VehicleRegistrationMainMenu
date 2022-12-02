import sqlite3
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

# Main Menu UI and button functionalities.
class MainMenu(QMainWindow):
    def __init__(self):
        super(MainMenu, self).__init__()
        loadUi("mainmenu.ui", self)
        self.setWindowTitle("Main Menu- Vehicle Registration Database")

        # Add New Vehicle Button on Main Menu.
        self.gotoaddnew = AddNew()
        self.pushButton.clicked.connect(self.gotoaddnew.show)

        # Check Licence Plate Button on Main Menu.
        self.gotocheck = CheckLicense()
        self.pushButton_2.clicked.connect(self.gotocheck.show)

        # View List Button on Main Menu
        self.database = ViewList()
        self.pushButton_3.clicked.connect(self.database.show)


    # Add new vehicle form UI (AddNew) - includes save and clear function.

# Add New Vehicle UI and button functionalities.
class AddNew(QWidget):
    def __init__(self):
        super(AddNew, self).__init__()
        loadUi("addnew-widget.ui", self)
        self.setWindowTitle("Add New Vehicle Form")

        # Clear Button Function when clicked.
        self.pushButton.clicked.connect(self.ClearData)

        # Save Button Function when clicked.
        self.pushButton_2.clicked.connect(self.SaveData)

        # Making sure the 'Year' field input only captures numbers.
        self.onlyInt = QIntValidator()
        self.lineEdit_4.setValidator(self.onlyInt)

    # Connecting form data to SQL database.
    def SaveData(self):
        name = self.lineEdit.text()
        make = self.lineEdit_2.text()
        model = self.lineEdit_3.text()
        year = self.lineEdit_4.text()
        license_plate = self.lineEdit_5.text()
        error = QMessageBox()

        # If statement function, only save if all fields have values.
        if len(name)==0 or len(make)==0 or len(model)==0 or len(year)==0 or len(license_plate)==0:
            error.setIcon(QMessageBox.Critical)
            error.setText("Error!")
            error.setInformativeText('MISSING INFO!')
            error.setWindowTitle("Error")
            error.exec_()

        else:
            conn = sqlite3.connect("Vehicle_Registration_Database.db")
            cur = conn.cursor()

            # Importing data from form to SQL database with those columns.
            form_info = [name, make, model, year, license_plate]
            #CREATE SQL QUERY PULLING DATA DIRECTLY TO TABLE, FIGURE OUT HOW!
            cur.execute(f"INSERT INTO Vehicle_Registration_List (name,make,model,year,license_plate) VALUES ('{name}','{make}','{model}','{year}','{license_plate}')")

            conn.commit()
            conn.close()

            # Clearing form data after it saves to Database.
            self.ClearData()
            self.close()

    # Clearing data from form after button is clicked.
    def ClearData(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()

# Check Licence Plate UI and button functionality.
class CheckLicense(QWidget):
    def __init__(self):
        super(CheckLicense, self).__init__()
        loadUi("checklicense.ui", self)
        self.setWindowTitle("License Plate Validator")

        # Setting up Check License Plate # Button to run the Query.
        self.pushButton.clicked.connect(self.VerifyLicense)

    # Full Query, returns error if license plate number does not exist in database.
    def VerifyLicense(self):
        license = self.lineEdit.text()
        error = QMessageBox()
        success = QMessageBox()

        if len(license)==0:
            error.setIcon(QMessageBox.Critical)
            error.setText("Error!")
            error.setInformativeText('Please Input License Plate #!')
            error.setWindowTitle("Error")
            error.exec_()
        else:
            conn = sqlite3.connect("Vehicle_Registration_Database.db")
            cur = conn.cursor()

            # SQL Query to compare user input to the database.
            # query = 'SELECT License_Plate FROM Vehicle_Registration_List WHERE License_Plate = \''+license+'\''
            query = f"SELECT License_Plate FROM Vehicle_Registration_List WHERE License_Plate = '{license}'"
            cur.execute(query)

            # Fetch SQL result and chooses message box to display.
            result_license = cur.fetchall()

            # If there is a "value", then proceed.
            if result_license:
                success.setIcon(QMessageBox.Information)
                success.setText("Valid!")
                success.setInformativeText('Vehicle is in the Database!')
                success.setWindowTitle("Success")
                success.exec_()
            else:
                error.setIcon(QMessageBox.Critical)
                error.setText("Error")
                error.setInformativeText('No Records Found, Please Try Again OR Add New Vehicle to Database.')
                error.setWindowTitle("Error")
                error.exec_()

        # Closing License Validation window after error is closed, need to adjust it to where window stays open if
        # license is incorrect to give user another chance to enter the right License_Plate.
        self.lineEdit.clear()
        self.close()

# View List UI - Records Table UI from DB with button functionalities.
class ViewList(QWidget):
    # Class Attribute
    currentlicenseplate: str = ""
    def __init__(self):
        super(ViewList, self).__init__()
        loadUi("viewlist.ui", self)
        self.setWindowTitle("Vehicle Registration Database")

        self.tableWidget.setHorizontalHeaderLabels(["Name", "Make", "Model", "Year", "License Plate #"])
        self.LoadData()
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

        # Add New Vehicle Button - Once pressed it will launch the add new vehicle module/window.
        self.gotoaddnew = AddNew()
        self.pushButton.clicked.connect(self.gotoaddnew.show)

        # Refresh button - once clicked it will run database query again.
        self.pushButton_4.clicked.connect(self.LoadData)

        # Delete button - runs DeleteRecord module below.
        self.pushButton_2.clicked.connect(self.DeleteRecord)

        # Edit button - runs EditRecord module below.
        self.pushButton_3.clicked.connect(self.EditRecord)

        # Save button - overwrites database based off what the tableWidget displays. Runs SaveData module below.
        self.pushButton_5.clicked.connect(self.SaveChanges)

        self.currentlicenseplate = None
        self.tableWidget.cellClicked.connect(self.SaveLicenseAttri)

    # This module saves the first click of the row's Licence Plate value, and saves it to the class attribute (
    # currentlicenseplate). We then call this attribute in the SQL query for 'EditRecord'.
    def SaveLicenseAttri(self,row):
        rowvalue = self.tableWidget.item(row, 4)
        error = QMessageBox()

        if rowvalue == None:
            error.setIcon(QMessageBox.Critical)
            error.setText("Error!")
            error.setInformativeText('PLEASE SELECT A CELL ON THE ROW YOU CHOSE TO EDIT!')
            error.setWindowTitle("Error")
            error.exec_()

        else:
            self.currentlicenseplate = rowvalue.text()

    # Populate Table Widget with data from Database
    def LoadData(self):
        conn = sqlite3.connect("Vehicle_Registration_Database.db")
        cur = conn.cursor()
        query = 'SELECT * FROM Vehicle_Registration_List'

        # Setting up Rows and Columns limits
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(5)

        # Extracting data from query into TableWidget
        for tablerow, row in enumerate(cur.execute(query)):
            self.tableWidget.setItem(tablerow, 0, QTableWidgetItem(row[0]))
            self.tableWidget.setItem(tablerow, 1, QTableWidgetItem(row[1]))
            self.tableWidget.setItem(tablerow, 2, QTableWidgetItem(row[2]))
            self.tableWidget.setItem(tablerow, 3, QTableWidgetItem(str(row[3])))
            self.tableWidget.setItem(tablerow, 4, QTableWidgetItem(row[4]))

        conn.close()

    # Delete Record Button Function.
    def DeleteRecord(self):
        # Pulling row ID and getting value from License_Plate coloumn
        rowid = self.tableWidget.currentRow()
        rowvalue = self.tableWidget.item(rowid, 4)

        # Connecting to Database and executing delete SQL command.
        conn = sqlite3.connect("Vehicle_Registration_Database.db")
        cur = conn.cursor()
        query = f"DELETE FROM Vehicle_Registration_List WHERE License_Plate = '{rowvalue.text()}'" #Get text

        # Deletes row from Gui Table.
        self.tableWidget.removeRow(rowid)

        cur.execute(query)
        conn.commit()
        conn.close()

    # Edit Records Button Function.
    def EditRecord(self):
        row = self.tableWidget.currentRow()
        rowvalue = self.tableWidget.item(row, 4)
        error = QMessageBox()

        if rowvalue == None:
            error.setIcon(QMessageBox.Critical)
            error.setText("Error!")
            error.setInformativeText('PLEASE SELECT A ROW WITH DATA TO CHANGE IT!')
            error.setWindowTitle("Error")
            error.exec_()
        else:
            self.tableWidget.setEditTriggers(QAbstractItemView.AnyKeyPressed|QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed|QAbstractItemView.SelectedClicked)

     # Save Changes Button Function.
    def SaveChanges(self):
        #1. Needs to save (OLD) license plate data BEFORE changes are made.
        #2. Record ID

        rowid = self.tableWidget.currentRow()
        rowvalue1 = self.tableWidget.item(rowid, 0)
        rowvalue2 = self.tableWidget.item(rowid, 1)
        rowvalue3 = self.tableWidget.item(rowid, 2)
        rowvalue4 = self.tableWidget.item(rowid, 3)
        rowvalue5 = self.tableWidget.item(rowid, 4)

        conn = sqlite3.connect("Vehicle_Registration_Database.db")
        cur = conn.cursor()

        query = f"UPDATE Vehicle_Registration_List SET Name='{rowvalue1.text()}', Make='{rowvalue2.text()}', Model='{rowvalue3.text()}', Year='{rowvalue4.text()}', License_Plate='{rowvalue5.text()}' WHERE License_Plate = '{self.currentlicenseplate}'"
        cur.execute(query)

        conn.commit()
        conn.close()

        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

# Main - What makes the application run.
if __name__ == '__main__':
    app = QApplication([])
    window = MainMenu()
    window.show()
    app.exec_()
import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QListWidget, QLabel, QFormLayout, QDialog, QMessageBox, QScrollArea, QCheckBox
)
from PyQt5.QtCore import Qt

import sqlite3

from add_patient_details import AddPatientDialog




class HospitalManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hospital Management System")
        # self.setGeometry(100, 100, 1000, 600)
        self.showMaximized()
        self.conn = sqlite3.connect("hospital.db")  # Database file
        self.cursor = self.conn.cursor()
        self.create_table()
        self.initUI()
        self.load_data()

    def initUI(self):
        # Main layout
        main_layout = QHBoxLayout(self)

        # Sidebar
        sidebar = QListWidget()
        sidebar.addItems(["Patients", "Appointments", "Invoice"])
        sidebar.setFixedWidth(200)

        # Right side (content)
        right_layout = QVBoxLayout()

        # Buttons and search
        top_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add")
        self.delete_btn = QPushButton("Delete")
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search...")
        # self.search_btn = QPushButton("Search")

        self.add_btn.clicked.connect(self.open_add_dialog)
        self.delete_btn.clicked.connect(self.delete_selected_rows)

        top_layout.addWidget(self.add_btn)
        top_layout.addWidget(self.delete_btn)
        top_layout.addStretch()
        top_layout.addWidget(self.search_box)
        # top_layout.addWidget(self.search_btn)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(15)
        self.table.setHorizontalHeaderLabels([
            "Patient Id", "Name", "Mobile No.", "Last Visit", "Diagnosis", "Age",
            "Gender", "Address", "City", "State", "Pincode",
            "Email", "Doctor Assigned", "Room No", "Status"
        ])

        dummy_data = [
            [1, "John Doe", "9876543210", "2025-09-01", "Fever", 30, "Male", "123 Street", "Delhi", "Delhi", "110001", "john@example.com", "Dr. Smith", "101", "Admitted"],
            [2, "Jane Smith", "8765432109", "2025-08-28", "Diabetes", 45, "Female", "456 Road", "Mumbai", "Maharashtra", "400001", "jane@example.com", "Dr. Mehta", "102", "Discharged"],
            [3, "Mike Johnson", "7654321098", "2025-09-10", "Fracture", 28, "Male", "789 Avenue", "Bangalore", "Karnataka", "560001", "mike@example.com", "Dr. Reddy", "103", "Under Treatment"],
        ]

        # self.table.setRowCount(len(dummy_data))
        # for row, record in enumerate(dummy_data):
        #     for col, item in enumerate(record):
        #         self.table.setItem(row, col, QTableWidgetItem(str(item)))

        # for row, record in enumerate(dummy_data):
        #     for col, item in enumerate(record):
        #         cell = QTableWidgetItem(str(item))
        #         cell.setTextAlignment(Qt.AlignCenter)   # Center align
        #         self.table.setItem(row, col, cell)


        # Add to right layout
        right_layout.addLayout(top_layout)
        right_layout.addWidget(self.table)

        # Add sidebar and right section to main layout
        main_layout.addWidget(sidebar)
        main_layout.addLayout(right_layout)

    def load_data(self):
        """Fetch data from DB and load into table"""
        self.cursor.execute("SELECT * FROM patients")
        rows = self.cursor.fetchall()

        self.table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            # Add checkbox
            checkbox = QCheckBox()
            checkbox.setStyleSheet("margin-left:20%;")  # align nicely
            self.table.setCellWidget(row_idx, 0, checkbox)
            for col_idx, item in enumerate(row_data):
                cell = QTableWidgetItem(str(item))
                cell.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_idx, col_idx, cell)

    def open_add_dialog(self):
        """Open Add Patient popup"""
        dialog = AddPatientDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            patient_data = dialog.new_patient
            self.cursor.execute("""
                INSERT INTO patients (
                    name, mobile, last_visit, diagnosis, age, gender,
                    address, city, state, pincode, email,
                    doctor_assigned, room_no, status
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, patient_data)
            self.conn.commit()
            self.load_data()  # Refresh table

    def delete_selected_rows(self):
        """Delete all checked patients from DB and refresh table"""
        rows_to_delete = []
        for row in range(self.table.rowCount()):
            widget = self.table.cellWidget(row, 0)
            if isinstance(widget, QCheckBox) and widget.isChecked():
                patient_id_item = self.table.item(row, 0)  # Patient Id is at col=1
                if patient_id_item:
                    rows_to_delete.append(patient_id_item.text())

        if not rows_to_delete:
            QMessageBox.warning(self, "No Selection", "Please check at least one row to delete.")
            return

        confirm = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete {len(rows_to_delete)} patient(s)?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            print('rows_to_delete: ', rows_to_delete)
            for patient_id in rows_to_delete:
                self.cursor.execute("DELETE FROM patients WHERE patient_id=?", (patient_id,))
            self.conn.commit()
            self.load_data()

    def closeEvent(self, event):
        """Close DB connection when app closes"""
        self.conn.close()
        event.accept()


    def closeEvent(self, event):
        """Close DB connection when app closes"""
        self.conn.close()
        event.accept()


    def create_table(self):
        """Create patients table if not exists"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY,
                name TEXT,
                mobile TEXT,
                last_visit TEXT,
                diagnosis TEXT,
                age INTEGER,
                gender TEXT,
                address TEXT,
                city TEXT,
                state TEXT,
                pincode TEXT,
                email TEXT,
                doctor_assigned TEXT,
                room_no TEXT,
                status TEXT
            )
        """)
        self.conn.commit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HospitalManagement()
    window.show()
    app.exec_()





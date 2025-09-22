from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QLabel, QPushButton, QMessageBox
)


class AddPatientDialog(QDialog):
    """Popup form to add new patient"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Patient")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.inputs = {}

        fields = [
            "Name", "Mobile No.", "Last Visit", "Diagnosis", "Age", "Gender",
            "Address", "City", "State", "Pincode", "Email",
            "Doctor Assigned", "Room No", "Status"
        ]

        for field in fields:
            line_edit = QLineEdit()
            form_layout.addRow(QLabel(field), line_edit)
            self.inputs[field] = line_edit

        layout.addLayout(form_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        save_btn.clicked.connect(self.save_patient)
        cancel_btn.clicked.connect(self.close)

    def save_patient(self):
        """Collect form data and return as tuple"""
        data = []
        for field, widget in self.inputs.items():
            value = widget.text().strip()
            if not value and field not in ["Last Visit", "Diagnosis", "Status"]:  
                QMessageBox.warning(self, "Validation Error", f"{field} cannot be empty.")
                return
            data.append(value)

        self.new_patient = tuple(data)
        self.accept()

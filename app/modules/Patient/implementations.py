# app/modules/patient/implementations.py
from .base import PatientBase

class PrintablePatient(PatientBase):
    """
    PatientBase için örnek implementasyon
    (abstract class test/demo amaçlı)
    """

    def get_priority(self) -> int:
        return 99

    def detailed_info(self) -> str:
        return (
            f"ID: {self.patient_id}, "
            f"Ad: {self.name}, "
            f"Yaş: {self.age}, "
            f"Durum: {self.status}"
        )
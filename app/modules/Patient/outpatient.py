# app/modules/patient/outpatient.py

from .base import PatientBase
from datetime import datetime
from typing import Optional, List

class Outpatient(PatientBase):
    """
    Ayaktan hasta sınıfı
    """

    def __init__(self, patient_id: Optional[int],  name: str, age: int, gender: str, appointment_date: Optional[str] = None, status: str = "aktif"
    ):
        super().__init__(patient_id, name, age, gender, status)

        self._appointment_history: List[str] = []
        self.appointment_date = appointment_date

    # property
    @property
    def appointment_date(self) -> Optional[str]:
        return self._appointment_date

    @appointment_date.setter
    def appointment_date(self, value: Optional[str]):
        if value is not None:
            try:
                datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                raise ValueError(
                    "Randevu tarihi 'YYYY-MM-DD' formatında olmalıdır."
                )
        self._appointment_date = value

    # abstract method override
    def get_priority(self) -> int:
        """Outpatient için düşük öncelik"""
        return 3

    def detailed_info(self) -> str:
        base_info = super().detailed_info()
        return (
            f"{base_info}\n"
            f"Randevu Tarihi: {self.appointment_date or '-'}"
        )

    # base davranışı override
    def update_status(self, new_status: str):
        if new_status in ("iptal", "tamamlandı") and self._appointment_date:
            self._appointment_history.append(self._appointment_date)
            self._appointment_date = None

        super().update_status(new_status)

    # yardımcı davranış
    def has_appointment(self) -> bool:
        return self._appointment_date is not None

    def get_appointment_history(self) -> List[str]:
        """ Hastanın geçmiş randevularını döndürür """
        return list(self._appointment_history)

# app/modules/appointment/base.py

from abc import ABC, abstractmethod
from datetime import datetime


class AppointmentBase(ABC):

    def __init__(
        self,
        appointment_id: int,
        patient_id: int,
        doctor_name: str,
        date_time: datetime
    ):
        self._appointment_id = appointment_id
        self._patient_id = patient_id
        self._doctor_name = doctor_name
        self._date_time = date_time
        self._status = "scheduled"
        self._created_at = datetime.now()

        if not self.validate_datetime(date_time):
            raise ValueError("Geçersiz tarih bilgisi")
        

    # Randevuya ait detaylı bilgileri döndürür
    @abstractmethod
    def get_details(self) -> str:
        pass

    # Randevuya ait kısa özet bilgiyi döndürür
    @abstractmethod
    def get_summary(self) -> str:
        pass

    def get_appointment_id(self) -> int:
        return self._appointment_id

    def get_patient_id(self) -> int:
        return self._patient_id

    def set_patient_id(self, patient_id: int):
        if patient_id <= 0:
            raise ValueError("Hasta ID pozitif olmalıdır")
        self._patient_id = patient_id

    def get_doctor_name(self) -> str:
        return self._doctor_name

    def set_doctor_name(self, doctor_name: str):
        if not doctor_name.strip():
            raise ValueError("Doktor adı boş olamaz")
        self._doctor_name = doctor_name

    def get_date_time(self) -> datetime:
        return self._date_time

    def set_date_time(self, new_datetime: datetime):
        if not self.validate_datetime(new_datetime):
            raise ValueError("Geçersiz tarih")
        self._date_time = new_datetime

    def get_status(self) -> str:
        return self._status

    def set_status(self, status: str):
        allowed = ["scheduled", "cancelled", "completed", "in_progress"]
        if status not in allowed:
            raise ValueError("Geçersiz randevu durumu")
        self._status = status

    def get_created_at(self) -> datetime:
        return self._created_at

    def cancel(self):
        self._status = "cancelled"

    def complete(self):
        self._status = "completed"

    def start(self):
        self._status = "in_progress"

    def reschedule(self, new_datetime: datetime):
        self.set_date_time(new_datetime)
        self._status = "scheduled"

    def is_active(self) -> bool:
        return self._status == "scheduled" and self._date_time >= datetime.now()

    def is_cancelled(self) -> bool:
        return self._status == "cancelled"

    def is_completed(self) -> bool:
        return self._status == "completed"

    @staticmethod
    def validate_datetime(dt) -> bool:
        return isinstance(dt, datetime)

    @classmethod
    def get_module_name(cls) -> str:
        return "Randevu Modülü"

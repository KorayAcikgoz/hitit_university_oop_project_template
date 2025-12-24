# app/modules/patient/inpatient.py

from .base import PatientBase
from typing import Optional
from .emergency_patient import EmergencyPatient

class Inpatient(PatientBase):
    """
    Yatan hasta sınıfı
    """
    
    _max_capacity = 16
    _current_inpatients = 0

    def __init__(self, patient_id: Optional[int], name: str, age: int, gender: str, room_number: Optional[int] = None, status: str = "aktif"
    ):
        # kapasite kontrolü
        if Inpatient._current_inpatients >= Inpatient._max_capacity:
            raise ValueError("Yatan hasta kapasitesi dolu! Yeni hasta kabul edilemiyor.")

        super().__init__(patient_id, name, age, gender, status)

        self.room_number = room_number
        self._is_discharged = False 

        Inpatient._current_inpatients += 1

    # property metotları
    @property
    def room_number(self):
        return self._room_number

    @room_number.setter
    def room_number(self, value):
        if value is not None and value <= 0:
            raise ValueError("Oda numarası pozitif bir sayı olmalıdır.")
        self._room_number = value

    # abstract method override
    def get_priority(self) -> int:
        """Inpatient için orta öncelik"""
        return 2

    def detailed_info(self) -> str:
        base_info = super().detailed_info()
        return (
            f"{base_info}\n"
            f"Oda No        : {self.room_number}"
        )

    # class methods
    @classmethod
    def get_capacity_info(cls):
        return f"Aktif yatan hasta sayısı: {cls._current_inpatients}/{cls._max_capacity}"

    @classmethod
    def _decrease_capacity(cls):
        if cls._current_inpatients > 0:
            cls._current_inpatients -= 1

    # base davranışı override
    def update_status(self, new_status: str):
        if new_status == "taburcu" and not self._is_discharged:
            Inpatient._decrease_capacity()
            self._is_discharged = True
            self.clear_room()

        super().update_status(new_status)
        
    def clear_room(self):
        """ Hasta taburcu edildiğinde oda bilgisini temizler """
        self._room_number = None
        
    @classmethod
    def from_emergency(
        cls,
        emergency_patient: "EmergencyPatient",
        room_number: int
    ):
        """ Emergency hastayı Inpatient'a dönüştürür """
        inpatient = cls(
            patient_id=emergency_patient.patient_id,
            name=emergency_patient.name,
            age=emergency_patient.age,
            gender=emergency_patient.gender,
            room_number=room_number,
            status="aktif"
        )

        return inpatient
    
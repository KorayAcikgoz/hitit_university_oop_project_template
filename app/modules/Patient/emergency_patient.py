# app/modules/patient/emergency_patient.py

from .base import PatientBase
from datetime import datetime
from typing import Optional, List


class EmergencyPatient(PatientBase):
    """
    Acil Hasta Sınıfı
    Semptomlara göre Yeşil / Sarı / Kırmızı alan belirler
    """

    def __init__(
        self,
        patient_id: int,
        name: str,
        age: int,
        gender: str,
        emergency_level: int,
        arrival_time: Optional[datetime] = None,
        status: str = "acil"
    ):
        super().__init__(patient_id, name, age, gender, status)

        if emergency_level not in (1, 2, 3):
            raise ValueError("Acil seviye 1, 2 veya 3 olmalıdır")

        self._emergency_level = emergency_level
        self._arrival_time = arrival_time or datetime.now()
        self._symptoms: List[str] = []

 

    @property
    def emergency_level(self) -> int:
        return self._emergency_level

    @property
    def arrival_time(self) -> datetime:
        return self._arrival_time

    @property
    def symptoms(self) -> List[str]:
        return list(self._symptoms)


    def get_priority(self) -> int:
        return {
            1: 100, 
            2: 80,   
            3: 60    
        }[self._emergency_level]

    def describe(self) -> str:
        return (
            f"[ACİL HASTA] "
            f"ID: {self.patient_id}, "
            f"Ad: {self.name}, "
            f"Yaş: {self.age}, "
            f"Cinsiyet: {self.gender}, "
            f"Alan: {self.determine_triage_area()}, "
            f"Semptomlar: {', '.join(self._symptoms) if self._symptoms else 'Yok'}, "
            f"Geliş Zamanı: {self._arrival_time.strftime('%Y-%m-%d %H:%M')}, "
            f"Durum: {self.status}"
        )
        
    
    def add_symptoms(self, symptoms: List[str]):
        self._symptoms.extend(symptoms)

    def determine_triage_area(self) -> str:
        """
        Semptomlara göre triyaj alanı belirler
        """

        if (
            "bilinç kaybı" in self._symptoms or
            "nefes darlığı" in self._symptoms or
            "şiddetli göğüs ağrısı" in self._symptoms
        ):
            return "Kırmızı Alan"

        elif (
            "yüksek ateş" in self._symptoms or
            "şiddetli baş ağrısı" in self._symptoms or
            "şiddetli karın ağrısı" in self._symptoms
        ):
            return "Sarı Alan"

        return "Yeşil Alan"


    def update_status(self, new_status: str):
        valid_statuses = ["acil", "stabil", "taburcu"]

        if new_status not in valid_statuses:
            raise ValueError("Geçersiz acil hasta durumu")

        self._status = new_status


    def stabilize(self):
        self.update_status("stabil")

    def escalate(self):
        if self._emergency_level > 1:
            self._emergency_level -= 1
            self._status = "acil"

    def __str__(self):
        return self.describe()
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
        patient_id: Optional[int],
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
        self._triage_area: Optional[str] = None

    # property metotları
    @property
    def triage_area(self) -> Optional[str]:
        return self._triage_area
    
    @property
    def emergency_level(self) -> int:
        return self._emergency_level

    @emergency_level.setter   
    def emergency_level(self, value: int):
        if value not in (1, 2, 3):
            raise ValueError("Acil seviye 1-3 arasında olmalıdır")
        self._emergency_level = value

    @property
    def arrival_time(self) -> datetime:
        return self._arrival_time

    @property
    def symptoms(self) -> List[str]:
        return list(self._symptoms)

    def get_priority(self) -> int:
        """
        Acil seviyeye göre hastanın öncelik puanını döndürür
        """
        return {
            1: 100, 
            2: 80,   
            3: 60    
        }[self._emergency_level]

    def detailed_info(self) -> str:
        base_info = super().detailed_info()
        return (
            f"{base_info}\n"
            f"Acil Seviye   : {self.emergency_level}\n"
            f"Triyaj Alanı  : {self.triage_area or self.determine_triage_area()}\n"
            f"Geliş Zamanı : {self.arrival_time.strftime('%Y-%m-%d %H:%M')}"
        )
        
    
    def add_symptoms(self, symptoms: List[str]):
        """
        Hastaya bir veya birden fazla semptom ekler
        """
        self._symptoms.extend(symptoms)

    def determine_triage_area(self) -> str:
        """
        Semptomlara göre triyaj alanını ve acil seviyeyi belirler
        """
        text = " ".join(s.lower() for s in self._symptoms)

        if any(k in text for k in ["göğüs ağrısı", "nefes darlığı", "bilinç kaybı", "şiddetli kanama"]):
            self._emergency_level = 3
            self._triage_area = "Kırmızı"
        elif any(k in text for k in ["yüksek ateş", "şiddetli ağrı", "kusma", "baş dönmesi"]):
            self._emergency_level = 2
            self._triage_area = "Sarı"
        else:
            self._emergency_level = 1
            self._triage_area = "Yeşil"

        return self._triage_area

    def update_status(self, new_status: str):
        """
        Acil hastanın durumunu günceller
        """
        super().update_status(new_status)


    def stabilize(self):
        """
        Hastayı stabil duruma geçirir
        """
        self.update_status("stabil")

    def escalate(self):
        """
        Hastanın acil seviyesini yükseltir
        """
        if self._emergency_level > 1:
            self._emergency_level -= 1
            self.update_status("acil")

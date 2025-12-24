# app/modules/patient/base.py

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional


class PatientBase(ABC):
    """
    Soyut Hasta Sınıfı
    Tüm hasta tipleri için ortak davranışları ve kuralları içerir.
    """

    # class attributes
    _hospital_name = "Ada Hospital"
    
    # sistemde geçerli hasta durumları
    _valid_statuses = ("aktif", "acil", "stabil", "taburcu", "iptal", "tamamlandı")

    def __init__(self, patient_id: Optional[int], name: str, age: int, gender: str, status: str = "aktif"):
        self._patient_id = patient_id
        self.name = name                  
        self.age = age                   
        self.gender = gender
        self._status = None
        self._status_history: list[tuple[str, datetime]] = []
        self.update_status(status)

    # property metotları
    @property
    def patient_id(self) -> Optional[int]:
        return self._patient_id
    
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value or not value.strip():
            raise ValueError("İsim alanı boş bırakılamaz")
        self._name = self.normalize_name(value)

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int):
        if not self.validate_age(value):
            raise ValueError("Geçersiz yaş değeri")
        self._age = value

    @property
    def gender(self) -> str:
        return self._gender

    @gender.setter
    def gender(self, value: str):
        if value.capitalize() not in ("Erkek", "Kadın"):
            raise ValueError("Geçersiz cinsiyet")
        self._gender = value.capitalize()
    
    @property
    def status(self) -> str:
        return self._status

    # durum yönetimi
    def update_status(self, new_status: str):
        """ Hasta durumunu günceller ve geçmişe kaydeder """
        if new_status not in self._valid_statuses:
            raise ValueError(f"Geçersiz hasta durumu: {new_status}")

        self._status = new_status
        self._status_history.append((new_status, datetime.now()))

    def get_status_history(self):
        """ Hastanın tüm durum geçmişini döndürür """
        return list(self._status_history)

    # abstract metotlar
    @abstractmethod
    def get_priority(self) -> int:
        """ Hasta öncelik seviyesini döndürür """
        pass

    @abstractmethod
    def detailed_info(self) -> str:
        """ Hasta bilgisini açıklayan string döndürür """
        pass

    # class metotlar
    @classmethod
    def get_hospital_name(cls) -> str:
        return cls._hospital_name

    @classmethod
    def from_dict(cls, data: dict):
        """ Dictionary üzerinden hasta oluşturur """
        return cls(
            patient_id=data["patient_id"],
            name=data["name"],
            age=data["age"],
            gender=data["gender"],
            status=data.get("status", "aktif"),
        )

    # static metotlar
    @staticmethod
    def validate_age(age: int) -> bool:
        return isinstance(age, int) and 0 <= age <= 120

    @staticmethod
    def normalize_name(name: str) -> str:
        return name.strip().title()

    def is_active(self) -> bool:
        """ Hastanın aktif bakım sürecinde olup olmadığını döndürür """
        return self._status in ("aktif", "acil", "stabil")

    # yardımcı fonksiyon
    def __lt__(self, other):
        """ Önceliğe göre karşılaştırma """
        return self.get_priority() < other.get_priority()
    
    def detailed_info(self) -> str:
        """
        Hastaya ait temel bilgileri alt alta döndürür.
        """
        return (
            f"Hasta ID      : {self.patient_id}\n"
            f"İsim          : {self.name}\n"
            f"Yaş           : {self.age}\n"
            f"Cinsiyet      : {self.gender}\n"
            f"Durum         : {self.status}"
        )
    
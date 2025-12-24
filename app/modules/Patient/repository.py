# app/modules/patient/repository.py

from typing import List, Optional
from .base import PatientBase
from .inpatient import Inpatient

class PatientRepository:
    """
    Hasta verilerinin in-memory olarak yönetildiği repository sınıfı
    """

    def __init__(self):
        self._patients: List[PatientBase] = []
        self._next_id: int = 2501 
        self._all_rooms = [
            101,102,103,104,
            201,202,203,204,
            301,302,303,304,
            401,402,403,404
        ]
        
    # hasta id oluşturma
    def generate_id(self) -> int:
        pid = self._next_id
        self._next_id += 1
        return pid

    def add(self, patient: PatientBase):
        """ 
        Yeni hasta ekler.
        ID yoksa otomatik ID atar. 
        """
        if patient.patient_id is None:
            patient._patient_id = self.generate_id()

        if self.get_by_id(patient.patient_id) is not None:
            raise ValueError(
                f"Aynı ID'ye sahip hasta zaten mevcut: {patient.patient_id}"
            )

        self._patients.append(patient)

    def remove(self, patient_id: int):
        """ 
        ID'ye göre hasta siler. 
        """
        patient = self.get_by_id(patient_id)
        if patient is None:
            raise ValueError(f"Silinecek hasta bulunamadı: {patient_id}")
        self._patients.remove(patient)

    def get_by_id(self, patient_id: int) -> Optional[PatientBase]:
        """ 
        ID'ye göre hasta döndürür. 
        """
        for patient in self._patients:
            if patient.patient_id == patient_id:
                return patient
        return None

    def list_all(self) -> List[PatientBase]:
        """ 
        Tüm hastaları listeler. 
        """
        return list(self._patients)

    def filter_by_status(self, status: str) -> List[PatientBase]:
        """ 
        Duruma göre hasta filtreler. 
        """
        return [p for p in self._patients if p.status == status]

    def filter_by_type(self, patient_type: str) -> List[PatientBase]:
        """ 
        Hasta tipine göre filtreleme 
        (Inpatient, Outpatient, EmergencyPatient) 
        """
        return [
            p for p in self._patients
            if p.__class__.__name__.lower() == patient_type.lower()
        ]

    def count(self) -> int:
        """ 
        Toplam hasta sayısını döndürür. 
        """
        return len(self._patients)
    
    def release_room_if_inpatient(self, patient: PatientBase):
        """ 
        Taburcu olan hasta Inpatient ise odasını boşaltır 
        """
        if isinstance(patient, Inpatient):
            patient.clear_room()
    
    def replace_patient(self, old_patient, new_patient):
        """ 
        Bir hasta kaydını başka bir hasta nesnesiyle değiştirir  
        """
        if old_patient not in self._patients:
            raise ValueError("Değiştirilecek hasta bulunamadı")

        self._patients.remove(old_patient)
        self._patients.append(new_patient)
        
    def get_available_room(self) -> int:
        used_rooms = {
            p.room_number for p in self._patients
            if isinstance(p, Inpatient) and p.room_number is not None
        }

        for room in self._all_rooms:
            if room not in used_rooms:
                return room

        raise ValueError("Boş oda bulunamadı")
    
    def list_rooms(self):
        """ 
        Oda numaralarına göre yatan hastaları döndürür 
        """
        rooms = {}

        for patient in self._patients:
            if isinstance(patient, Inpatient) and patient.room_number is not None:
                rooms[patient.room_number] = patient

        return rooms
    
    def list_patients_by_priority(self, only_active: bool = False):
        """
        Hastaları öncelik değerine göre sıralar.
        Emergency > Inpatient > Outpatient gibi çalışır.
        """
        patients = self._patients

        if only_active:
            patients = [p for p in patients if p.is_active()]

        return sorted(patients, key=lambda p: p.get_priority(), reverse=True)


    def list_active_patients(self):
        """ 
        Taburcu edilmemiş (aktif) hastaları döndürür 
        """
        return [p for p in self._patients if p.is_active()]
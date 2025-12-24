from .repository import PatientRepository
from .base import PatientBase
from .inpatient import Inpatient
from .emergency_patient import EmergencyPatient


class PatientService:
    """
    Hasta işlemlerine ait iş kurallarını yöneten servis katmanı
    """

    def __init__(self, repository: PatientRepository):
        self._repository = repository

   
    def register_patient(self, patient: PatientBase):
        """ 
        Yeni hasta kaydı oluşturur
        Inpatient ise oda otomatik atanır 
        """
        if isinstance(patient, Inpatient) and patient.room_number is None:
            room = self._repository.get_available_room()
            patient.room_number = room

        self._repository.add(patient)
        return patient


    def discharge_patient(self, patient_id: int):
        """ 
        Hastayı taburcu eder 
        """
        patient = self._repository.get_by_id(patient_id)
        if not patient:
            raise ValueError("Hasta bulunamadı")

        patient.update_status("taburcu")

   
    def update_patient_status(self, patient_id: int, new_status: str):
        """ 
        Belirtilen ID’ye sahip hastanın durumunu günceller. 
        """
        patient = self._repository.get_by_id(patient_id)
        if not patient:
            raise ValueError("Hasta bulunamadı")

        patient.update_status(new_status)

    
    def get_patient(self, patient_id: int) -> PatientBase:
        
        patient = self._repository.get_by_id(patient_id)
        if not patient:
            raise ValueError("Hasta bulunamadı")
        return patient

    def list_patients(self):
        """ 
        Sistemde kayıtlı tüm hastaları listeler. 
        """
        return self._repository.list_all()


    def list_patients_by_type(self, patient_type: str):
        """ 
        Hasta tipine göre filtreleme yapar.
        (Inpatient, Outpatient, EmergencyPatient)
        """
        return self._repository.filter_by_type(patient_type)

    def total_patient_count(self) -> int:
        """ 
        Sistemdeki toplam hasta sayısını döndürür. 
        """
        return self._repository.count()

    
    def list_active_patients(self):
        """ 
        Taburcu edilmemiş hastaları listeler. 
        """
        return [
            p for p in self._repository.list_all()
            if p.status != "taburcu"
        ]


    def list_emergency_patients(self):
        """ 
        Taburcu edilmemiş acil hastaları listeler. 
        """
        return [
            p for p in self._repository.list_all()
            if isinstance(p, EmergencyPatient) and p.status != "taburcu"
        ]


    def admit_emergency_patient(self, patient_id: int):
        """ 
        Emergency hastayı yatışa alır (Inpatient'a dönüştürür)  
        """
        patient = self._repository.get_by_id(patient_id)

        if not patient or not isinstance(patient, EmergencyPatient):
            raise ValueError("Acil hasta bulunamadı")

        room = self._repository.get_available_room()
        inpatient = Inpatient.from_emergency(patient, room)

        self._repository.replace_patient(patient, inpatient)
        return inpatient
    
    def list_room_occupancy(self):
        """ 
        Odalarda hangi hastalar var bilgisini döndürür 
        """
        return self._repository.list_rooms()
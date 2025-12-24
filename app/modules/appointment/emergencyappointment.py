from datetime import datetime
from .base import AppointmentBase


class EmergencyAppointment(AppointmentBase):

    # Sistemdeki toplam ambulans sayısı
    TOTAL_AMBULANCES = 5

    def __init__(
        self,
        appointment_id: int,
        patient_id: int,
        doctor_name: str,
        date_time: datetime
    ):
        super().__init__(
            appointment_id=appointment_id,
            patient_id=patient_id,
            doctor_name=doctor_name,
            date_time=date_time
        )

        self.injured_count = 0
        self.incident_address = ""
        self.critical_level = 0
        self.emergency_note = ""
        self.requested_ambulances = 0
        self.dispatched_ambulances = 0
        self.remaining_ambulances = self.TOTAL_AMBULANCES
        self.event_created_at = datetime.now()

        # Yaralı + kritiklik bilgisi birlikte tutulur
        self.casualty_info = {}

    # Acil randevu detaylarını döndürür
    def get_details(self) -> str:
        return (
            f"ACİL OLAY RAPORU\n"
            f"Olay No            : {self._appointment_id}\n"
            f"Oluşturulma        : {self.event_created_at.strftime('%d.%m.%Y %H:%M')}\n"
            f"Olay Adresi        : {self.incident_address}\n"
            f"Yaralı Sayısı      : {self.injured_count}\n"
            f"Kritiklik Seviyesi : {self.critical_level}\n"
            f"Acil Not           : {self.emergency_note if self.emergency_note else 'Yok'}\n"
            f"Gönderilen Ambulans: {self.dispatched_ambulances}\n"
            f"Kalan Ambulans     : {self.remaining_ambulances}\n"
            f"Durum              : {self._status}"
        )

    # Acil randevu için kısa özet bilgi
    def get_summary(self) -> str:
        return (
            f"ACİL | Olay No {self._appointment_id} | "
            f"Kritiklik: {self.critical_level} | "
            f"Yaralı: {self.injured_count}"
        )

    # Yaralı sayısını belirler
    def set_injured_count(self, count: int):
        if count <= 0:
            raise ValueError("Yaralı sayısı pozitif olmalıdır")
        self.injured_count = count
        self._update_casualty_info()

    # Olay adresini belirler
    def set_incident_address(self, address: str):
        if not address.strip():
            raise ValueError("Adres boş olamaz")
        self.incident_address = address

    # Genel kritiklik seviyesini belirler (1–5)
    def set_critical_level(self, level: int):
        if level < 1 or level > 5:
            raise ValueError("Kritiklik seviyesi 1 ile 5 arasında olmalıdır")
        self.critical_level = level
        self._update_casualty_info()

    # Opsiyonel acil durum notu ekler
    def set_emergency_note(self, note: str):
        if note:
            self.emergency_note = note

    # Olay için istenen ambulans sayısını alır
    def request_ambulances(self, count: int):
        if count <= 0:
            raise ValueError("Ambulans sayısı pozitif olmalıdır")
        self.requested_ambulances = count

    # Mevcut ambulanslara göre sevk işlemi yapar
    def dispatch_ambulances(self) -> bool:
        if self.requested_ambulances <= self.remaining_ambulances:
            self.dispatched_ambulances = self.requested_ambulances
            self.remaining_ambulances -= self.dispatched_ambulances
            return True
        return False

    # Mevcut ambulans bilgisini döndürür
    def get_remaining_ambulances(self) -> int:
        return self.remaining_ambulances

    # Yaralı ve kritiklik bilgilerini birlikte günceller
    def _update_casualty_info(self):
        self.casualty_info = {
            "injured_count": self.injured_count,
            "critical_level": self.critical_level
        }

    # Acil durum kritik mi
    def is_critical_event(self) -> bool:
        return self.critical_level >= 4

    # Olay için yeterli ambulans var mı
    def has_sufficient_ambulance(self) -> bool:
        return self.requested_ambulances <= self.remaining_ambulances

    # Başka modüller için sade olay verisi
    def get_event_data(self) -> dict:
        return self.casualty_info

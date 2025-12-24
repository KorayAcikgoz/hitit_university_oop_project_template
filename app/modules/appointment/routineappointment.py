from datetime import datetime, timedelta
from typing import Optional
from .base import AppointmentBase
import random


class RoutineAppointment(AppointmentBase):

    def __init__(
        self,
        appointment_id: int,
        patient_id: int,
        doctor_name: str,
        date_time: datetime,
        room_number: int,
        duration_minutes: int = 30,
        triage_area: Optional[str] = None
    ):
        super().__init__(
            appointment_id=appointment_id,
            patient_id=patient_id,
            doctor_name=doctor_name,
            date_time=date_time
        )

        if not self._is_valid_room(room_number):
            raise ValueError("Oda numarası pozitif bir sayı olmalıdır")

        if not self._is_valid_duration(duration_minutes):
            raise ValueError("Randevu süresi 10–120 dakika arasında olmalıdır")

        self._room_number = room_number
        self._duration_minutes = duration_minutes
        self._triage_area = triage_area
        self._notes: Optional[str] = None
        self._queue_number = random.randint(0, 50)


    # Randevunun detaylı bilgisini döndürür
    def get_details(self) -> str:
        return (
            f"RUTİN RANDEVU\n"
            f"Randevu ID : {self.get_appointment_id()}\n"
            f"Doktor     : {self.get_doctor_name()}\n"
            f"Oda        : {self._room_number}\n"
            f"Tarih      : {self.get_date_time().strftime('%d.%m.%Y %H:%M')}\n"
            f"Sıra No    : {self.get_queue_number()}\n"
            f"Süre       : {self._duration_minutes} dk\n"
            f"Alan       : {self.get_triage_area()}\n"
            f"Durum      : {self.get_status()}"
        )

    # Randevunun kısa özet bilgisini döndürür
    def get_summary(self) -> str:
        return (
            f"[RUTİN] {self.get_date_time().strftime('%d.%m.%Y %H:%M')} | "
            f"Dr. {self.get_doctor_name()} | Oda {self._room_number}"
        )

    # Triyaj alanını döndürür (Patient modülünden gelen bilgi)
    def get_triage_area(self) -> str:
        return self._triage_area if self._triage_area else "Belirtilmedi"

    # Randevuya açıklama notu ekler
    def add_note(self, note: str):
        if not note.strip():
            raise ValueError("Not boş olamaz")
        self._notes = note

    # Randevu notunu döndürür
    def get_note(self) -> str:
        return self._notes if self._notes else "Not yok"

    # Randevu süresini günceller
    def update_duration(self, new_duration: int):
        if not self._is_valid_duration(new_duration):
            raise ValueError("Geçersiz süre")
        self._duration_minutes = new_duration

    # Randevunun bitiş saatini hesaplar
    def get_end_time(self) -> datetime:
        return self.get_date_time() + timedelta(minutes=self._duration_minutes)

    # Randevu bugün mü kontrol eder
    def is_today(self) -> bool:
        return self.get_date_time().date() == datetime.now().date()

    # Randevu geçmişte mi kontrol eder
    def is_past(self) -> bool:
        return self.get_date_time() < datetime.now()

    # Oda numarasının geçerliliğini kontrol eder
    @staticmethod
    def _is_valid_room(room_number: int) -> bool:
        return isinstance(room_number, int) and room_number > 0

    # Randevu süresinin geçerliliğini kontrol eder
    @staticmethod
    def _is_valid_duration(duration: int) -> bool:
        return isinstance(duration, int) and 10 <= duration <= 120
    
    # random sıra numarası verir
    def get_queue_number(self) -> int:
        return self._queue_number


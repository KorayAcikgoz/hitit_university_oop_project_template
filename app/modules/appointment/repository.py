from datetime import date
from typing import List, Optional
from .base import AppointmentBase


class AppointmentRepository:

    def __init__(self):
        self._appointments: List[AppointmentBase] = []

    # Randevu kaydeder
    def save(self, appointment: AppointmentBase) -> None:
        if self.find_by_id(appointment.get_appointment_id()):
            raise ValueError("Bu ID'ye sahip bir randevu zaten var.")
        self._appointments.append(appointment)

    # Randevu ID geçerli mi
    @staticmethod
    def is_valid_id(appointment_id: int) -> bool:
        return isinstance(appointment_id, int) and appointment_id > 0

    # ID'ye göre randevu bulur
    def find_by_id(self, appointment_id: int) -> Optional[AppointmentBase]:
        for appointment in self._appointments:
            if appointment.get_appointment_id() == appointment_id:
                return appointment
        return None

    # Tarihe göre randevuları filtreler
    def filter_by_date(self, target_date: date) -> List[AppointmentBase]:
        return [
            appointment
            for appointment in self._appointments
            if appointment.get_date_time().date() == target_date
        ]

    # Doktora göre randevuları filtreler
    def filter_by_doctor(self, doctor_name: str) -> List[AppointmentBase]:
        return [
            appointment
            for appointment in self._appointments
            if appointment.get_doctor_name() == doctor_name
        ]

    # Aynı doktor için tarih-saat çakışması var mı
    def has_time_conflict(self, new_appointment: AppointmentBase) -> bool:
        for appointment in self._appointments:
            if (
                appointment.get_doctor_name() == new_appointment.get_doctor_name()
                and appointment.get_date_time() == new_appointment.get_date_time()
                and not appointment.is_cancelled()
            ):
                return True
        return False

    # Randevu siler
    def delete(self, appointment_id: int) -> bool:
        appointment = self.find_by_id(appointment_id)
        if appointment:
            self._appointments.remove(appointment)
            return True
        return False

    # Tüm randevuları döndürür
    def list_all(self) -> List[AppointmentBase]:
        return list(self._appointments)

    # Toplam randevu sayısı
    def count(self) -> int:
        return len(self._appointments)

    # Randevu günceller
    def update(self, appointment: AppointmentBase) -> None:
        existing = self.find_by_id(appointment.get_appointment_id())
        if not existing:
            raise ValueError("Güncellenecek randevu bulunamadı.")

        index = self._appointments.index(existing)
        self._appointments[index] = appointment

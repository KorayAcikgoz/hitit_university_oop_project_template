from datetime import datetime, date
from .base import AppointmentBase
from .repository import AppointmentRepository


class AppointmentService:

    def __init__(self, repository: AppointmentRepository):
        self.repository = repository

    # Randevu oluşturma
    def create_appointment(self, appointment: AppointmentBase):

        if not AppointmentRepository.is_valid_id(
            appointment.get_appointment_id()
        ):
            raise ValueError("Geçersiz randevu ID")

        if self.repository.has_time_conflict(appointment):
            raise ValueError("Bu doktora bu saatte başka bir randevu var")

        self.repository.save(appointment)
        return appointment

    # Randevu iptal etme
    def cancel_appointment(self, appointment_id: int):

        appointment = self.repository.find_by_id(appointment_id)
        if not appointment:
            raise ValueError("Randevu bulunamadı")

        appointment.cancel()
        self.repository.update(appointment)
        return appointment

    # Randevu erteleme
    def reschedule_appointment(self, appointment_id: int, new_datetime: datetime):

        appointment = self.repository.find_by_id(appointment_id)
        if not appointment:
            raise ValueError("Randevu bulunamadı")

        if not AppointmentBase.validate_datetime(new_datetime):
            raise ValueError("Geçersiz tarih formatı")

        appointment.reschedule(new_datetime)
        self.repository.update(appointment)
        return appointment

    # Doktora göre randevu listeleme
    def list_by_doctor(self, doctor_name: str):
        return self.repository.filter_by_doctor(doctor_name)

    # ID'ye göre randevu getirme
    def get_by_id(self, appointment_id: int):
        return self.repository.find_by_id(appointment_id)

    # Tarihe göre randevuları listeleme
    def list_by_date(self, target_date: date):
        return self.repository.filter_by_date(target_date)

    # Tüm randevuları listeleme
    def list_all(self):
        return self.repository.list_all()

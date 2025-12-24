from datetime import datetime, timedelta, time
from .base import AppointmentBase


class OnlineAppointment(AppointmentBase):

    # Poliklinikler ve doktorlar
    POLICLINICS = {
        "Dahiliye": ["Dr. Ahmet", "Dr. Ayşe"],
        "Kardiyoloji": ["Dr. Mehmet", "Dr. Elif"],
        "Dermatoloji": ["Dr. Can", "Dr. Zeynep"]
    }

    # Online randevular 1 saat sürer
    APPOINTMENT_DURATION = 60

    def __init__(
        self,
        appointment_id: int,
        patient_id: int,
        policlinic: str,
        doctor_name: str,
        date_time: datetime
    ):
        super().__init__(
            appointment_id=appointment_id,
            patient_id=patient_id,
            doctor_name=doctor_name,
            date_time=date_time
        )

        self.policlinic = policlinic
        self.end_time = self._date_time + timedelta(minutes=self.APPOINTMENT_DURATION)

    # Randevuya ait detaylı bilgileri döndürür
    def get_details(self) -> str:
        return (
            f"ONLINE RANDEVU\n"
            f"Randevu ID : {self._appointment_id}\n"
            f"Hasta ID  : {self._patient_id}\n"
            f"Poliklinik: {self.policlinic}\n"
            f"Doktor    : {self._doctor_name}\n"
            f"Tarih     : {self._date_time.strftime('%d.%m.%Y')}\n"
            f"Saat      : {self._date_time.strftime('%H:%M')} - "
            f"{self.end_time.strftime('%H:%M')}\n"
            f"Durum     : {self._status}"
        )

    # Randevuya ait kısa özet bilgi
    def get_summary(self) -> str:
        return (
            f"Online | {self.policlinic} | "
            f"Dr. {self._doctor_name} | "
            f"{self._date_time.strftime('%d.%m.%Y %H:%M')}"
        )

    # Mevcut poliklinikleri döndürür
    @classmethod
    def get_policlinics(cls):
        return list(cls.POLICLINICS.keys())

    # Seçilen polikliniğe ait doktorları döndürür
    @classmethod
    def get_doctors_by_policlinic(cls, policlinic: str):
        if policlinic not in cls.POLICLINICS:
            raise ValueError("Geçersiz poliklinik")
        return cls.POLICLINICS[policlinic]

    # Bugünden itibaren 7 günlük uygun tarihleri döndürür
    @staticmethod
    def get_available_dates():
        today = datetime.now().date()
        return [today + timedelta(days=i) for i in range(1, 8)]

    # 10:00–17:00 arası 1 saatlik zaman dilimleri
    @staticmethod
    def get_daily_time_slots():
        return [time(hour=h, minute=0) for h in range(10, 17)]

    # Tarih ve saatten datetime oluşturur
    @staticmethod
    def build_datetime(selected_date, selected_time):
        return datetime.combine(selected_date, selected_time)

    # Doktor için saat çakışması kontrolü
    @staticmethod
    def has_time_conflict(
        doctor_name: str,
        date_time: datetime,
        existing_appointments: list
    ) -> bool:
        for appt in existing_appointments:
            if (
                isinstance(appt, OnlineAppointment)
                and appt._doctor_name == doctor_name
                and appt._date_time == date_time
            ):
                return True
        return False

    # Saat aralığı kontrolü
    @staticmethod
    def is_valid_time_slot(date_time: datetime) -> bool:
        return time(10, 0) <= date_time.time() <= time(16, 0)

    # Tarih aralığı kontrolü (bugün + 7 gün)
    @staticmethod
    def is_valid_date(date_time: datetime) -> bool:
        today = datetime.now().date()
        return today < date_time.date() <= today + timedelta(days=7)

    # Hastanın aynı gün başka online randevusu var mı
    @staticmethod
    def has_patient_daily_conflict(
        patient_id: int,
        date_time: datetime,
        existing_appointments: list
    ) -> bool:
        for appt in existing_appointments:
            if (
                isinstance(appt, OnlineAppointment)
                and appt._patient_id == patient_id
                and appt._date_time.date() == date_time.date()
            ):
                return True
        return False

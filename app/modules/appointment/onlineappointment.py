# app/modules/appointment/onlineappointment.py

from datetime import datetime, timedelta
from .base import AppointmentBase


class OnlineAppointment(AppointmentBase):

    PLATFORM_FEES = {
        "zoom": 50,
        "teams": 40,
        "google_meet": 30
    }

    BASE_FEE = 200

    def __init__(
        self,
        appointment_id: int,
        patient_id: int,
        doctor_name: str,
        date_time: datetime,
        meeting_link: str,
        platform: str,
        estimated_duration: int = 20,
        recording_enabled: bool = False
    ):
        super().__init__(appointment_id, patient_id, doctor_name, date_time)

        self.meeting_link = meeting_link
        self.platform = platform.lower()
        self.estimated_duration = estimated_duration
        self.recording_enabled = recording_enabled

        self.connection_status = "not_started"
        self.session_started_at = None
        self.session_ended_at = None

    def calculate_fee(self) -> int:
        fee = self.BASE_FEE

        platform_fee = self.PLATFORM_FEES.get(self.platform, 20)
        fee += platform_fee

        if self.recording_enabled:
            fee += 50

        if self.estimated_duration > 30:
            fee += 100

        return fee

    def get_details(self) -> str:
        return (
            f"Online Randevu | Dr. {self.doctor_name} | "
            f"Platform: {self.platform} | "
            f"Süre: {self.estimated_duration} dk | "
            f"Kayıt: {'Açık' if self.recording_enabled else 'Kapalı'}"
        )

    # Online görüşmeyi başlatır
    def start_session(self):

        if self.connection_status != "not_started":
            raise RuntimeError("Oturum zaten başlatılmış veya tamamlanmış.")

        self.connection_status = "in_progress"
        self.session_started_at = datetime.now()

    # Online görüşmeyi sonlandırır
    def end_session(self):

        if self.connection_status != "in_progress":
            raise RuntimeError("Başlatılmamış bir oturum sonlandırılamaz.")

        self.connection_status = "completed"
        self.session_ended_at = datetime.now()

    # görüşme süresini dakika cinsinden göster
    def actual_duration(self) -> int:

        if not self.session_started_at or not self.session_ended_at:
            return 0

        delta = self.session_ended_at - self.session_started_at
        return int(delta.total_seconds() // 60)

    # Online randevuyu ileri bir tarihe erteler
    def reschedule_online(self, new_datetime: datetime):

        if not self.validate_datetime(new_datetime):
            raise ValueError("Geçersiz tarih formatı.")

        self.date_time = new_datetime
        self.connection_status = "not_started"
        self.session_started_at = None
        self.session_ended_at = None

    # Platform destekleniyor mu?
    def _is_platform_supported(self) -> bool:

        return self.platform in self.PLATFORM_FEES

    # Desteklenen online platformları göster
    @classmethod
    def supported_platforms(cls):

        return list(cls.PLATFORM_FEES.keys())

    # Online randevular için varsayılan süre
    @classmethod
    def default_duration(cls) -> int:

        return 20

    # Meeting link geçerli mi kontrolü
    @staticmethod
    def is_valid_meeting_link(link: str) -> bool:

        return isinstance(link, str) and link.startswith("http")

    # Süre geçerli mi?
    @staticmethod
    def is_valid_duration(minutes: int) -> bool:

        return isinstance(minutes, int) and 5 <= minutes <= 120

    # Kayıt desteği olan platformları kontrol eder
    @staticmethod
    def can_be_recorded(platform: str) -> bool:

        return platform.lower() in ["zoom", "teams"]

    # Kayıt özelliğini aktif eder
    def enable_recording(self):

        if not self.can_be_recorded(self.platform):
            raise ValueError("Bu platform kayıt desteklemiyor.")
        self.recording_enabled = True

    # Kayıt özelliğini kapatır
    def disable_recording(self):

        self.recording_enabled = False

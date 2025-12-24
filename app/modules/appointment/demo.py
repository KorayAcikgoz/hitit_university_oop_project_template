from datetime import datetime, timedelta
from .repository import AppointmentRepository
from .implementations import AppointmentService
from .routineappointment import RoutineAppointment
from .emergencyappointment import EmergencyAppointment
from .onlineappointment import OnlineAppointment


# Ana menüyü ekrana basar
def print_menu():
    print("\n" + "=" * 50)
    print("   HASTANE RANDEVU SİSTEMİ   ")
    print("=" * 50)
    print("1. Yeni Randevu Oluştur")
    print("2. Randevuları Listele")
    print("3. Randevu Ertele")
    print("4. Randevu İptal Et")
    print("5. Çıkış")
    print("=" * 50)


# Listeleme alt menüsünü gösterir
def print_list_menu():
    print("\n--- RANDEVU LİSTELEME ---")
    print("1. Doktora Göre Listele")
    print("2. Acil Randevuyu Listele (ID'ye Göre)")
    print("3. Tarihe Göre Listele")
    print("4. Tüm Randevuları Listele")
    print("5. Geri Dön")


# Yeni randevu oluşturma işlemini yönetir
def create_appointment(service: AppointmentService):
    print("\nRandevu Türü:")
    print("1. Rutin")
    print("2. Acil (112)")
    print("3. Online")

    choice = input("Seçim: ")

    try:
        appointment_id = int(input("Randevu Numarası: "))
        now = datetime.now()

        # Rutin randevu oluşturur
        if choice == "1":
            patient_id = int(input("Hasta ID: "))
            doctor_name = input("Doktor Adı: ")
            room = int(input("Oda No: "))
            duration = int(input("Süre (dk): "))

            appointment = RoutineAppointment(
                appointment_id=appointment_id,
                patient_id=patient_id,
                doctor_name=doctor_name,
                date_time=now,
                room_number=room,
                duration_minutes=duration
            )

        # Acil (112) randevu oluşturur
        elif choice == "2":
            appointment = EmergencyAppointment(
                appointment_id=appointment_id,
                patient_id=0,
                doctor_name="",
                date_time=now
            )

            appointment.set_injured_count(int(input("Yaralı Sayısı: ")))
            appointment.set_incident_address(input("Olay Adresi: "))
            appointment.set_critical_level(int(input("Kritiklik Seviyesi (1-5): ")))

            note = input("Acil Durum Notu (opsiyonel): ")
            if note.strip():
                appointment.set_emergency_note(note)

            while True:
                requested = int(input("Gönderilecek Ambulans Sayısı: "))
                appointment.request_ambulances(requested)

                if appointment.dispatch_ambulances():
                    break
                else:
                    print(
                        f"❌ Yetersiz ambulans. "
                        f"Mevcut: {appointment.get_remaining_ambulances()}"
                    )

        # Online randevu oluşturur
        elif choice == "3":
            patient_id = int(input("Hasta ID: "))

            policlinics = OnlineAppointment.POLICLINICS
            names = list(policlinics.keys())

            print("\nPoliklinikler:")
            for i, name in enumerate(names, 1):
                print(f"{i}. {name}")

            pol_index = int(input("Seçim: ")) - 1
            policlinic = names[pol_index]

            doctors = policlinics[policlinic]
            print("\nDoktorlar:")
            for i, d in enumerate(doctors, 1):
                print(f"{i}. {d}")

            doctor = doctors[int(input("Seçim: ")) - 1]

            today = datetime.now().date()
            dates = [today + timedelta(days=i) for i in range(1, 8)]

            print("\nTarihler:")
            for i, d in enumerate(dates, 1):
                print(f"{i}. {d}")

            selected_date = dates[int(input("Seçim: ")) - 1]

            print("\nSaatler:")
            for h in range(10, 17):
                print(f"{h}:00")

            hour = int(input("Saat: "))
            selected_datetime = datetime(
                selected_date.year,
                selected_date.month,
                selected_date.day,
                hour,
                0
            )

            all_appointments = service.list_all()

            for appt in all_appointments:
                if (
                    isinstance(appt, OnlineAppointment)
                    and appt.get_doctor_name() == doctor
                    and appt.get_date_time() == selected_datetime
                ):
                    print("❌ Doktor bu saatte dolu.")
                    return

            if OnlineAppointment.has_patient_daily_conflict(
                patient_id, selected_datetime, all_appointments
            ):
                print("❌ Hasta aynı gün ikinci online randevu alamaz.")
                return

            appointment = OnlineAppointment(
                appointment_id=appointment_id,
                patient_id=patient_id,
                doctor_name=doctor,
                date_time=selected_datetime,
                policlinic=policlinic
            )

        else:
            print("❌ Geçersiz seçim.")
            return

        service.create_appointment(appointment)
        print("✅ Randevu başarıyla oluşturuldu.")

    except Exception as e:
        print(f"❌ Hata: {e}")


# Doktora göre randevuları listeler
def list_by_doctor(service: AppointmentService):
    doctor = input("Doktor Adı: ")
    appointments = service.list_by_doctor(doctor)

    if not appointments:
        print("❌ Randevu bulunamadı.")
        return

    for appt in appointments:
        if not isinstance(appt, EmergencyAppointment):
            print(appt.get_details())


# ID’ye göre acil randevu gösterir
def list_emergency_by_id(service: AppointmentService):
    appointment_id = int(input("Acil Randevu ID: "))
    appt = service.get_by_id(appointment_id)

    if not appt or not isinstance(appt, EmergencyAppointment):
        print("❌ Acil randevu bulunamadı.")
        return

    print(appt.get_details())


# Tarihe göre randevuları listeler
def list_by_date(service: AppointmentService):
    try:
        date_str = input("Tarih (YYYY-MM-DD): ")
        target = datetime.strptime(date_str, "%Y-%m-%d").date()
        appointments = service.list_by_date(target)

        if not appointments:
            print("❌ Bu tarihte randevu yok.")
            return

        for appt in appointments:
            print(appt.get_details())

    except ValueError:
        print("❌ Tarih formatı hatalı.")


# Tüm randevuları listeler
def list_all_appointments(service: AppointmentService):
    appointments = service.list_all()

    if not appointments:
        print("❌ Kayıtlı randevu yok.")
        return

    for appt in appointments:
        print(appt.get_details())


# Randevu tarihini değiştirir
def reschedule_appointment(service: AppointmentService):
    appointment_id = int(input("Randevu ID: "))
    appt = service.get_by_id(appointment_id)

    if not appt:
        print("❌ Geçersiz randevu ID.")
        return

    if isinstance(appt, EmergencyAppointment):
        print("❌ Acil randevular ertelenemez.")
        return

    try:
        new_date = input("Yeni tarih (YYYY-MM-DD HH:MM): ")
        new_dt = datetime.strptime(new_date, "%Y-%m-%d %H:%M")
        service.reschedule_appointment(appointment_id, new_dt)
        print("✅ Randevu ertelendi.")
    except ValueError:
        print("❌ Tarih formatı hatalı.")


# Randevuyu iptal eder
def cancel_appointment(service: AppointmentService):
    appointment_id = int(input("Randevu ID: "))
    appt = service.get_by_id(appointment_id)

    if not appt:
        print("❌ Geçersiz randevu ID.")
        return

    if isinstance(appt, EmergencyAppointment):
        print("❌ Acil randevular iptal edilemez.")
        return

    service.cancel_appointment(appointment_id)
    print("✅ Randevu iptal edildi.")


# Demo uygulamasını çalıştırır
def run_demo():
    repository = AppointmentRepository()
    service = AppointmentService(repository)

    while True:
        print_menu()
        choice = input("Seçiminiz: ")

        if choice == "1":
            create_appointment(service)

        elif choice == "2":
            while True:
                print_list_menu()
                sub = input("Seçiminiz: ")

                if sub == "1":
                    list_by_doctor(service)
                elif sub == "2":
                    list_emergency_by_id(service)
                elif sub == "3":
                    list_by_date(service)
                elif sub == "4":
                    list_all_appointments(service)
                elif sub == "5":
                    break
                else:
                    print("Geçersiz seçim.")

        elif choice == "3":
            reschedule_appointment(service)
        elif choice == "4":
            cancel_appointment(service)
        elif choice == "5":
            print("Sistemden çıkılıyor 👋")
            break
        else:
            print("Geçersiz seçim.")


if __name__ == "__main__":
    run_demo()

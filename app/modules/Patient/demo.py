from .repository import PatientRepository
from .service import PatientService
from .inpatient import Inpatient
from .outpatient import Outpatient
from .emergency_patient import EmergencyPatient
from datetime import datetime

def print_patient_list(title, patients):
    print(f"\n{title}")

    if not patients:
        print("Kayıt bulunamadı.")
        return

    for i, p in enumerate(patients, start=1):
        room_info = "-"
        emergency_info = "-"

        if hasattr(p, "room_number") and p.room_number is not None:
            room_info = f"Oda={p.room_number}"

        if hasattr(p, "emergency_level"):
            emergency_info = f"Seviye={p.emergency_level}"
            if hasattr(p, "triage_area") and p.triage_area:
                emergency_info += f" | Alan={p.triage_area}"

        print(
            f"{i}. "
            f"ID={p.patient_id} | "
            f"{p.name} | "
            f"Yaş={p.age} | "
            f"Cinsiyet={p.gender} | "
            f"Durum={p.status} | "
            f"{room_info} | "
            f"{emergency_info}"
        )

def show_header(service):
    now = datetime.now()

    total = service.total_patient_count()
    active = len(service.list_active_patients())
    emergency = len(service.list_emergency_patients())
    inpatients = len(service.list_patients_by_type("Inpatient"))

    print("-" * 42)
    print("        ADA HOSPITAL")
    print("        Information System")
    print("-" * 42)
    print()
    print(f"📅 Tarih : {now.strftime('%d %B %Y')}")
    print(f"⏰ Saat  : {now.strftime('%H:%M')}")
    print()
    print("📊 Sistem Özeti")
    print("-" * 42)
    print(f"• Toplam Hasta     : {total}")
    print(f"• Aktif Hasta      : {active}")
    print(f"• Acil Hasta       : {emergency}")
    print(f"• Yatan Hasta      : {inpatients}")
    print("-" * 42)
    
def main_menu():
    print("\nANA MENÜ")
    print("1 - Hasta Kayıt İşlemleri")
    print("2 - Hasta İşlem Merkezi")
    print("0 - Çıkış")


def add_patient_menu():
    print("\nHASTA KAYIT İŞLEMLERİ")
    print("1 - Yatan Hasta ")
    print("2 - Ayaktan Hasta ")
    print("3 - Acil Hasta ")
    print("0 - Geri")


def filter_menu():
    print("\nHASTA İŞLEM MERKEZİ")
    print("1 - Tüm Hastalar")
    print("2 - Aktif Hastalar")
    print("3 - Acil Hastalar")
    print("4 - Önceliğe Göre Sıralı")
    print("0 - Geri")


def inpatient_menu():
    print("\n1 - Taburcu Et")
    print("2 - Durum Güncelle")
    print("3 - Oda Değiştir")
    print("4 - Bilgileri Gör")
    print("0 - Geri")


def emergency_menu():
    print("\n1 - Acil Seviyesi Yükselt")
    print("2 - Stabil Yap")
    print("3 - Yatışa Al")
    print("4 - Bilgileri Gör")
    print("0 - Geri")


def outpatient_menu():
    print("\n1 - Randevu İptal")
    print("2 - Durum Güncelle")
    print("3 - Bilgileri Gör")
    print("0 - Geri")



# hasta seçimi
def select_patient(patients):
    print_patient_list("Hasta Listesi", patients)

    try:
        idx = int(input("\nHasta seç (numara): ")) - 1
        return patients[idx]
    except:
        print("Geçersiz seçim.")
        return None

# hasta türüne göre işlem
def handle_patient(patient, service: PatientService):
    while True:
        print(f"\nSeçilen Hasta: {patient.name} ({patient.__class__.__name__})")

        if isinstance(patient, Inpatient):
            inpatient_menu()
            c = input("Seçim: ")

            if c == "1":
                service.discharge_patient(patient.patient_id)
                print("Hasta taburcu edildi.")
                break

            elif c == "2":
                status = input("Yeni durum: ")
                patient.update_status(status)

            elif c == "3":
                new_room = service._repository.get_available_room()
                patient.room_number = new_room
                print(f"Oda değiştirildi → {new_room}")

            elif c == "4":
                print(patient.detailed_info())

            elif c == "0":
                break

        elif isinstance(patient, EmergencyPatient):
            emergency_menu()
            c = input("Seçim: ")

            if c == "1":
                patient.escalate()
                print("Acil seviyesi yükseltildi.")

            elif c == "2":
                patient.stabilize()
                print("Hasta stabilize edildi.")

            elif c == "3":
                inpatient = service.admit_emergency_patient(patient.patient_id)
                print("Hasta yatışa alındı:")
                print(patient.detailed_info())
                break

            elif c == "4":
                print(patient.detailed_info())

            elif c == "0":
                break

        else:  # Outpatient
            outpatient_menu()
            c = input("Seçim: ")

            if c == "1":
                patient.update_status("iptal")
                print("Randevu iptal edildi.")

            elif c == "2":
                status = input("Yeni durum: ")
                patient.update_status(status)

            elif c == "3":
                print(patient.detailed_info())

            elif c == "0":
                break


def run_demo():
    repo = PatientRepository()
    service = PatientService(repo)

    while True:
        show_header(service)
        main_menu()
        choice = input("Seçiminiz: ")

        # HASTA EKLE
        if choice == "1":
            while True:
                add_patient_menu()
                sub = input("Seçim: ")

                try:
                    if sub == "1":
                        p = Inpatient(
                            None,
                            input("İsim: "),
                            int(input("Yaş: ")),
                            input("Cinsiyet: ")
                        )
                        patient = service.register_patient(p)
                        print("\nHasta başarıyla eklendi ✔")
                        print("\nHasta Bilgileri")
                        print(patient.detailed_info())

                    elif sub == "2":
                        p = Outpatient(
                            None,
                            input("İsim: "),
                            int(input("Yaş: ")),
                            input("Cinsiyet: "),
                            input("Randevu Tarihi (YYYY-MM-DD): ")
                        )
                        service.register_patient(p)
                        print("\nHasta başarıyla eklendi ✔")
                        print("\nHasta Bilgileri")
                        print(patient.detailed_info())

                    elif sub == "3":
                        p = EmergencyPatient(
                            None,
                            input("İsim: "),
                            int(input("Yaş: ")),
                            input("Cinsiyet: "),
                            int(input("Acil Seviye (1-3): "))
                        )
                        symptoms = input("Semptomlar (virgül ile): ").split(",")
                        p.add_symptoms([s.strip() for s in symptoms])
                        service.register_patient(p)
                        print("\nHasta başarıyla eklendi ✔")
                        print("\nHasta Bilgileri")
                        print(patient.detailed_info())

                    elif sub == "0":
                        break

                except Exception as e:
                    print("Hata:", e)

        # HASTA LİSTELERİ
        elif choice == "2":
            while True:
                filter_menu()
                f = input("Seçim: ")

                if f == "1":
                    patients = service.list_patients()
                elif f == "2":
                    patients = service.list_active_patients()
                elif f == "3":
                    patients = service.list_emergency_patients()
                elif f == "4":
                    patients = repo.list_patients_by_priority(only_active=True)
                elif f == "0":
                    break
                else:
                    continue

                patient = select_patient(patients)
                if patient:
                    handle_patient(patient, service)

        elif choice == "0":
            print("Sistem kapatılıyor...")
            break


if __name__ == "__main__":
    run_demo()
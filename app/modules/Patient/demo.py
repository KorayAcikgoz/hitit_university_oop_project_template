# app/modules/patient/demo.py

from .repository import PatientRepository
from .service import PatientService
from .inpatient import Inpatient
from .outpatient import Outpatient
from .emergency_patient import EmergencyPatient
from datetime import datetime


def show_header():
    now = datetime.now()
    print("\nADA HOSPITAL")
    print(f"Tarih: {now.strftime('%d %B %Y')}  Saat: {now.strftime('%H:%M')}\n")


def main_menu():
    print("1 - Hasta Ekle")
    print("2 - Hasta İşlemleri")
    print("3 - Listeleme / Filtreleme")
    print("0 - Çıkış")


def add_patient_menu():
    print("\nHasta Ekle:")
    print("1 - Yatan Hasta (Inpatient)")
    print("2 - Ayaktan Hasta (Outpatient)")
    print("3 - Acil Hasta (Emergency)")
    print("0 - Geri")


def patient_actions_menu():
    print("\nHasta İşlemleri:")
    print("1 - Hasta Taburcu Et")
    print("2 - Hasta Durumu Güncelle")
    print("3 - Acil Seviyesi Yükselt")
    print("4 - Hasta ID ile Görüntüle")
    print("0 - Geri")


def list_menu():
    print("\nListeleme / Filtreleme:")
    print("1 - Tüm Hastalar")
    print("2 - Duruma Göre Listele")
    print("3 - Tipe Göre Listele")
    print("4 - Toplam Hasta Sayısı")
    print("0 - Geri")


def run_demo():
    repo = PatientRepository()
    service = PatientService(repo)

    while True:
        show_header()
        main_menu()
        choice = input("Seçiminiz: ").strip()

        # HASTA EKLE
        if choice == "1":
            while True:
                add_patient_menu()
                sub = input("Seçim: ").strip()

                try:
                    if sub == "1":
                        p = Inpatient(
                            patient_id=int(input("ID: ")),
                            name=input("İsim: "),
                            age=int(input("Yaş: ")),
                            gender=input("Cinsiyet: "),
                            room_number=int(input("Oda No: "))
                        )
                        service.register_patient(p)
                        print("Inpatient eklendi")

                    elif sub == "2":
                        p = Outpatient(
                            patient_id=int(input("ID: ")),
                            name=input("İsim: "),
                            age=int(input("Yaş: ")),
                            gender=input("Cinsiyet: "),
                            appointment_date=input("Randevu Tarihi (YYYY-MM-DD): ")
                        )
                        service.register_patient(p)
                        print("Outpatient eklendi")

                    elif sub == "3":
                        p = EmergencyPatient(
                            patient_id=int(input("ID: ")),
                            name=input("İsim: "),
                            age=int(input("Yaş: ")),
                            gender=input("Cinsiyet: "),
                            emergency_level=int(input("Acil Seviye (1-3): "))
                        )

                        symptoms = input("Semptomlar (virgülle ayır): ").split(",")
                        p.add_symptoms([s.strip() for s in symptoms])

                        service.register_patient(p)
                        print("EmergencyPatient eklendi")
                        print("Triyaj Alanı:", p.determine_triage_area())

                    elif sub == "0":
                        break
                    else:
                        print("Geçersiz seçim")

                except Exception as e:
                    print("Hata:", e)

        # HASTA İŞLEMLERİ
        elif choice == "2":
            while True:
                patient_actions_menu()
                sub = input("Seçim: ").strip()

                try:
                    if sub == "1":
                        pid = int(input("Hasta ID: "))
                        service.discharge_patient(pid)
                        print("Hasta taburcu edildi")

                    elif sub == "2":
                        pid = int(input("Hasta ID: "))
                        status = input("Yeni Durum: ")
                        service.update_patient_status(pid, status)
                        print("Durum güncellendi")

                    elif sub == "3":
                        pid = int(input("Hasta ID: "))
                        patient = service.get_patient(pid)

                        if isinstance(patient, EmergencyPatient):
                            patient.escalate()
                            print("Acil seviyesi yükseltildi")
                        else:
                            print("Bu işlem sadece acil hastalar için geçerli")

                    elif sub == "4":
                        pid = int(input("Hasta ID: "))
                        print(service.get_patient(pid).describe())

                    elif sub == "0":
                        break
                    else:
                        print("Geçersiz seçim")

                except Exception as e:
                    print("Hata:", e)

        # LİSTELEME
        elif choice == "3":
            while True:
                list_menu()
                sub = input("Seçim: ").strip()

                if sub == "1":
                    for p in service.list_patients():
                        print(p.describe())

                elif sub == "2":
                    status = input("Durum: ")
                    for p in service.list_patients_by_status(status):
                        print(p.describe())

                elif sub == "3":
                    t = input("Tip: ")
                    for p in service.list_patients_by_type(t):
                        print(p.describe())

                elif sub == "4":
                    print("Toplam Hasta:", service.total_patient_count())

                elif sub == "0":
                    break
                else:
                    print("Geçersiz seçim")

        elif choice == "0":
            print("Demo kapatılıyor...")
            break

        else:
            print("Geçersiz seçim!")


if __name__ == "__main__":
    run_demo()
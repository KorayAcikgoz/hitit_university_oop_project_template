# main.py

import time
import os
from datetime import datetime

from app.modules.Patient.demo import run_demo as run_patient_demo
from app.modules.appointment.demo import run_demo as run_appointment_demo


def clear():
    os.system("clear" if os.name == "posix" else "cls")


def slow_print(text, delay=0.02):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()


def line(char="═", length=70):
    print(char * length)


def loading(text, duration=1.3):
    spinner = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f"\r{text} {spinner[i % 4]}", end="", flush=True)
        time.sleep(0.15)
        i += 1
    print("\r" + " " * 80 + "\r", end="")


def show_header():
    clear()
    now = datetime.now().strftime("%d %B %Y  •  %H:%M")

    line()
    slow_print("A D A   H O S P I T A L".center(70), 0.01)
    slow_print("Integrated Hospital Information System".center(70), 0.01)
    print(f"                     {now}")
    line()

# Menü
def main_menu():
    slow_print("\n Select User Role\n", 0.02)
    print("   [1] Patient")
    print("   [2] Doctor / Medical Staff")
    print("   [3] Administrator")
    print("   [0] Exit")
    return input("\n > ").strip()


def patient_menu():
    slow_print("\n Patient Portal", 0.02)
    line("-")
    print("   [1] Appointment System")
    print("   [0] Back")


def staff_menu():
    slow_print("\n Doctor / Staff Portal", 0.02)
    line("-")
    print("   [1] Patient Management")
    print("   [2] Appointment Management")
    print("   [0] Back")


def admin_menu():
    slow_print("\n Administrator Panel", 0.02)
    line("-")
    print("   [1] Patient Management")
    print("   [2] Appointment Management")
    print("   [0] Back")



def main():
    last_refresh = 0

    while True:
        current_time = time.time()

        # Header her 30 saniyede bir güncellensin
        if current_time - last_refresh >= 30:
            show_header()
            last_refresh = current_time

        role = main_menu()

        if role == "0":
            loading("Shutting down system")
            slow_print("\n System closed successfully. Stay healthy.")
            break

        while True:
            show_header()

            if role == "1":  # Patient
                patient_menu()
                choice = input("\n > ").strip()

                if choice == "1":
                    loading("Opening Appointment System")
                    run_appointment_demo()
                elif choice == "0":
                    break

            elif role == "2":  # Doctor / Staff
                staff_menu()
                choice = input("\n > ").strip()

                if choice == "1":
                    loading("Opening Patient Management Module")
                    run_patient_demo()
                elif choice == "2":
                    loading("Opening Appointment Management Module")
                    run_appointment_demo()
                elif choice == "0":
                    break

            elif role == "3":  # Admin
                admin_menu()
                choice = input("\n > ").strip()

                if choice == "1":
                    loading("Opening Patient Management Module")
                    run_patient_demo()
                elif choice == "2":
                    loading("Opening Appointment Management Module")
                    run_appointment_demo()
                elif choice == "0":
                    break

            else:
                slow_print("\n Invalid selection.")
                time.sleep(1)

            input("\n Press ENTER to return to main menu...")


if __name__ == "__main__":
    main()
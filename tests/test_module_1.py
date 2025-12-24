from app.modules.Patient.repository import PatientRepository
from app.modules.Patient.service import PatientService
from app.modules.Patient.outpatient import Outpatient
from app.modules.Patient.inpatient import Inpatient
from app.modules.Patient.emergency_patient import EmergencyPatient


def test_repository_add_and_get_patient():
    repo = PatientRepository()

    patient = Outpatient(
        patient_id=None,
        name="Ali",
        age=30,
        gender="erkek",
        appointment_date="2025-01-01"
    )

    repo.add(patient)

    fetched = repo.get_by_id(patient.patient_id)

    assert fetched is not None
    assert fetched.name == "Ali"


def test_service_register_and_discharge_patient():
    repo = PatientRepository()
    service = PatientService(repo)

    patient = Inpatient(
        patient_id=None,
        name="Ayşe",
        age=45,
        gender="kadın",
        room_number=101
    )

    service.register_patient(patient)
    service.discharge_patient(patient.patient_id)

    assert patient.status == "taburcu"
    assert patient.room_number is None


def test_list_patients_by_type():
    repo = PatientRepository()
    service = PatientService(repo)

    p1 = Outpatient(
        patient_id=None,
        name="Ali",
        age=28,
        gender="erkek",
        appointment_date="2025-01-01"
    )

    p2 = Inpatient(
        patient_id=None,
        name="Ayşe",
        age=50,
        gender="kadın",
        room_number=102
    )

    service.register_patient(p1)
    service.register_patient(p2)

    inpatients = service.list_patients_by_type("Inpatient")

    assert len(inpatients) == 1
    assert inpatients[0].name == "Ayşe"


def test_emergency_patient_triage():
    patient = EmergencyPatient(
        patient_id=None,
        name="Mehmet",
        age=65,
        gender="erkek",
        emergency_level=1
    )

    patient.add_symptoms(["Göğüs ağrısı", "Nefes darlığı"])

    triage_area = patient.determine_triage_area()

    assert triage_area in ["Kırmızı", "Sarı", "Yeşil"]
    assert patient.emergency_level in (1, 2, 3)
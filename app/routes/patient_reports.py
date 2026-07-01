from datetime import datetime

from flask import render_template, request

from app.models.patient_model import Patient
from app.services.patient_service import calculate_age
from app.services import bmi_category

def register_patients_routes(app):
    @app.route("/patients")
    def patients():

        visit_date = request.args.get("visit_date")

        patients = (
            Patient.query
            .order_by(Patient.registration_date.desc())
            .all()
        )

        patient_records = []

        for patient in patients:

            if not patient.vitals:
                continue

            latest_visit = patient.vitals[0]

            if visit_date:
                try:
                    selected_date = datetime.strptime(
                        visit_date,
                        "%Y-%m-%d"
                    ).date()

                    if latest_visit.visit_date != selected_date:
                        continue

                except ValueError:
                    pass

            patient_records.append({

                "patient_id": patient.patient_id,

                "first_name": patient.first_name,

                "last_name": patient.last_name,

                "age": calculate_age(patient.date_of_birth),

                "bmi_status": bmi_category(latest_visit.bmi),

                "visit_date": latest_visit.visit_date

            })

        return render_template(

            "patients.html",

            patient_records=patient_records,

            selected_date=visit_date,

            record_count=len(patient_records)

        )
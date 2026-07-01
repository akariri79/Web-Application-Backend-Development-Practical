from flask import request, jsonify
from datetime import datetime
from app.extensions import db
from app.models import Patient, Vitals, GeneralAssessment, OverweightAssessment
from app.services import calculate_age
from app.services import bmi_category


def api_response(data=None, message="success", success=True, code=200):
    return jsonify({
        "message": message,
        "success": success,
        "code": code,
        "data": data
    }), code


def register_api_routes(app):
    @app.route("/patients/register", methods=["POST"])
    def register_patient():
        data = request.get_json(silent=True)

        if not data.get("unique"):
            return api_response(message="Patient ID is required", success=False, code=400)

        if db.session.get(Patient, data["unique"]):
            return api_response(message="Patient ID already exists", success=False, code=409)

        patient = Patient(
            patient_id=data["unique"],
            first_name=data["firstname"],
            last_name=data["lastname"],
            date_of_birth=datetime.strptime(data["dob"], "%Y-%m-%d").date(),
            gender=data["gender"],
            registration_date=datetime.strptime(data["reg_date"], "%Y-%m-%d").date()
        )
        db.session.add(patient)
        db.session.commit()
        return api_response(data=patient.to_dict(), message="Patient registered", code=201)

    @app.route("/patients/view", methods=["GET"])
    def list_patients():
        patients = Patient.query.order_by(Patient.registration_date.desc()).all()
        return api_response(data=[p.to_dict() for p in patients])

    @app.route("/patients/show/<string:patient_id>", methods=["GET"])
    def show_patient(patient_id):
        patient = db.session.get(Patient, patient_id)
        if not patient:
            return api_response(message="Patient not found", success=False, code=404)
        return api_response(data=[patient.to_dict()])

    @app.route("/vital/add", methods=["POST"])
    def add_vital():
        data = request.get_json()
        vital = Vitals(
            visit_date=datetime.strptime(data["visit_date"], "%Y-%m-%d").date(),
            height_cm=float(data["height"]),
            weight_kg=float(data["weight"]),
            bmi=float(data["bmi"]),
            patient_id=str(data["patient_id"])
        )
        db.session.add(vital)
        db.session.commit()
        return api_response(
            data={"slug": vital.vitals_id, "message": "Vital Added Successfully"},
            code=201
        )

    @app.route("/visits/add", methods=["POST"])
    def add_visit():
        data = request.get_json()
        vitals_id = int(data["vital_id"])
        vitals = db.session.get(Vitals, vitals_id)
        if not vitals:
            return api_response(message="Vitals record not found", success=False, code=404)

        if vitals.bmi > 25:
            assessment = OverweightAssessment(
                vitals_id=vitals_id,
                general_health=data.get("general_health"),
                diet_history=data.get("on_diet"),
                comments=data.get("comments")
            )
            slug = "overweight_assessment_id"
        else:
            assessment = GeneralAssessment(
                vitals_id=vitals_id,
                general_health=data.get("general_health"),
                drug_usage=data.get("on_drugs"),
                comments=data.get("comments")
            )
            slug = "general_assessment_id"

        db.session.add(assessment)
        db.session.commit()
        return api_response(
            data={"slug": getattr(assessment, slug), "message": "Visit Added Successfully"},
            code=201
        )

    @app.route("/visits/view", methods=["POST"])
    def list_visits_by_date():
        data = request.get_json()
        visit_date = datetime.strptime(data["visit_date"], "%Y-%m-%d").date()
        results = []
        for patient in Patient.query.all():
            match = next((v for v in patient.vitals if v.visit_date == visit_date), None)
            if not match:
                continue
            results.append({
                "name": f"{patient.first_name} {patient.last_name}",
                "age": calculate_age(patient.date_of_birth),
                "bmi": match.bmi,
                "status": bmi_category(match.bmi)
            })
        return api_response(data=results)
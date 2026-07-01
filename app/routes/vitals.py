from flask import render_template, redirect, url_for, flash
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.forms.vitals_form import VitalsForm
from app.models.patient_model import Patient
from app.models.vitals_model import Vitals
from app.services import (
    calculate_bmi,
    determine_assessment,
    GENERAL_ASSESSMENT,
    OVERWEIGHT_ASSESSMENT
)
from datetime import date


def register_vitals_routes(app):

    @app.route("/vitals/<string:patient_id>", methods=["GET", "POST"])
    def record_vitals(patient_id):

        # Retrieve the patient
        patient = db.get_or_404(Patient, patient_id)

        today = date.today()

        form = VitalsForm()


        if form.validate_on_submit():

            # Calculate BMI
            bmi = calculate_bmi(
                form.height_cm.data,
                form.weight_kg.data
            )

            # Create Vitals object
            vitals = Vitals(
                patient_id=patient.patient_id,
                visit_date=today,
                height_cm=form.height_cm.data,
                weight_kg=form.weight_kg.data,
                bmi=bmi
            )

            try:
                db.session.add(vitals)
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                app.logger.error(f"Failed to save vitals: {e}")
                flash("Unable to save vitals.", "danger")
                return render_template(
                    "record_vitals.html",
                    form=form,
                    patient=patient
                )

            assessment = determine_assessment(bmi)

            flash("Vitals recorded successfully.", "success")

            if assessment == GENERAL_ASSESSMENT:
                return redirect(
                    url_for(
                        "general_assessment",
                        vitals_id=vitals.vitals_id
                    )
                )
            if assessment == OVERWEIGHT_ASSESSMENT:
                return redirect(
                    url_for(
                        "overweight_assessment",
                        vitals_id=vitals.vitals_id
                )
            )

            flash(
                "Unable to determine assessment type.",
                "danger"
            )

            return redirect(url_for("home"))

        return render_template(
            "record_vitals.html",
            form=form,
            patient=patient,
            today=today
        )



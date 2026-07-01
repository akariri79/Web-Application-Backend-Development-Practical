from datetime import date

from flask import render_template, redirect, url_for, flash
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.forms.patient_form import PatientForm
from app.models.patient_model import Patient


def register_patient_routes(app):

    @app.route("/register", methods=["GET", "POST"])
    def register_patient_form():

        form = PatientForm()

        if form.validate_on_submit():

            # Check if Patient ID already exists
            existing_patient = Patient.query.filter_by(
                patient_id=form.patient_id.data
            ).first()


            if existing_patient:
                flash(
                    "A patient with this Patient ID already exists.",
                    "danger"
                )
                return render_template(
                    "register_patient_form.html",
                    form=form
                )

            # Create Patient object
            patient = Patient(
                patient_id=form.patient_id.data,
                registration_date=date.today(),
                first_name=form.first_name.data,
                # middle_name=form.middle_name.data,
                last_name=form.last_name.data,
                gender=form.gender.data,
                date_of_birth=form.date_of_birth.data
            )

            try:
                db.session.add(patient)
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                app.logger.error(f"Failed to register patient: {e}")
                flash("Unable to register patient.", "danger")
                return render_template(
                    "patient_registration.html",
                    form=form
                )

            flash(
                "Patient registered successfully.",
                "success"
            )

            return redirect(
                url_for(
                    "record_vitals",
                    patient_id=patient.patient_id
                )
            )

        return render_template(
            "patient_registration.html",
            form=form
        )
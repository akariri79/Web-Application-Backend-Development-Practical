from flask import render_template, redirect, url_for, flash
from app.extensions import db
from sqlalchemy.exc import SQLAlchemyError
from app.models.vitals_model import Vitals
from app.models.assessments_model import GeneralAssessment
from app.models.assessments_model import OverweightAssessment
from app.forms.assessment_form import (
    GeneralAssessmentForm,
    OverweightAssessmentForm
)
from datetime import date

today=date.today()

def register_assessment_routes(app):

    @app.route("/assessment/general/<string:vitals_id>", methods=["GET", "POST"])
    def general_assessment(vitals_id):

        vitals = db.session.get(Vitals, vitals_id)

        if vitals is None:
            flash("Vitals record not found.", "danger")
            return redirect(url_for("home"))

        form = GeneralAssessmentForm()

        if form.validate_on_submit():

            assessment = GeneralAssessment(
                vitals_id=vitals.vitals_id,
                general_health=form.general_health.data,
                drug_usage=form.drug_usage.data,
                comments=form.comments.data
            )

            try:
                db.session.add(assessment)
                db.session.commit()

            except SQLAlchemyError as e:
                db.session.rollback()
                app.logger.error(f"Failed to save assessment: {e}")
                flash("Unable to save assessment.","danger")
                return render_template(
                    "general_assessment.html",
                    form=form,
                    vitals=vitals
                )

            flash("General assessment completed successfully.","success")
            return redirect(url_for("patients"))

        return render_template(
            "general_assessment.html",
            form=form,
            vitals=vitals,
            today=today
        )

    @app.route("/assessment/overweight/<int:vitals_id>",methods=["GET", "POST"])
    def overweight_assessment(vitals_id):

        vitals = db.session.get(Vitals, vitals_id)

        if vitals is None:
            flash("Vitals record not found.", "danger")
            return redirect(url_for("home"))

        form = OverweightAssessmentForm()

        if form.validate_on_submit():

            assessment = OverweightAssessment(
                vitals_id=vitals.vitals_id,
                general_health=form.general_health.data,
                diet_history=form.diet_history.data,
                comments=form.comments.data
            )

            try:
                db.session.add(assessment)
                db.session.commit()

            except SQLAlchemyError as e:
                db.session.rollback()
                app.logger.error(f"Failed to save assessment: {e}")
                flash("Unable to save assessment.","danger")
                return render_template(
                    "overweight_assessment.html",
                    form=form,
                    vitals=vitals
                )

            flash("Overweight assessment completed successfully.","success")

            return redirect(url_for("patients"))

        return render_template(
            "overweight_assessment.html",
            form=form,
            vitals=vitals,
            today=today
        )

from app.extensions import db

class Vitals(db.Model):
    __tablename__ = "vitals"
    vitals_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(20), db.ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False)
    visit_date = db.Column(db.Date, nullable=False)
    height_cm = db.Column(db.Float, nullable=False)
    weight_kg = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    patient = db.relationship("Patient", back_populates="vitals")
    general_assessment = db.relationship(
        "GeneralAssessment",
        back_populates="vitals",
        uselist=False,
        cascade="all, delete-orphan"
    )
    overweight_assessment = db.relationship(
        "OverweightAssessment",
        back_populates="vitals",
        uselist=False,
        cascade="all, delete-orphan"
    )
    
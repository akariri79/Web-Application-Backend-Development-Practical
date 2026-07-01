from app.extensions import db


# Create Patient Table
class Patient(db.Model):
    __tablename__ = "patients"
    patient_id = db.Column(db.String(20), primary_key=True)
    registration_date = db.Column(db.Date, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    vitals = db.relationship("Vitals", back_populates="patient",
                             cascade="all, delete-orphan",
                             single_parent=True,
                             order_by="desc(Vitals.visit_date)"
                             )

    # inside class Patient(db.Model):
    def to_dict(self):
        return {
            "id": self.patient_id,
            "firstname": self.first_name,
            "lastname": self.last_name,
            "dob": self.date_of_birth.isoformat(),
            "gender": self.gender,
            "reg_date": self.registration_date.isoformat()
        }
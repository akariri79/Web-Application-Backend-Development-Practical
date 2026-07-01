# Web App & Backend Development Practical

A web application built for the IntelliSOFT Consulting Limited technical assessment. The app registers patients, records their vitals, routes them to the appropriate health assessment form based on their BMI, and displays a filterable patient listing.

---

## Approach

This project implements its **own RESTful backend** rather than consuming the APIs provided in the Postman collection. Both the frontend (Jinja2/HTML) and the REST API endpoints are served from the same Flask application.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Web Framework | Flask |
| ORM | SQLAlchemy (via Flask-SQLAlchemy) |
| Database Migrations | Flask-Migrate (Alembic) |
| Forms | Flask-WTF / WTForms |
| Templating | Jinja2 |
| Database | PostgreSQL (hosted on Railway) |
| Production Server | Waitress |
| Environment Config | python-dotenv |

---

## Project Structure

```
project_root/
├── app/
│   ├── __init__.py         # App factory (create_app)
│   ├── extensions.py       # db and migrate instances
│   ├── forms/              # Flask-WTF form definitions
│   ├── models/             # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── patient.py
│   │   ├── vitals.py
│   │   ├── general_assessment.py
│   │   └── overweight_assessment.py
│   ├── routes/             # Route registration
│   │   ├── __init__.py
│   │   ├── api_routes.py   # REST API endpoints
│   │   └── ...             # Jinja2 page routes
│   ├── services/           # Business logic (BMI, age calculation)
│   ├── static/             # CSS, JS, images
│   └── templates/          # HTML templates
├── .env                    # Environment variables (not committed)
├── .flaskenv               # Flask CLI config (committed)
├── config.py               # App configuration class
├── requirements.txt        # Python dependencies
└── run.py                  # Entry point
```

---

## Database Schema

Four tables, linked by foreign keys:

**patients** — core patient record
- `patient_id` (String, primary key — clinician-supplied, unique)
- `first_name`, `last_name`
- `date_of_birth`, `gender`
- `registration_date`

**vitals** — one or more per patient, one per visit date
- `vitals_id` (Integer, primary key)
- `patient_id` (FK → patients)
- `visit_date`, `height_cm`, `weight_kg`, `bmi`

**general_assessments** — one per vitals record, only when BMI ≤ 25
- `general_assessment_id` (Integer, primary key)
- `vitals_id` (FK → vitals, unique)
- `general_health`, `drug_usage`, `comments`

**overweight_assessments** — one per vitals record, only when BMI > 25
- `overweight_assessment_id` (Integer, primary key)
- `vitals_id` (FK → vitals, unique)
- `general_health`, `diet_history`, `comments`

BMI is auto-calculated server-side: `BMI = weight_kg / (height_cm / 100) ** 2`

---

## Application Pages

| Page | URL | Description |
|---|---|---|
| Patient Registration | `/register` | Captures patient details and saves to the database |
| Vitals Form | `/vitals/<patient_id>` | Records height, weight, and auto-calculates BMI |
| General Assessment | `/general-assessment/<vitals_id>` | Shown when BMI ≤ 25 |
| Overweight Assessment | `/overweight-assessment/<vitals_id>` | Shown when BMI > 25 |
| Patient Listing | `/patients` | Filterable table of all patients with BMI status |

**BMI routing logic:** after saving vitals, the app automatically redirects to the correct assessment form — General if BMI ≤ 25, Overweight if BMI > 25.

**BMI status thresholds:**
- Underweight: BMI < 18.5
- Normal: 18.5 ≤ BMI < 25
- Overweight: BMI ≥ 25

---

## Screenshots

### Patient Registration
![Patient Registration](screenshots/registration.png)

### Vitals Form
![Vitals Form](screenshots/vitals.png)

### General Assessment Form
![General Assessment Form](screenshots/general_assessment.png)

### Overweight Assessment Form
![Overweight Assessment Form](screenshots/overweight_assessment.png)

### Patient Listing
![Patient Listing](screenshots/patient_listing.png)

---

## REST API Endpoints

All endpoints return JSON in the following shape:
```json
{
  "message": "success",
  "success": true,
  "code": 200,
  "data": {}
}
```

### Patients

**Register a patient**
```
POST /patients/register
```
```json
{
  "unique": "12345611qq",
  "firstname": "John",
  "lastname": "Mdoe",
  "dob": "2002-01-01",
  "gender": "Male",
  "reg_date": "2025-10-31"
}
```

**List all patients**
```
GET /patients/view
```
No body required.

**View a single patient**
```
GET /patients/show/<patient_id>
```
`patient_id` is the clinician-supplied unique ID (e.g. `/patients/show/12345611qq`).

### Vitals

**Add vitals**
```
POST /vital/add
```
```json
{
  "visit_date": "2025-10-31",
  "height": "156",
  "weight": "80",
  "bmi": "24.5",
  "patient_id": "12345611qq"
}
```
Returns a `slug` field in the response — this is the `vitals_id` needed for the visit assessment call.

### Visit Assessments

**Add a visit assessment**
```
POST /visits/add
```
The server determines which assessment table to write to based on the BMI value stored against the provided `vital_id` — no form-type flag needed in the request.

For BMI ≤ 25 (General Assessment):
```json
{
  "vital_id": "1",
  "general_health": "Good",
  "on_drugs": "No",
  "comments": "Patient appears healthy"
}
```

For BMI > 25 (Overweight Assessment):
```json
{
  "vital_id": "1",
  "general_health": "Poor",
  "on_diet": "Yes",
  "comments": "Referred to dietician"
}
```

**List patients by visit date**
```
POST /visits/view
```
```json
{
  "visit_date": "2025-10-31"
}
```
Returns a list of patients who had a visit on that date, including name, age, BMI value, and BMI status.

---

## Local Setup

### Prerequisites
- Python 3.10+
- A PostgreSQL instance (local or hosted — this project uses Railway)
- Postman or curl for testing API endpoints

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/akariri79/Web-Application-Backend-Development-Practical.git
cd "Web App & Backend development practical updated"
```

**2. Create and activate a virtual environment**
```bash
python -m venv .venv

# Windows (Command Prompt)
.venv\Scripts\activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create a `.env` file** in the project root with your database connection string:
```
DATABASE_URL=postgresql+psycopg2://user:password@host:port/dbname
```
If connecting to Railway's Postgres externally (from your local machine), use the `DATABASE_PUBLIC_URL` value from Railway's Variables tab — not the internal URL.

**5. Run database migrations**
```bash
flask db upgrade
```
This creates all four tables in your Postgres instance. No manual SQL required.

**6. Start the server**
```bash
waitress-serve --host=127.0.0.1 --port=5000 run:app
```
The app is now running at `http://127.0.0.1:5000`.

---

## Making Schema Changes

If you modify any model (add a column, create a new table, etc.), run:
```bash
flask db migrate -m "describe what changed"
flask db upgrade
```
Never use `db.create_all()` — Flask-Migrate tracks schema history and `db.create_all()` bypasses it, which causes conflicts.

---

## Notes

- Patient IDs are **clinician-supplied strings** (up to 20 characters) — the system rejects duplicate registrations at both the application and database level.
- A patient can have **multiple vitals records**, but only one per visit date.
- Each vitals record links to **at most one** assessment (either General or Overweight, never both).
- The `.flaskenv` file is committed intentionally — it contains only `FLASK_APP=run.py` and no sensitive values. The `.env` file containing database credentials is excluded from version control via `.gitignore`.

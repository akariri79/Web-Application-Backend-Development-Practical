def register_routes(app):
    from .home import register_home_routes
    from .patient_registration import register_patient_routes
    from .vitals import register_vitals_routes
    from .assessment import register_assessment_routes
    from .patient_reports import register_patients_routes
    from .api_routes import register_api_routes

    register_home_routes(app)
    register_patient_routes(app)
    register_vitals_routes(app)
    register_assessment_routes(app)
    register_patients_routes(app)
    register_api_routes(app)
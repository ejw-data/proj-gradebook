from flask import Blueprint, request, redirect
from models import db, Authentication, SelectedCohort
import json
from query import submission_request, submission_missing, \
    absenses_session, absenses_unit, absenses_top5, \
    feedback, at_risk_top5, feedback_comments, alerts, \
    feedback_most_recent, cohort_list


api = Blueprint('api', __name__, url_prefix='/api')

# ---------------------------------------------------------- #
# Universal routes
# ---------------------------------------------------------- #

# ---------------------------------------------------------- #

# Cohort selector route
@api.route('/cohort')
def cohorts():
    # generate list of cohorts
    data = cohort_list()
    return json.dumps(data)

# need to insert database via notebook
@api.route('/currentcohort')
def currentcohort():
    # generate list of cohorts
    cohort = SelectedCohort.query.order_by(SelectedCohort.record_id.desc()).first()
    return json.dumps({'cohort_number': cohort.cohort_id})


@api.route('/cohortsubmit', methods=['POST'])
def submit_cohort():
    cohort_id = request.form.get("cohortList")

    add_cohort = SelectedCohort(
        cohort_id = cohort_id
        )

    db.session.add(add_cohort)
    db.session.commit()
    
    print(cohort_id)
    return redirect(request.referrer)

# ---------------------------------------------------------- #
# Login routes
@api.route('/login')
def login():
    # db.create_all(bind=['login'])

    name = Authentication.query.order_by(Authentication.login_id.desc()).first()
    return json.dumps({'username': name.username,
                       'password': name.password}
                    )



@api.route('/modalsubmit', methods=['POST'])
def submit_login():
    username = request.form['user']
    password = request.form['password']

    print(f"Username is {username}")
    print(f"Password is {password}")

    # db.create_all(bind=['login'])

    add_credentials = Authentication(
        first_name= "Erin33",
        last_name = "Wills33",
        username = username,
        password = password
        )

    db.session.add(add_credentials)
    db.session.commit()

    return redirect(request.referrer)  

# ---------------------------------------------------------- #
# Unit page routes

@api.route('/submission')
def submission():
    data = submission_request()
    return json.dumps(data)

@api.route('/missing-submission')
def missing_submission():
    data = submission_missing()
    return json.dumps(data)
 
@api.route('/absenses-person')
def absenses_by_person():
    data = absenses_top5()
    return json.dumps(data)
 
@api.route('/absenses-unit')
def absenses_by_unit():
    data = absenses_unit()
    return json.dumps(data)
 
@api.route('/feedback')
def overall_feedback():
    data = feedback()
    return json.dumps(data)
 
@api.route('/at-risk')
def at_risk_students():
    data = at_risk_top5()
    return json.dumps(data)
 
@api.route('/feedback-comments')
def feedback_comments_list():
    data = feedback_comments()
    return json.dumps(data)
 
@api.route('/alerts')
def student_alerts():
    data = alerts()
    return json.dumps(data)

@api.route('/feedback_recent')
def feedback_recent():
    data = feedback_most_recent()
    return json.dumps(data)



# ---------------------------------------------------------- #
# Session routes

@api.route('/absenses-session')
def absenses_by_session():
    data = absenses_session()
    return json.dumps(data)


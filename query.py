from sqlalchemy import create_engine

# --------------------------------------------------- #
# Universal queries used in the routes
# Note:  most of the below code could be done in a much simpler way using pandas
#        I chose the below methods so I did not need to import any other packages

# generate list of cohorts
def cohort_list():
    engine = create_engine('sqlite:///gradebook.db')

    query = '''
    SELECT cohort_name, cohort_id  
    FROM cohort 
    ORDER BY start_date DESC;
    '''

    conn = engine.connect()

    data = conn.execute(query).fetchall()

    results = []
    for i,j in data:
        results.append([i,j])

    conn.close()
    engine.dispose()

    return results







# --------------------------------------------------- #
# Unit queries

def submission_request():

    engine = create_engine('sqlite:///gradebook.db')

    query = '''
    With studentCTE(student_id, person_id,sCTEcohort_id) AS 
        (SELECT student_id, person_id, cohort_id
        FROM student s 
        WHERE cohort_id = 
            (SELECT c.cohort_id 
            FROM cohort c 
            WHERE DATE() > c.start_date
            AND DATE() < c.end_date
            )
        ), 
    unitCTE (unit_id, uCTEcohort_id, unit_due) AS 
        (SELECT unit_id, cohort_id, unit_due
        FROM unit u
        WHERE cohort_id = 
            (SELECT c.cohort_id 
            FROM cohort c 
            WHERE DATE() > c.start_date
            AND DATE() < c.end_date
            )
        AND unit_required = 1
        AND unit_due < DATE()
        )
    SELECT sb.unit_id, 
        COUNT(1) FILTER(WHERE label = "Very Early") as VeryEarly,
        COUNT(1) FILTER(WHERE label = "Early") as Early,
        COUNT(1) FILTER(WHERE label = "On-time") as Ontime, 
        COUNT(1) FILTER(WHERE label = "Late") as Late, 
        COUNT(1) FILTER(WHERE label = "Very Late") as VeryLate, 
        COUNT(1) FILTER(WHERE label IS NULL) as NU
    FROM submission sb
    INNER JOIN studentCTE 
    ON sb.student_id = studentCTE.student_id
    INNER JOIN unitCTE
    ON sb.unit_id = unitCTE.unit_id  
    LEFT JOIN (
    SELECT attendance_status.*, lead(bin) OVER (ORDER BY bin NULLS FIRST) AS next_bin
    from attendance_status
    ) b ON (bin IS NULL OR ROUND(JULIANDAY(sb.submission_date) - JULIANDAY(unitCTE.unit_due)) >= bin) AND (next_bin IS NULL OR ROUND(JULIANDAY(sb.submission_date) - JULIANDAY(unitCTE.unit_due)) < next_bin)
    GROUP BY sb.unit_id;
    '''

    conn = engine.connect()

    data = conn.execute(query).fetchall()

    unit, veryearly, early, ontime, late, verylate, ns = [], [], [], [], [], [], []

    for row in data:
        unit.append(row[0])
        veryearly.append(row[1])
        early.append(row[2])
        ontime.append(row[3])
        late.append(row[4])
        verylate.append(row[5])
        ns.append(row[6])

    submission_dict = {
        "unit":unit,
        "veryearly":veryearly,
        "early":early,
        "ontime":ontime,
        "late":late,
        "verylate":verylate,
        "notsubmitted": ns
    }  

    conn.close()
    engine.dispose()

    return submission_dict

def submission_missing():

    engine = create_engine('sqlite:///gradebook.db')

    query = '''
    SELECT s.first_name, s.last_name, COUNT(1) as cnt
    FROM submission s 
    WHERE s.submission_date IS NULL
    AND s.student_id IN 
        (SELECT student_id
        FROM student s2
        WHERE s2.cohort_id = 3)
    AND s.unit_id IN
        (SELECT unit_id
        FROM unit u
        WHERE unit_due < DATE()
        AND u.cohort_id = 3)
    GROUP BY s.last_name
    ORDER BY cnt DESC
    LIMIT 5;
    '''

    conn = engine.connect()

    data = conn.execute(query).fetchall()

    missing_list = []
    for row in data:
        name = f'{row[0]} {row[1]}'
        misses = row[2]
        missing_list.append( (name, misses) )

    conn.close()
    engine.dispose()

    return missing_list 

def absenses_top5():

    engine = create_engine('sqlite:///gradebook.db')

    query = '''
    WITH personCTE AS 
        (SELECT person_id, student_id 
        FROM student s 
        WHERE cohort_id = 3), 
    absenseCTE AS (SELECT a.student_id, COUNT(1) as Absenses
        FROM attendance a 
        WHERE a.student_id IN 
            (SELECT s.student_id
            FROM student s
            WHERE s.cohort_id=3)
        AND a.present IS NULL
        GROUP BY a.student_id 
        ORDER BY Absenses DESC)
    SELECT name, aCTE.Absenses
    FROM personCTE
    INNER JOIN person p2 
    ON p2.person_id = personCTE.person_id
    INNER JOIN absenseCTE aCTE
    ON aCTE.student_id = personCTE.student_id
    ORDER BY Absenses DESC
    LIMIT 5;
    '''
    conn = engine.connect()

    data = conn.execute(query).fetchall()

    # logic 
    results = []
    for i,j in data:
        results.append([i,j])

    conn.close()
    engine.dispose()

    return results

def absenses_unit():

    engine = create_engine('sqlite:///gradebook.db')

    query = '''
    WITH temp_Session (session_idCTE, session_nameCTE, unit_idCTE) AS 
        (SELECT session_id, session_name, unit_id
        FROM session 
        WHERE cohort_id = 3
        AND DATE() > session_start),
    temp_Attendance AS 
        (SELECT *, count(1) as absenses 
        FROM attendance a
        WHERE present is NULL
        GROUP BY session_id)
    SELECT unit_idCTE, SUM(absenses) as TotalAbsenses
    FROM temp_Session
    LEFT JOIN temp_Attendance
    ON temp_Session.session_idCTE = temp_Attendance.session_id
    GROUP BY unit_idCTE
    ORDER BY unit_idCTE
    '''
    conn = engine.connect()

    data = conn.execute(query).fetchall()

    # logic 
    unit, absenses = [], []

    for row in data:
        unit.append(row[0])
        absenses.append(row[1])


    results = {
        "unit":unit,
        "absenses":absenses
    } 

    conn.close()
    engine.dispose()

    return results  

def feedback():

    engine = create_engine('sqlite:///gradebook.db')

    query = '''
    SELECT 
        f.week, 
        AVG(f.overall_satisfaction), 
        AVG(f.academic_support),
        AVG(f.outside_class_productivity), 
        AVG(f.pace), 
        AVG(f.instructor_engagement), 
        AVG(f.instructor_clarity), 
        AVG(f.instructor_knowledge), 
        AVG(f.homework_feedback),
        AVG(f.outside_class_time_spent) 
    FROM feedback f 
    WHERE f.student_id IN 
        (SELECT s.student_id
        FROM student s
        WHERE s.cohort_id=3)
    GROUP BY f.week 
    ORDER BY f.week ASC;
    '''
    conn = engine.connect()

    data = conn.execute(query).fetchall()

    # logic 
    week, satisfaction, support, outside_learning, pace = [], [], [], [], []
    engagement, clarity, knowledge, homework, time  = [], [], [], [], []

    for row in data:
        week.append(row[0])
        satisfaction.append(round(row[1],2))
        support.append(round(row[2],2))
        outside_learning.append(round(row[3],2))
        pace.append(round(row[4],2))
        engagement.append(round(row[5],2))
        clarity.append(round(row[6],2))
        knowledge.append(round(row[7],2))
        homework.append(round(row[8],2))
        time.append(round(row[9],2))
        

    results = {
        "week":week,
        "satisfaction":satisfaction,
        "support":support,
        "outside_learning":outside_learning,
        "pace":pace,
        "engagement":engagement,
        "clarity":clarity,
        "knowledge":knowledge,
        "homework":homework,
        "time":time
    } 

    conn.close()
    engine.dispose()

    return results  

def at_risk_top5():

    engine = create_engine('sqlite:///gradebook.db')

    query = '''
    WITH riskCTE AS
    (SELECT 
        f.student_id,
        (
            IIF(f.overall_satisfaction > 3, 1,0) + 
            IIF(f.academic_support > 3, 1,0) + 
            IIF(f.outside_class_productivity > 3, 1,0) + 
            IIF(f.pace > 3, 1,0) + 
            IIF(f.instructor_engagement > 3, 1,0) + 
            IIF(f.instructor_clarity > 3, 1,0 + 
            IIF(f.instructor_knowledge > 3, 1,0) + 
            IIF(f.homework_feedback > 3, 1,0) + 
            IIF(f.outside_class_time_spent > 3, 1,0) 
        )  
        ) as at_risk
    FROM feedback f
    WHERE student_id IN 
        (SELECT student_id
        FROM student s
        WHERE s.cohort_id = 		
            (SELECT c.cohort_id 
            FROM cohort c 
            WHERE DATE() > c.start_date
            AND DATE() < c.end_date
            )
        )
    )
    SELECT p.name, riskCTE.at_risk
    FROM riskCTE
    INNER JOIN student s2  
    ON s2.student_id = riskCTE.student_id 
    INNER JOIN person p 
    ON s2.person_id = p.person_id 
    ORDER BY riskCTE.at_risk DESC
    LIMIT 5;
    '''

    conn = engine.connect()

    data = conn.execute(query).fetchall()

    # logic 
    results = []
    for i,j in data:
        results.append([i,j])

    conn.close()
    engine.dispose()

    return results 

def feedback_comments():

    engine = create_engine('sqlite:///gradebook.db')

    query = '''
    With studentCTE AS 
        (SELECT student_id, tempStudent.person_id, p.name
        FROM
            (SELECT s.student_id, s.person_id
            FROM student s
            WHERE s.cohort_id=3) as tempStudent
        INNER JOIN person p 
        ON p.person_id = tempStudent.person_id
        ),
    feedbackCTE AS 
        (SELECT * 
        FROM feedback f
        WHERE student_id IN 
            (SELECT student_id
            FROM student s2
            WHERE s2.cohort_id = 3
            )
        AND week <= 
            (SELECT MAX(f.week) as maxWeek
            FROM feedback f
            WHERE student_id IN 
                (SELECT student_id
                FROM student s3
                WHERE s3.cohort_id = 3
                )
            )
        AND (class_comments IS NOT NULL OR instructional_support_comments IS NOT NULL)
        )
    SELECT feedbackCTE.week, name, class_comments, instructional_support_comments
    FROM feedbackCTE
    LEFT JOIN studentCTE
    ON feedbackCTE.student_id = studentCTE.student_id;
    '''
    conn = engine.connect()

    data = conn.execute(query).fetchall()

    # logic 
    results = []
    for i,j,k,l in data:
        results.append([i,j,k,l])

    conn.close()
    engine.dispose()

    return results 

def alerts():

    engine = create_engine('sqlite:///gradebook.db')

    query = '''
    WITH riskCTE AS
    (SELECT 
        f.student_id,
        (
            IIF(f.overall_satisfaction > 3, 1,0) + 
            IIF(f.academic_support > 3, 1,0) + 
            IIF(f.outside_class_productivity > 3, 1,0) + 
            IIF(f.pace > 3, 1,0) + 
            IIF(f.instructor_engagement > 3, 1,0) + 
            IIF(f.instructor_clarity > 3, 1,0 + 
            IIF(f.instructor_knowledge > 3, 1,0) + 
            IIF(f.homework_feedback > 3, 1,0) + 
            IIF(f.outside_class_time_spent > 3, 1,0) 
        )  
        ) as at_risk
    FROM feedback f
    WHERE student_id IN 
        (SELECT student_id
        FROM student s
        WHERE s.cohort_id = 		
            (SELECT c.cohort_id 
            FROM cohort c 
            WHERE DATE() > c.start_date
            AND DATE() < c.end_date
            )
        )
    )
    SELECT p.name, riskCTE.at_risk
    FROM riskCTE
    INNER JOIN student s2  
    ON s2.student_id = riskCTE.student_id 
    INNER JOIN person p 
    ON s2.person_id = p.person_id 
    ORDER BY riskCTE.at_risk DESC
    LIMIT 5;
    '''
    conn = engine.connect()

    data = conn.execute(query).fetchall()

    # logic 
    results = []
    for i,j in data:
        results.append([i,j])

    conn.close()
    engine.dispose()

    return results 

def feedback_most_recent():

    engine = create_engine('sqlite:///gradebook.db')

    query = '''
    SELECT 
        f.week, 
        AVG(f.overall_satisfaction), 
        AVG(f.academic_support),
        AVG(f.outside_class_productivity), 
        AVG(f.pace), 
        AVG(f.instructor_engagement), 
        AVG(f.instructor_clarity), 
        AVG(f.instructor_knowledge), 
        AVG(f.homework_feedback),
        AVG(f.outside_class_time_spent) 
    FROM feedback f 
    WHERE f.student_id IN 
        (SELECT s.student_id
        FROM student s
        WHERE s.cohort_id=3)
    GROUP BY f.week 
    ORDER BY f.week DESC 
    LIMIT 1;
    '''
    conn = engine.connect()

    data = conn.execute(query).fetchall()
    data = data[0]
    # logic 
    results = {
        "week":round(data[0],2),
        "satisfaction":round(data[1],2),
        "support":round(data[2],2),
        "outside_learning":round(data[3],2),
        "pace":round(data[4],2),
        "engagement":round(data[5],2),
        "clarity":round(data[6],2),
        "knowledge":round(data[7],2),
        "homework":round(data[8],2),
        "time":round(data[9],2)
    } 

    conn.close()
    engine.dispose()

    return results 

# --------------------------------------------------- #
# Session queries

def absenses_session():
    # used to supply data to chart
    engine = create_engine('sqlite:///gradebook.db')

    query = '''
    WITH temp_Session (session_idCTE, session_chapCTE, session_nameCTE, unit_idCTE) AS 
        (SELECT session_id, session_chapter, session_name, unit_id
        FROM session 
        WHERE cohort_id = 3
        AND DATE() > session_start),
    total_absenses AS 
        (SELECT session_id, COUNT(1) as absenses 
        FROM attendance a2
        WHERE present is NULL
        GROUP BY session_id)
    SELECT session_chapCTE, session_nameCTE, COALESCE(absenses,0) as TotalAbsenses 
    FROM temp_Session
    LEFT JOIN total_absenses as ta 
    ON temp_Session.session_idCTE = ta.session_id
    GROUP BY temp_Session.session_chapCTE
    ORDER BY session_chapCTE ASC;	
    '''
    conn = engine.connect()

    data = conn.execute(query).fetchall()

    # logic 
    chapter, name, absenses = [], [], []

    for row in data:
        chapter.append(row[0])
        name.append(row[1])
        absenses.append(row[2])


    results = {
        "chapter":chapter,
        "name":name,
        "absenses":absenses
    } 

    conn.close()
    engine.dispose()

    return results  

def feedback_comments_session():

    engine = create_engine('sqlite:///gradebook.db')

    query = '''
    With studentCTE AS 
        (SELECT student_id, tempStudent.person_id, p.name
        FROM
            (SELECT s.student_id, s.person_id
            FROM student s
            WHERE s.cohort_id=3) as tempStudent
        INNER JOIN person p 
        ON p.person_id = tempStudent.person_id
        ),
    feedbackCTE AS 
        (SELECT * 
        FROM feedback f
        WHERE student_id IN 
            (SELECT student_id
            FROM student s2
            WHERE s2.cohort_id = 3
            )
        AND week = 
            (SELECT MAX(f.week) as maxWeek
            FROM feedback f
            WHERE student_id IN 
                (SELECT student_id
                FROM student s3
                WHERE s3.cohort_id = 3
                )
            )
        AND (class_comments IS NOT NULL OR instructional_support_comments IS NOT NULL)
        )
    SELECT feedbackCTE.week, name, class_comments, instructional_support_comments
    FROM feedbackCTE
    LEFT JOIN studentCTE
    ON feedbackCTE.student_id = studentCTE.student_id;
    '''
    conn = engine.connect()

    data = conn.execute(query).fetchall()

    # logic 
    results = []
    for i,j,k,l in data:
        results.append([i,j,k,l])

    conn.close()
    engine.dispose()

    return results 




# def template2():

#     engine = create_engine('sqlite:///gradebook.db')

#     query = '''
    
#     '''
#     conn = engine.connect()

#     data = conn.execute(query).fetchall()

#     # logic 
#     results = []
#     results.append(data)

#     conn.close()
#     engine.dispose()

#     return results 

# def template3():

#     engine = create_engine('sqlite:///gradebook.db')

#     query = '''
    
#     '''
#     conn = engine.connect()

#     data = conn.execute(query).fetchall()

#     # logic 
#     results = []
#     results.append(data)

#     conn.close()
#     engine.dispose()

#     return results 

# def template4():

#     engine = create_engine('sqlite:///gradebook.db')

#     query = '''
    
#     '''
#     conn = engine.connect()

#     data = conn.execute(query).fetchall()

#     # logic 
#     results = []
#     results.append(data)

#     conn.close()
#     engine.dispose()

#     return results 




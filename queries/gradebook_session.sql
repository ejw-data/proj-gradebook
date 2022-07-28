

--1.  Absenses per Session 
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

--1. most recent feedback comments
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
ON feedbackCTE.student_id = studentCTE.student_id


--1.  Video links per SESSION 
SELECT session_chapter, session_name, session_start, zoom_url  
FROM "session" s 
WHERE cohort_id = 
	(SELECT MAX(s.cohort_id) as maxCohort
        FROM session s)
AND session_start < DATE()
ORDER BY session_start ASC;


--1.  Most at risk (top 5) 
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


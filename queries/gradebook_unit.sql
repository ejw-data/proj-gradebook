--Queries - Units  

--1.  Alerts  (???)  


--1.  Available cohorts
SELECT cohort_name, cohort_id  
FROM cohort c 
ORDER BY start_date DESC;



--1.  homwork submissions, by early, on-time, late, not-submitted

-- new database containing data
SELECT * FROM attendance_status;



-- Binned data

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
SELECT sb.unit_id, label, COUNT(1) AS Total_Submissions, ROUND(JULIANDAY(sb.submission_date) - JULIANDAY(unitCTE.unit_due)) as days_from_due_date, DENSE_RANK() OVER(ORDER BY sb.unit_id) as week
FROM submission sb
INNER JOIN studentCTE 
ON sb.student_id = studentCTE.student_id
INNER JOIN unitCTE
ON sb.unit_id = unitCTE.unit_id  
LEFT JOIN (
SELECT attendance_status.*, lead(bin) OVER (ORDER BY bin NULLS FIRST) AS next_bin
from attendance_status) b 
ON (bin IS NULL OR days_from_due_date >= bin) AND (next_bin IS NULL OR days_from_due_date < next_bin)
GROUP BY sb.unit_id, label;

-- Need to give name and status and then aggregate them by unit and session and person




-- 1 pivot (chart 1)

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
	COUNT(1) FILTER(WHERE label IS NULL) as NU, 
	COUNT(1) FILTER(WHERE label = "Late") as Late, 
	COUNT(1) FILTER(WHERE label = "On-time") as Ontime, 
	COUNT(1) FILTER(WHERE label = "VeryLate") as VeryLate, 
	COUNT(1) FILTER(WHERE label = "Early") as Early,
	COUNT(1) FILTER(WHERE label = "VeryEarly") as VeryEarly
FROM submission sb
INNER JOIN studentCTE 
ON sb.student_id = studentCTE.student_id
INNER JOIN unitCTE
ON sb.unit_id = unitCTE.unit_id  
LEFT JOIN (
SELECT attendance_status.*, lead(bin) OVER (ORDER BY bin NULLS FIRST) AS next_bin
from attendance_status) b 
ON (bin IS NULL OR ROUND(JULIANDAY(sb.submission_date) - JULIANDAY(unitCTE.unit_due)) >= bin) AND (next_bin IS NULL OR ROUND(JULIANDAY(sb.submission_date) - JULIANDAY(unitCTE.unit_due)) < next_bin)
GROUP BY sb.unit_id;




--2a.  most missed assignments by unit (top 5)  
SELECT s.unit_id, COUNT(1) as cnt
FROM submission s 
WHERE s.submission_date IS NULL
GROUP BY s.unit_id
ORDER BY cnt DESC
LIMIT 5;

-- added subquery for student_ID of only cohort 3
-- add subquery to only get latest ID
SELECT s.unit_id, COUNT(1) as cnt
FROM submission s 
WHERE s.submission_date IS NULL 
AND s.student_id IN 
	(SELECT student_id
	FROM student s2
	WHERE s2.cohort_id = 3)
GROUP BY s.unit_id
ORDER BY cnt DESC
LIMIT 5;

--2b.  most missed assignments by person (top 5)  
--SELECT SUBSTRING(s.first_name, " ", s.last_name) as fullname, COUNT(1) as cnt
--FROM submission s 
--WHERE s.submission_date IS NULL
--GROUP BY fullname
--ORDER BY cnt DESC
--LIMIT 5;



-- Add substring search - use CTE?  so I can get the group by to work?
-- (List1)
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

SELECT * FROM session


--1. Absenses per unit
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
	


--1.  most absenses by person (top 5)  
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




--1.  Survey results as CTE 
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
	)
SELECT *
FROM feedbackCTE
LEFT JOIN studentCTE
ON feedbackCTE.student_id = studentCTE.student_id;



--1.  Survey results as derived table
SELECT * FROM
	(SELECT student_id, tempStudent.person_id, p.name
	FROM
		(SELECT s.student_id, s.person_id
		FROM student s
		WHERE s.cohort_id=3) as tempStudent
	INNER JOIN person p 
	ON p.person_id = tempStudent.person_id
	) AS ss 
INNER JOIN 
	(SELECT * 
	FROM feedback f
	WHERE f.week = 
		(SELECT MAX(f.week) as maxWeek
		FROM feedback f
		WHERE student_id IN 
			(SELECT student_id
			FROM student s2
			WHERE s2.cohort_id = 3
			)
		)
	AND f.student_id IN
		(SELECT s3.student_id
		FROM student s3
		WHERE s3.cohort_id = 3
		)
	) as tt
ON ss.student_id = tt.student_id;





--1. summarized values for most recent feedback - Overall satisfaction, Instructor Score, Support Score, Pace, etc.
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

--1.  Week 7 Summarized feedback 

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
		IIF(f.instructor_clarity > 3, 1,0) + 
		IIF(f.instructor_knowledge > 3, 1,0) + 
		IIF(f.homework_feedback > 3, 1,0) + 
		IIF(f.outside_class_time_spent > 3, 1,0) 
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




--1.  Survey feedback  (comments)

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

-- Grades and submissions
SELECT * FROM submission s;
SELECT * FROM  student;
SELECT * FROM unit;

-- Homework submissions:
SELECT unit_name, students_enrolled, hw_submissions, graded_assignments, (ROUND(graded_assignments/students_enrolled*100,2)) AS percent_submitted  
FROM unit
WHERE cohort_id = 3
AND unit_required = TRUE;

-- Student Notes and Grader Feedback
SELECT unit_id, first_name, last_name, grade, submission_notes, feedback
FROM submission s 
WHERE unit_id IN 
	(SELECT unit_id 
	FROM unit
	WHERE cohort_id = 3
	AND unit_required = TRUE);


-- unit names formatted
SELECT unit_id, SUBSTRING(unit_name, IIF(LENGTH(unit_name) < 10, unit_name, INSTR(unit_name, " ")+ 1)) AS title, unit_due
FROM unit
WHERE career_assignment_bool = FALSE 
AND unit_required = TRUE
AND cohort_id = 3;


-- convert letter grades to numerical
SELECT grade,
	CASE grade
		WHEN 'A+' THEN 100
		WHEN 'A' THEN 96
		WHEN 'A-' THEN 93
		WHEN 'B+' THEN 90
		WHEN 'B' THEN 86
		WHEN 'B-' THEN 83
		WHEN 'C+' THEN 80
		WHEN 'C' THEN 76
		WHEN 'C-' THEN 73
		WHEN 'D+' THEN 66
		WHEN 'D' THEN 63
		WHEN 'D-' THEN 60
		ELSE 0
		END score
FROM submission s ;

SELECT * FROM submission s 

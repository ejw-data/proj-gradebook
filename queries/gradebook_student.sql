-- Drop down menu
WITH studentCTE AS 
	(SELECT s.student_id, s.person_id  
	FROM student s 
	WHERE cohort_id = 3)
SELECT student_id, name
FROM studentCTE
INNER JOIN person p 
ON studentCTE.person_id = p.person_id 



--1.  Week Averages Summarized feedback per student 

SELECT 
	f.student_id, 
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
WHERE f.student_id = 54;

--1.  All weeks of one person (and most recent)

SELECT 
	f.student_id, 
	f.week,
	f.overall_satisfaction, 
	f.academic_support,
	f.outside_class_productivity, 
	f.pace, 
	f.instructor_engagement, 
	f.instructor_clarity, 
	f.instructor_knowledge, 
	f.homework_feedback,
	f.outside_class_time_spent 
FROM feedback f 
WHERE f.student_id = 54
ORDER BY week ASC;

-- Only most recent week
SELECT 
	f.student_id, 
	f.week,
	f.overall_satisfaction, 
	f.academic_support,
	f.outside_class_productivity, 
	f.pace, 
	f.instructor_engagement, 
	f.instructor_clarity, 
	f.instructor_knowledge, 
	f.homework_feedback,
	f.outside_class_time_spent 
FROM feedback f 
WHERE f.student_id = 54
ORDER BY week DESC
LIMIT 1;


-- Homework missing
SELECT count(1) AS "Not Submitted"
FROM submission s 
WHERE student_id = 54
AND submission_date IS NOT NULL
AND s.unit_id IN 
	(SELECT unit_id
	FROM unit u
	WHERE cohort_id = 		
		(SELECT c.cohort_id 
		FROM cohort c 
		WHERE DATE() > c.start_date
		AND DATE() < c.end_date
		)
	AND unit_required = 1
	AND unit_due < DATE()
	);

--Total Absenses
SELECT count(1) as Absenses 
FROM attendance a 
WHERE a.student_id = 54
AND a.present is NULL;

-- CURENT at-Risk
SELECT 
	f.student_id, 
	f.week,
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
WHERE student_id = 54
ORDER BY f.week DESC
LIMIT 1;

-- Days since last homework submission
SELECT (JULIANDAY(DATE()) - JULIANDAY(submission_date)) as Days_since_last_submission
FROM submission s 
WHERE s.student_id = 54
ORDER BY submission_date DESC
LIMIT 1

-- AT Risk Rating
SELECT 
	f.student_id, f.week,
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
WHERE student_id = 54


-- Submission status (need to check)
With unitCTE (unit_id, unit_name, uCTEcohort_id, unit_due) AS 
	(SELECT unit_id, unit_name, cohort_id, unit_due
	FROM unit u
	WHERE cohort_id = 		
		(SELECT c.cohort_id 
		FROM cohort c 
		WHERE DATE() > c.start_date
		AND DATE() < c.end_date
		)
	AND unit_required = 1
	AND unit_due < DATE()
	),
submissionCTE AS 
	(SELECT unit_id, submission_date 
	FROM submission
	WHERE student_id = 54)
SELECT unitCTE.unit_name, (ROUND(JULIANDAY(sCTE.submission_date) - JULIANDAY(unitCTE.unit_due))) AS days_from_due_date, label 
FROM submissionCTE sCTE
INNER JOIN unitCTE
ON sCTE.unit_id = unitCTE.unit_id  
LEFT JOIN 
	(SELECT attendance_status.*, lead(bin) OVER (ORDER BY bin NULLS FIRST) AS next_bin
	 FROM attendance_status) b 
ON (bin IS NULL OR ROUND(JULIANDAY(sCTE.submission_date) - JULIANDAY(unitCTE.unit_due)) >= bin) AND (next_bin IS NULL OR ROUND(JULIANDAY(sCTE.submission_date) - JULIANDAY(unitCTE.unit_due)) < next_bin)
GROUP BY sCTE.unit_id;


-- Feedback comments
SELECT week, class_comments, instructional_support_comments
FROM feedback f
WHERE student_id = 54
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

-- Grader feedback (only one student)
SELECT feedback
FROM submission s  
WHERE s.student_id = 54
AND feedback IS NOT NULL;


-- Grader feedback (all cohort students)
SELECT first_name, last_name, unit_id, feedback
FROM submission s  
WHERE s.student_id = 
	(SELECT student_id
	FROM student s3
	WHERE s3.cohort_id = 3
	)
AND feedback IS NOT NULL;

SELECT * FROM submission s  

SELECT * FROM grade g 

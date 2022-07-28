
--Find all students from current cohort
With temp_table(student_id, person_id) 
as (SELECT student_id, person_id
FROM student s 
WHERE cohort_id = (
	SELECT c.cohort_id 
	FROM cohort c 
	WHERE DATE() > c.start_date
	AND DATE() < c.end_date
	)
)
SELECT tt.*, p.name 
FROM temp_table tt
INNER JOIN person p 
ON tt.person_id = p.person_id 


-- Feedback of One Person
With studentCTE(student_id, person_id) AS 
	(SELECT student_id, person_id
	FROM student s 
	WHERE cohort_id = 
		(SELECT c.cohort_id 
		FROM cohort c 
		WHERE DATE() > c.start_date
		AND DATE() < c.end_date
		)
	),
feedbackCTE AS 
	(SELECT * 
	FROM feedback f
	WHERE week IN 
		(SELECT w.week_id
		FROM  week w 
		WHERE w.week_end_date < DATE()
		AND w.cohort_id = 
			(SELECT c.cohort_id
			FROM cohort c
			WHERE DATE() > c.start_date 
			AND DATE() < c.end_date 
			)
		)
	)
SELECT p.name, fCTE.* 
FROM studentCTE sCTE
INNER JOIN feedbackCTE fCTE 
ON sCTE.student_id = fCTE.student_id 
INNER JOIN person p 
ON p.person_id = sCTE.person_id
WHERE fCTE.student_id = 53;



-- Feedback of Weekly Averages
With studentCTE(student_id, person_id) AS 
	(SELECT student_id, person_id
	FROM student s 
	WHERE cohort_id =
		(SELECT c.cohort_id 
		FROM cohort c 
		WHERE DATE() > c.start_date
		AND DATE() < c.end_date
		)
	),
feedbackCTE AS 
	(SELECT * 
	FROM feedback f
	WHERE week IN 
		(SELECT w.week_id
		FROM  week w 
		WHERE w.week_end_date < DATE()
		AND w.cohort_id = 
			(SELECT c.cohort_id
			FROM cohort c
			WHERE DATE() > c.start_date 
			AND DATE() < c.end_date 
			)
		)
	)
SELECT fCTE.week, AVG(fCTE.overall_satisfaction)
FROM studentCTE sCTE
INNER JOIN feedbackCTE fCTE 
ON sCTE.student_id = fCTE.student_id
GROUP BY week;
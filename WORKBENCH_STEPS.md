# MySQL Workbench Quick Steps

Use this if your teacher asks for SQL Workbench demo.

1. Open MySQL Workbench.
2. Create/open a local connection.
3. Go to **File -> Open SQL Script**.
4. Open `sql/workbench_setup.sql`.
5. Click the lightning bolt (**Execute**) to run all statements.
6. In left **SCHEMAS**, refresh and open `resume_shortlisting_db`.
7. Right click table `application` -> **Select Rows - Limit 1000**.

## Useful demo queries

```sql
USE resume_shortlisting_db;

SELECT c.name, j.job_title, a.status, s.score, s.decision
FROM candidate c
JOIN application a ON c.candidate_id = a.candidate_id
JOIN job j ON a.job_id = j.job_id
LEFT JOIN shortlist s ON a.application_id = s.application_id
ORDER BY s.score DESC;
```

```sql
SELECT job_id, COUNT(application_id) AS total_applications
FROM application
GROUP BY job_id
HAVING COUNT(application_id) >= 1;
```

# MySQL Workbench Quick Steps

Use this if your teacher asks for SQL Workbench demo.

1. Open MySQL Workbench.
2. Create/open a local connection.
3. Go to **File -> Open SQL Script**.
4. Open `sql/workbench_setup.sql`.
5. Click the lightning bolt (**Execute**) to run all statements.
6. In left **SCHEMAS**, refresh and open `resume_iq_pro`.
7. Right click table `applications` -> **Select Rows - Limit 1000**.

## Useful demo queries

```sql
USE resume_iq_pro;

SELECT c.full_name, j.title, a.match_score, a.status
FROM applications a
JOIN candidates c ON c.id = a.candidate_id
JOIN jobs j ON j.id = a.job_id
ORDER BY a.match_score DESC;
```

```sql
SELECT j.department, COUNT(*) AS total_apps, ROUND(AVG(a.match_score),2) AS avg_score
FROM applications a
JOIN jobs j ON j.id = a.job_id
GROUP BY j.department;
```

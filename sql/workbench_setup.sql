-- Resume Shortlisting DBMS Script (clean single-run version)
-- Compatible with MySQL Workbench.

DROP DATABASE IF EXISTS resume_shortlisting_db;
CREATE DATABASE resume_shortlisting_db;
USE resume_shortlisting_db;

CREATE TABLE Candidate (
    candidate_id INT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(50),
    phone VARCHAR(15),
    qualification VARCHAR(50)
);

CREATE TABLE Skill (
    skill_id INT PRIMARY KEY,
    skill_name VARCHAR(50)
);

CREATE TABLE Candidate_Skill (
    candidate_id INT,
    skill_id INT,
    PRIMARY KEY (candidate_id, skill_id),
    FOREIGN KEY (candidate_id) REFERENCES Candidate(candidate_id),
    FOREIGN KEY (skill_id) REFERENCES Skill(skill_id)
);

CREATE TABLE Experience (
    exp_id INT PRIMARY KEY,
    candidate_id INT,
    company_name VARCHAR(50),
    role VARCHAR(50),
    years_of_experience INT,
    FOREIGN KEY (candidate_id) REFERENCES Candidate(candidate_id)
);

CREATE TABLE Project (
    project_id INT PRIMARY KEY,
    candidate_id INT,
    project_title VARCHAR(100),
    technologies_used VARCHAR(100),
    FOREIGN KEY (candidate_id) REFERENCES Candidate(candidate_id)
);

CREATE TABLE Job (
    job_id INT PRIMARY KEY,
    job_title VARCHAR(50),
    min_experience INT
);

CREATE TABLE Application (
    application_id INT PRIMARY KEY,
    candidate_id INT,
    job_id INT,
    application_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (candidate_id) REFERENCES Candidate(candidate_id),
    FOREIGN KEY (job_id) REFERENCES Job(job_id)
);

CREATE TABLE Shortlist (
    shortlist_id INT AUTO_INCREMENT PRIMARY KEY,
    application_id INT,
    score INT,
    decision VARCHAR(20),
    FOREIGN KEY (application_id) REFERENCES Application(application_id)
);

INSERT INTO Skill (skill_id, skill_name) VALUES
(1, 'Java'),
(2, 'Python'),
(3, 'SQL'),
(4, 'C++'),
(5, 'Machine Learning');

INSERT INTO Candidate (candidate_id, name, email, phone, qualification) VALUES
(101, 'Lakshay Singh', 'lakshay@gmail.com', '9995559999', 'B.Tech'),
(102, 'Abhayraj Singh', 'abhay@gmail.com', '8888888000', 'B.Tech'),
(103, 'Rohit Sharma', 'rohit@gmail.com', '7776767677', 'B.Tech'),
(104, 'Neha Kapoor', 'neha@gmail.com', '9988776655', 'MCA'),
(105, 'Kunal Verma', 'kunal@gmail.com', '9876501234', 'B.Tech');

INSERT INTO Candidate_Skill (candidate_id, skill_id) VALUES
(101, 1), (101, 3),
(102, 2), (102, 3),
(103, 1), (103, 5),
(104, 2), (104, 5),
(105, 2), (105, 4);

INSERT INTO Experience (exp_id, candidate_id, company_name, role, years_of_experience) VALUES
(1, 101, 'ABC Corp', 'Software Intern', 1),
(2, 102, 'XYZ Ltd', 'Python Developer', 2),
(3, 103, 'TechSoft', 'ML Engineer', 3),
(4, 104, 'DataVista', 'Data Analyst', 2),
(5, 105, 'CloudByte', 'Backend Developer', 3);

INSERT INTO Project (project_id, candidate_id, project_title, technologies_used) VALUES
(201, 101, 'Resume Parser', 'Java, SQL'),
(202, 102, 'Web Scraper', 'Python'),
(203, 103, 'Job Recommendation System', 'Python, ML'),
(204, 104, 'Hiring Dashboard', 'Python, SQL'),
(205, 105, 'API Gateway', 'Python, C++');

INSERT INTO Job (job_id, job_title, min_experience) VALUES
(301, 'Software Engineer', 1),
(302, 'Data Analyst', 2),
(303, 'ML Engineer', 3),
(304, 'Backend Developer', 2),
(305, 'Python Developer', 2);

INSERT INTO Application (application_id, candidate_id, job_id, application_date, status) VALUES
(401, 101, 301, '2024-03-01', 'Applied'),
(402, 102, 302, '2024-03-02', 'Applied'),
(403, 103, 303, '2024-03-03', 'Applied'),
(404, 104, 302, '2024-03-04', 'Applied'),
(405, 105, 304, '2024-03-05', 'Applied');

INSERT INTO Shortlist (application_id, score, decision) VALUES
(401, 85, 'Selected'),
(402, 78, 'Selected'),
(403, 65, 'Selected'),
(404, 74, 'Selected'),
(405, 88, 'Selected');

CREATE OR REPLACE VIEW selected_candidates AS
SELECT c.name, j.job_title, s.score
FROM Candidate c
JOIN Application a ON c.candidate_id = a.candidate_id
JOIN Job j ON a.job_id = j.job_id
JOIN Shortlist s ON a.application_id = s.application_id
WHERE s.decision = 'Selected';

DELIMITER $$

CREATE PROCEDURE evaluate_application(IN app_id INT)
BEGIN
    DECLARE app_score INT;

    SET app_score = FLOOR(60 + RAND() * 40);

    IF app_score >= 70 THEN
        INSERT INTO Shortlist (application_id, score, decision)
        VALUES (app_id, app_score, 'Selected');
    ELSE
        INSERT INTO Shortlist (application_id, score, decision)
        VALUES (app_id, app_score, 'Rejected');
    END IF;
END $$

CREATE FUNCTION calculate_score(exp INT)
RETURNS INT
DETERMINISTIC
BEGIN
    RETURN exp * 20;
END $$

CREATE TRIGGER update_application_status
AFTER INSERT ON Shortlist
FOR EACH ROW
BEGIN
    UPDATE Application
    SET status = NEW.decision
    WHERE application_id = NEW.application_id;
END $$

CREATE PROCEDURE process_all_applications()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE aid INT;

    DECLARE app_cursor CURSOR FOR SELECT application_id FROM Application;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN app_cursor;
    read_loop: LOOP
        FETCH app_cursor INTO aid;
        IF done = 1 THEN
            LEAVE read_loop;
        END IF;
        CALL evaluate_application(aid);
    END LOOP;
    CLOSE app_cursor;
END $$

DELIMITER ;

START TRANSACTION;
INSERT INTO Candidate VALUES (106, 'Test User', 'test@gmail.com', '6666666666', 'B.Tech');
SAVEPOINT sp1;
ROLLBACK TO sp1;
COMMIT;

-- Useful demo queries
SELECT * FROM Candidate;
SELECT * FROM Skill;
SELECT * FROM Application;
SELECT * FROM selected_candidates;

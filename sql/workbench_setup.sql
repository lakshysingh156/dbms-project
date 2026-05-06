-- ResumeIQ Pro MySQL Workbench Setup Script
-- Run this script in MySQL Workbench to create schema + tables + demo data.

CREATE DATABASE IF NOT EXISTS resume_iq_pro;
USE resume_iq_pro;

CREATE TABLE IF NOT EXISTS candidates (
  id INT AUTO_INCREMENT PRIMARY KEY,
  full_name VARCHAR(120) NOT NULL,
  email VARCHAR(150) NOT NULL UNIQUE,
  phone VARCHAR(40),
  skills TEXT NOT NULL,
  experience_years DECIMAL(4,1) NOT NULL DEFAULT 0,
  education VARCHAR(160),
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS jobs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(120) NOT NULL,
  department VARCHAR(120) NOT NULL,
  required_skills TEXT NOT NULL,
  min_experience DECIMAL(4,1) NOT NULL DEFAULT 0,
  description TEXT,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS applications (
  id INT AUTO_INCREMENT PRIMARY KEY,
  candidate_id INT NOT NULL,
  job_id INT NOT NULL,
  resume_url VARCHAR(255),
  match_score DECIMAL(5,2) NOT NULL DEFAULT 0,
  status VARCHAR(30) NOT NULL DEFAULT 'Under Review',
  reviewer_notes TEXT,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_app_candidate FOREIGN KEY (candidate_id) REFERENCES candidates(id),
  CONSTRAINT fk_app_job FOREIGN KEY (job_id) REFERENCES jobs(id)
);

INSERT INTO candidates (full_name, email, phone, skills, experience_years, education)
VALUES
('Aarav Sharma', 'aarav.sharma@email.com', '9876543210', 'python, sql, flask, machine learning', 2.5, 'B.Tech CSE'),
('Priya Mehta', 'priya.mehta@email.com', '9811122233', 'java, spring, mysql, rest api', 3.0, 'B.Tech IT'),
('Rohan Singh', 'rohan.singh@email.com', '9898989898', 'javascript, react, nodejs, mongodb', 1.8, 'BCA');

INSERT INTO jobs (title, department, required_skills, min_experience, description)
VALUES
('Backend Developer', 'Engineering', 'python, sql, flask', 2.0, 'Develop APIs and database logic'),
('Full Stack Developer', 'Product', 'javascript, react, nodejs, sql', 2.0, 'Build end-to-end web features');

INSERT INTO applications (candidate_id, job_id, resume_url, match_score, status, reviewer_notes)
VALUES
(1, 1, 'https://example.com/resumes/aarav.pdf', 87.50, 'Shortlisted', 'Strong backend fundamentals'),
(2, 1, 'https://example.com/resumes/priya.pdf', 69.00, 'Shortlisted', 'Good SQL and API experience'),
(3, 2, 'https://example.com/resumes/rohan.pdf', 76.00, 'Shortlisted', 'Good full stack profile');

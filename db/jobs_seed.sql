-- -------------------------------------------------------------------------------------------------------
--   Used for the development of job recommendations



-- IMPORTANT    * This seed should not be used outside of the job recommendations development as
--                  it contains smaller representations of the larger tables used in this file.
--
--              * Database - helpoutsjobrec01
--              * Tables    
--                  - users
--                  - jobs
--                  - projects

--            * new - skills
--            * new - user_skills -> Reference table to link skills to users.



-- -------------------------------------------------------------------------------------------------------

-- CREATE DATABASE helpoutsjobrec01

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS job_skills;
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS user_skills;
DROP TABLE IF EXISTS skills;
DROP TABLE IF EXISTS users;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE skills (
  id INT PRIMARY KEY AUTO_INCREMENT,
  skill VARCHAR(100) NOT NULL
);

CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100)
);

CREATE TABLE user_skills (
  id INT PRIMARY KEY,
  user_id INT NOT NULL,
  skill_id INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (skill_id) REFERENCES skills(id)
);

CREATE TABLE projects (
  id INT PRIMARY KEY AUTO_INCREMENT,
  project_title VARCHAR(100) NOT NULL,
  project_type VARCHAR(20) NOT NULL,
  status VARCHAR(3) NOT NULL DEFAULT 'D',
  start_date DATETIME,
  end_date DATETIME
);

CREATE TABLE jobs (
  id INT PRIMARY KEY AUTO_INCREMENT,
  job_title VARCHAR(100) NOT NULL,
  skills VARCHAR(500),
  status VARCHAR(3) NOT NULL DEFAULT 'D',
  area VARCHAR(100) NOT NULL,
  created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
  start_date DATETIME,
  end_date DATETIME,
  project_id INT NOT NULL,
  FOREIGN KEY (project_id) REFERENCES projects(id)
);

CREATE TABLE job_skills (
  id INT PRIMARY KEY AUTO_INCREMENT,
  job_id INT NOT NULL,
  skill_id INT NOT NULL,
  FOREIGN KEY (job_id) REFERENCES jobs(id),
  FOREIGN KEY (skill_id) REFERENCES skills(id),
  UNIQUE (job_id, skill_id)
);


INSERT INTO skills (skill) VALUES
('Carpentry'),
('Painting'),
('General DIY'),
('Plumbing'),
('Electrical Repair'),
('Furniture Repair'),
('Bike Repair'),
('Tool Maintenance'),
('Gardening'),
('Landscaping'),
('Tree Planting'),
('Litter Picking'),
('Grass Cutting'),
('Hedge Trimming'),
('Community Garden Work'),
('House Cleaning'),
('Community Cleaning'),
('Basic Maintenance'),
('Furniture Moving'),
('Cooking'),
('Baking'),
('Event Setup'),
('Event Stewarding'),
('Fundraising Support'),
('Event Organisation'),
('IT Support'),
('Smartphone Help'),
('Computer Basics'),
('Website Help'),
('Music Teaching'),
('Tutoring'),
('Youth Support'),
('Community Outreach'),
('Companionship Visits');

INSERT INTO users (id, name) VALUES
    (1, 'Leo'),
    (2, 'Ryan'),
    (3, 'John'),
    (4, 'Daisy'),
    (5, 'Jemma'),
    (6, 'Patrick'),
    (7, 'Sarah'),
    (8, 'Tom'),
    (9, 'Niamh'),
    (10, 'Sean'),
    (11, 'Aoife'),
    (12, 'Michael'),
    (13, 'Laura'),
    (14, 'Brian'),
    (15, 'Emma');

INSERT INTO user_skills (id, user_id, skill_id) VALUES
    (1, 1, 1),  -- Leo knows Carpentry
    (2, 2, 9),  -- Ryan knows Gardening
    (3, 3, 20), -- John knows Cooking
    (4, 4, 26), -- Daisy knows IT Support
    (5, 5, 33), -- Jemma knows Community Outreach
    (6, 6, 1),   -- Patrick - Carpentry
    (7, 7, 9),   -- Sarah - Gardening
    (8, 8, 20),  -- Tom - Cooking
    (9, 9, 26),  -- Niamh - IT Support
    (10, 10, 33),-- Sean - Community Outreach
    (11, 11, 1), -- Aoife - Carpentry
    (12, 12, 9), -- Michael - Gardening
    (13, 13, 20),-- Laura - Cooking
    (14, 14, 26),-- Brian - IT Support
    (15, 15, 33);-- Emma - Community Outreach

INSERT INTO projects (id, project_title, project_type, status, start_date, end_date) VALUES
    (1, 'Community Improvement Initiative', 'Community', 'A', '2026-03-01 00:00:00', '2026-12-31 23:59:59');

INSERT INTO jobs (id, job_title, status, area, start_date, end_date, project_id) VALUES
    (1, 'Build & Repair Park Benches', 'A', 'Dundalk', '2026-03-15 00:00:00', '2026-05-31 00:00:00', 1),
    (2, 'Maintain Community Garden', 'A', 'Dundalk', '2026-04-01 00:00:00', '2026-08-31 00:00:00', 1),
    (3, 'Prepare Meals for Community Event', 'A', 'Dundalk', '2026-05-10 00:00:00', '2026-06-15 00:00:00', 1),
    (4, 'Tech Support for Seniors', 'A', 'Dundalk', '2026-03-20 00:00:00', '2026-09-30 00:00:00', 1),
    (5, 'Community Outreach Coordinator', 'A', 'Dundalk', '2026-06-01 00:00:00', '2026-12-31 00:00:00', 1);

INSERT INTO job_skills (job_id, skill_id) VALUES
  (1, 1),   -- Carpentry
  (2, 9),   -- Gardening
  (3, 20),  -- Cooking
  (4, 26),  -- IT Support
  (5, 33);  -- Community Outreach
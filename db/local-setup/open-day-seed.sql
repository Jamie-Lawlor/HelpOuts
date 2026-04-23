SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS logs, subscriptions, reviews, job_location, job_requests, user_jobs, map_icons, user_skills, job_skills, skills, jobs, projects, messages, user_permissions, community_requests, users, communities;

DROP PROCEDURE IF EXISTS getJobRecommendations;

SET FOREIGN_KEY_CHECKS = 1;

-- =====================

-- TABLES

-- =====================

CREATE TABLE communities (

    id INT PRIMARY KEY AUTO_INCREMENT,

    name VARCHAR(100) NOT NULL,

    area VARCHAR(100) NOT NULL,

    description VARCHAR(500) NOT NULL,

    profile_picture VARCHAR(1000),

    lat DECIMAL(9,6),

    lng DECIMAL(9,6)

);

CREATE TABLE users (

    id INT PRIMARY KEY AUTO_INCREMENT,

    name VARCHAR(50),

    email VARCHAR(120) UNIQUE,

    password VARCHAR(255),

    type VARCHAR(12),

    work_area VARCHAR(100),

    specialism VARCHAR(100),

    rating INT,

    verified BOOLEAN,

    verification_accuracy DECIMAL(5,2),

    community_id INT,

    FOREIGN KEY (community_id) REFERENCES communities(id)

);

CREATE TABLE projects (

    id INT PRIMARY KEY AUTO_INCREMENT,

    project_title VARCHAR(100),

    project_description VARCHAR(1000),

    project_type VARCHAR(20),

    start_date DATE,

    end_date DATE,

    community_id INT,

    FOREIGN KEY (community_id) REFERENCES communities(id)

);

CREATE TABLE jobs (

    id INT PRIMARY KEY AUTO_INCREMENT,

    job_title VARCHAR(100),

    job_description VARCHAR(500),

    short_title VARCHAR(50),

    short_type VARCHAR(20),

    status VARCHAR(3),

    number_of_helpers INT,

    area VARCHAR(100),

    start_date DATE,

    end_date DATE,

    project_id INT,

    FOREIGN KEY (project_id) REFERENCES projects(id)

);

CREATE TABLE skills (

    id INT PRIMARY KEY AUTO_INCREMENT,

    skill VARCHAR(100)

);

CREATE TABLE user_skills (

    user_id INT,

    skill_id INT,

    FOREIGN KEY (user_id) REFERENCES users(id),

    FOREIGN KEY (skill_id) REFERENCES skills(id)

);

CREATE TABLE job_skills (

    job_id INT,

    skill_id INT,

    FOREIGN KEY (job_id) REFERENCES jobs(id),

    FOREIGN KEY (skill_id) REFERENCES skills(id)

);

CREATE TABLE map_icons (

    id INT PRIMARY KEY AUTO_INCREMENT,

    icon_url VARCHAR(200),

    description VARCHAR(100)

);

CREATE TABLE job_location (

    lat DECIMAL(9,6),

    lng DECIMAL(9,6),

    job_id INT,

    icon_id INT,

    FOREIGN KEY (job_id) REFERENCES jobs(id),

    FOREIGN KEY (icon_id) REFERENCES map_icons(id)

);

-- =====================

-- COMMUNITIES

-- =====================

INSERT INTO communities VALUES

(1, 'Mens Shed Dundalk', 'Dundalk', 'Community workshop group', NULL, 54.0059, -6.3958),

(2, 'Ardee Tidy Towns', 'Ardee', 'Town improvement group', NULL, 53.8579, -6.5405),

(3, 'Dundalk Tidy Towns', 'Dundalk', 'Cleaner Dundalk initiative', NULL, 54.0047, -6.4012),

(4, 'Pieta', 'Monaghan', 'Mental health support', NULL, 54.2872, -6.9750),

-- 👇 YOUR OPEN DAY TEST COMMUNITY

(10, 'DKIT Open Day', 'Dundalk', 'Testing environment for open day demos', NULL, 54.0049, -6.3915);

-- =====================

-- USERS

-- =====================

INSERT INTO users VALUES

(1, 'Leo Fitz', 'leo@test.com', 'pass', 'helper', 'Dundalk', 'Electrician', 4, FALSE, 0.0, 10),

(2, 'Mark Byrne', 'mark@test.com', 'pass', 'chairperson', 'Dundalk', 'Event Manager', 5, TRUE, 99.0, 10);

-- =====================

-- PROJECTS

-- =====================

INSERT INTO projects VALUES

(1, 'Community Park', 'Build park', 'environment', '2026-01-01', '2026-06-01', 1),

-- OPEN DAY PROJECTS

(20, 'Campus Tours', 'Guide visitors', 'event', '2026-04-22', '2026-04-22', 10),

(21, 'Refreshments', 'Food & drink setup', 'event', '2026-04-22', '2026-04-22', 10);

-- =====================

-- JOBS (FIXED DATES ✅)

-- =====================

INSERT INTO jobs VALUES

(1, 'Install benches', 'Install seating', 'Benches', 'construction', 'A', 5, 'Dundalk', '2026-02-01', '2026-02-01', 1),

(30, 'Campus Tour Guide', 'Guide groups', 'Tour', 'event', 'A', 5, 'DKIT', '2026-04-22', '2026-04-22', 20),

(31, 'Coffee Assistant', 'Serve drinks', 'Coffee', 'event', 'A', 4, 'DKIT', '2026-04-22', '2026-04-22', 21);

-- =====================

-- SKILLS

-- =====================

INSERT INTO skills VALUES

(1, 'Carpentry'),

(5, 'Electrical'),

(23, 'Stewarding'),

(33, 'Communication');

INSERT INTO user_skills VALUES

(1, 5),

(1, 33);

INSERT INTO job_skills VALUES

(30, 33),

(1, 1);

-- =====================

-- MAP

-- =====================

INSERT INTO map_icons VALUES

(1, 'construction.svg', 'construction'),

(5, 'event.svg', 'event');

INSERT INTO job_location VALUES

(54.0049, -6.3915, 30, 5),

(54.0049, -6.3915, 31, 5);

-- =====================

-- STORED PROC

-- =====================

DELIMITER //

CREATE PROCEDURE getJobRecommendations (IN userId INT)

BEGIN

    SELECT j.*, COUNT(js.skill_id) AS match_score

    FROM jobs j

    JOIN projects p ON j.project_id = p.id

    JOIN job_skills js ON j.id = js.job_id

    JOIN user_skills us ON js.skill_id = us.skill_id

    WHERE us.user_id = userId

      AND p.community_id = (SELECT community_id FROM users WHERE id = userId)

    GROUP BY j.id

    ORDER BY match_score DESC;

END//

DELIMITER ;
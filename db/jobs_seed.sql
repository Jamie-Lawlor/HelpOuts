---------------------------------------------------------------------------------------------------------
--   Used for the development of job recommendations
--
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
--
--
--
--
--
--
---------------------------------------------------------------------------------------------------------

CREATE DATABASE helpoutsjobrec01

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS user_skills;
DROP TABLE IF EXISTS skills;
DROP TABLE IF EXISTS users;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE skills (
    id INT PRIMARY KEY AUTO_INCREMENT,
    skill VARCHAR(100) NOT NULL,
)
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    FOREIGN KEY (community_id) REFERENCES communities(id)
);

CREATE TABLE user_skills (
    id INT PRIMARY KEY,
    user_id INT NOT NULL,
    skill_id INT NOT NULL,
)

CREATE TABLE projects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_title VARCHAR(100) NOT NULL,
    project_type VARCHAR(20) NOT NULL,
    status VARCHAR(3) NOT NULL DEFAULT 'D',
    start_date DATETIME,
    end_date DATETIME,
);

CREATE TABLE jobs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    job_title VARCHAR(100) NOT NULL,
    skills VARCHAR(500)
    status VARCHAR(3) NOT NULL DEFAULT 'D',
    area VARCHAR(100) NOT NULL,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    start_date DATETIME,
    end_date DATETIME,
    project_id INT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id)
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
('Social Media Help'),
('Tutoring'),
('Youth Support'),
('Community Outreach'),
('Companionship Visits');

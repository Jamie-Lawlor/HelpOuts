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
SET
    FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS job_skills;

DROP TABLE IF EXISTS jobs;

DROP TABLE IF EXISTS projects;

DROP TABLE IF EXISTS user_skills;

DROP TABLE IF EXISTS skills;

DROP TABLE IF EXISTS users;

SET
    FOREIGN_KEY_CHECKS = 1;

CREATE TABLE
    skills (
        id INT PRIMARY KEY AUTO_INCREMENT,
        skill VARCHAR(100) NOT NULL
    );

CREATE TABLE
    users (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100)
    );

CREATE TABLE
    user_skills (
        id INT PRIMARY KEY,
        user_id INT NOT NULL,
        skill_id INT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (skill_id) REFERENCES skills (id)
    );

CREATE TABLE
    projects (
        id INT PRIMARY KEY AUTO_INCREMENT,
        project_title VARCHAR(100) NOT NULL,
        project_type VARCHAR(20) NOT NULL,
        status VARCHAR(3) NOT NULL DEFAULT 'D',
        start_date DATETIME,
        end_date DATETIME
    );

CREATE TABLE
    jobs (
        id INT PRIMARY KEY AUTO_INCREMENT,
        job_title VARCHAR(100) NOT NULL,
        skills VARCHAR(500),
        status VARCHAR(3) NOT NULL DEFAULT 'D',
        area VARCHAR(100) NOT NULL,
        created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        start_date DATETIME,
        end_date DATETIME,
        project_id INT NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects (id)
    );

CREATE TABLE
    job_skills (
        id INT PRIMARY KEY AUTO_INCREMENT,
        job_id INT NOT NULL,
        skill_id INT NOT NULL,
        FOREIGN KEY (job_id) REFERENCES jobs (id),
        FOREIGN KEY (skill_id) REFERENCES skills (id),
        UNIQUE (job_id, skill_id)
    );

INSERT INTO
    skills (skill)
VALUES
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

INSERT INTO
    users (id, name)
VALUES
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

-- Single Skill Users
-- INSERT INTO user_skills (id, user_id, skill_id) VALUES
--     (1, 1, 1),  -- Leo knows Carpentry
--     (2, 2, 9),  -- Ryan knows Gardening
--     (3, 3, 20), -- John knows Cooking
--     (4, 4, 26), -- Daisy knows IT Support
--     (5, 5, 33), -- Jemma knows Community Outreach
--     (6, 6, 1),   -- Patrick - Carpentry
--     (7, 7, 9),   -- Sarah - Gardening
--     (8, 8, 20),  -- Tom - Cooking
--     (9, 9, 26),  -- Niamh - IT Support
--     (10, 10, 33),-- Sean - Community Outreach
--     (11, 11, 1), -- Aoife - Carpentry
--     (12, 12, 9), -- Michael - Gardening
--     (13, 13, 20),-- Laura - Cooking
--     (14, 14, 26),-- Brian - IT Support
--     (15, 15, 33);-- Emma - Community Outreach
-- Multi-Skill Users
INSERT INTO
    user_skills (id, user_id, skill_id)
VALUES
    -- Leo
    (1, 1, 1),
    (2, 1, 2),
    (3, 1, 3),
    (4, 1, 6),
    (5, 1, 8),
    -- Ryan
    (6, 2, 9),
    (7, 2, 10),
    (8, 2, 12),
    (9, 2, 13),
    (10, 2, 14),
    -- John
    (11, 3, 20),
    (12, 3, 21),
    (13, 3, 22),
    (14, 3, 24),
    (15, 3, 25),
    -- Daisy
    (16, 4, 26),
    (17, 4, 27),
    (18, 4, 28),
    (19, 4, 29),
    (20, 4, 30),
    -- Jemma
    (21, 5, 33),
    (22, 5, 32),
    (23, 5, 31),
    (24, 5, 34),
    (25, 5, 23),
    -- Patrick
    (26, 6, 4),
    (27, 6, 18),
    (28, 6, 19),
    (29, 6, 3),
    (30, 6, 5),
    -- Sarah
    (31, 7, 15),
    (32, 7, 11),
    (33, 7, 9),
    (34, 7, 10),
    (35, 7, 12),
    -- Tom
    (36, 8, 20),
    (37, 8, 22),
    (38, 8, 23),
    (39, 8, 17),
    (40, 8, 16),
    -- Niamh
    (41, 9, 26),
    (42, 9, 29),
    (43, 9, 30),
    (44, 9, 33),
    (45, 9, 28),
    -- Sean
    (46, 10, 33),
    (47, 10, 24),
    (48, 10, 25),
    (49, 10, 23),
    (50, 10, 30),
    -- Aoife
    (51, 11, 7),
    (52, 11, 8),
    (53, 11, 3),
    (54, 11, 6),
    (55, 11, 5),
    -- Michael
    (56, 12, 13),
    (57, 12, 14),
    (58, 12, 9),
    (59, 12, 18),
    (60, 12, 12),
    -- Laura
    (61, 13, 21),
    (62, 13, 20),
    (63, 13, 33),
    (64, 13, 32),
    (65, 13, 31),
    -- Brian
    (66, 14, 26),
    (67, 14, 27),
    (68, 14, 28),
    (69, 14, 33),
    (70, 14, 24),
    -- Emma
    (71, 15, 16),
    (72, 15, 17),
    (73, 15, 33),
    (74, 15, 34),
    (75, 15, 20);

INSERT INTO
    projects (
        id,
        project_title,
        project_type,
        status,
        start_date,
        end_date
    )
VALUES
    (
        1,
        'Community Improvement Initiative',
        'Community',
        'A',
        '2026-03-01 00:00:00',
        '2026-12-31 23:59:59'
    ),
    (
        2,
        'Town Tidy-Up Week',
        'Community',
        'A',
        '2026-04-01 00:00:00',
        '2026-04-30 23:59:59'
    ),
    (
        3,
        'Senior Support & Digital Help',
        'Support',
        'A',
        '2026-03-15 00:00:00',
        '2026-10-31 23:59:59'
    ),
    (
        4,
        'Community Events & Fundraising',
        'Events',
        'A',
        '2026-05-01 00:00:00',
        '2026-12-31 23:59:59'
    );

INSERT INTO
    jobs (
        id,
        job_title,
        status,
        area,
        start_date,
        end_date,
        project_id
    )
VALUES
    (
        1,
        'Build & Repair Park Benches',
        'A',
        'Dundalk',
        '2026-03-15 00:00:00',
        '2026-05-31 00:00:00',
        1
    ),
    (
        2,
        'Maintain Community Garden',
        'A',
        'Dundalk',
        '2026-04-01 00:00:00',
        '2026-08-31 00:00:00',
        1
    ),
    (
        3,
        'Prepare Meals for Community Event',
        'A',
        'Dundalk',
        '2026-05-10 00:00:00',
        '2026-06-15 00:00:00',
        1
    ),
    (
        4,
        'Tech Support for Seniors',
        'A',
        'Dundalk',
        '2026-03-20 00:00:00',
        '2026-09-30 00:00:00',
        1
    ),
    (
        5,
        'Community Outreach Coordinator',
        'A',
        'Dundalk',
        '2026-06-01 00:00:00',
        '2026-12-31 00:00:00',
        1
    ),
    (
        6,
        'Community Litter Picking Team',
        'A',
        'Dundalk',
        '2026-04-05 00:00:00',
        '2026-04-20 00:00:00',
        2
    ),
    (
        7,
        'Grass Cutting for Public Green',
        'A',
        'Dundalk',
        '2026-04-06 00:00:00',
        '2026-04-25 00:00:00',
        2
    ),
    (
        8,
        'Paint Community Railings',
        'A',
        'Dundalk',
        '2026-04-10 00:00:00',
        '2026-04-28 00:00:00',
        2
    ),
    (
        9,
        'Fix Small Public Repairs',
        'A',
        'Dundalk',
        '2026-04-12 00:00:00',
        '2026-04-30 00:00:00',
        2
    ),
    (
        10,
        'Smartphone Help Drop-In',
        'A',
        'Dundalk',
        '2026-03-20 00:00:00',
        '2026-09-30 00:00:00',
        3
    ),
    (
        11,
        'Computer Basics Workshop Assistant',
        'A',
        'Dundalk',
        '2026-04-01 00:00:00',
        '2026-10-31 00:00:00',
        3
    ),
    (
        12,
        'Home Visit Companionship',
        'A',
        'Dundalk',
        '2026-03-25 00:00:00',
        '2026-12-15 00:00:00',
        3
    ),
    (
        13,
        'Basic Maintenance for Seniors Homes',
        'A',
        'Dundalk',
        '2026-04-05 00:00:00',
        '2026-11-30 00:00:00',
        3
    ),
    (
        14,
        'Event Setup Crew',
        'A',
        'Dundalk',
        '2026-05-10 00:00:00',
        '2026-06-30 00:00:00',
        4
    ),
    (
        15,
        'Event Stewarding Volunteers',
        'A',
        'Dundalk',
        '2026-06-01 00:00:00',
        '2026-08-31 00:00:00',
        4
    ),
    (
        16,
        'Fundraising Support Team',
        'A',
        'Dundalk',
        '2026-05-15 00:00:00',
        '2026-12-31 00:00:00',
        4
    ),
    (
        17,
        'Community Outreach for Events',
        'A',
        'Dundalk',
        '2026-05-20 00:00:00',
        '2026-12-31 00:00:00',
        4
    );

-- Single Skill Jobs
-- INSERT INTO job_skills (job_id, skill_id) VALUES
--   (1, 1),   -- Carpentry
--   (2, 9),   -- Gardening
--   (3, 20),  -- Cooking
--   (4, 26),  -- IT Support
--   (5, 33);  -- Community Outreach
-- Multi-Skill Jobs
INSERT INTO
    job_skills (job_id, skill_id)
VALUES
    (1, 1),
    (1, 3),
    (1, 8),
    (1, 18),
    (2, 9),
    (2, 10),
    (2, 13),
    (2, 14),
    (3, 20),
    (3, 21),
    (3, 22),
    (3, 24),
    (4, 26),
    (4, 27),
    (4, 28),
    (4, 29),
    (5, 33),
    (5, 31),
    (5, 32),
    (5, 34),
    (6, 12),
    (6, 17),
    (6, 33),
    (7, 13),
    (7, 9),
    (7, 10),
    (7, 18),
    (8, 2),
    (8, 3),
    (8, 8),
    (8, 18),
    (9, 3),
    (9, 6),
    (9, 8),
    (9, 18),
    (10, 27),
    (10, 26),
    (10, 28),
    (10, 33),
    (11, 28),
    (11, 26),
    (11, 31),
    (11, 33),
    (12, 34),
    (12, 33),
    (12, 32),
    (13, 18),
    (13, 3),
    (13, 6),
    (13, 1),
    (14, 22),
    (14, 23),
    (14, 19),
    (14, 18),
    (15, 23),
    (15, 33),
    (15, 32),
    (16, 24),
    (16, 25),
    (16, 33),
    (16, 30),
    (17, 33),
    (17, 25),
    (17, 30),
    (17, 24);


    -- u -> users, s -> skills, us -> user_skill
select u.name as name, s.skill from users as u
inner join user_skills as us on u.id = us.user_id
inner join skills as s on us.skill_id = s.id;

-- j -> jobs, s -> skills, us -> user_skill
select j.job_title as name, s.skill from jobs as j
inner join job_skills as js on j.id = js.job_id
inner join skills as s on js.skill_id = s.id;



-- all jobs from a project with their skill
select j.job_title, p.project_title, s.skill as js from jobs as j
inner join projects as p on j.project_id = p.id
inner join job_skills as js on j.id = js.job_id
inner join skills as s on js.skill_id = s.id;


select u.name as name, s.skill from users as u 
inner join user_skills as us on u.id = us.user_id
inner join skills as s on us.skill_id = s.id
where name = "Leo";


-- select j.job_title, u.name, s.skill from users as u
-- inner join user_skills as us on u.id = us.user_id
-- inner join job_skills as js on j.id = js.job_id;

select j.job_title, s.skill, u.name from jobs as j
inner join job_skills as js on j.id = js.job_id
inner join skills as s on s.id = js.skill_id
inner join user_skills as us on js.skill_id = us.skill_id
inner join users as u on us.user_id = u.id;


select j.job_title, s.skill, u.name from jobs as j
inner join job_skills as js on j.id = js.job_id
inner join skills as s on s.id = js.skill_id
inner join user_skills as us on js.skill_id = us.skill_id
inner join users as u on us.user_id = u.id;



SELECT
  j.id,
  j.job_title,
  j.status,
  j.area,
  u.id AS user_id,
  u.name,
  COUNT(DISTINCT js.skill_id) AS match_score
FROM jobs AS j
INNER JOIN job_skills AS js ON j.id = js.job_id
INNER JOIN user_skills AS us ON js.skill_id = us.skill_id
INNER JOIN users AS u ON us.user_id = u.id
WHERE u.id = 3
GROUP BY
  j.id, j.job_title, j.status, j.area, u.id, u.name
ORDER BY match_score DESC, j.id;
        

DELIMITER //
	CREATE PROCEDURE getJobRecommendations (
		IN userId INT
    )
       BEGIN
		SELECT
			  j.id,
			  j.job_title,
			  j.status,
			  j.area,
			  u.id AS user_id,
			  u.name,
			  COUNT(DISTINCT js.skill_id) AS match_score
			FROM jobs
	
			INNER JOIN job_skills as js on j.id = js.job_id
			INNER JOIN skills as s on s.id = js.skill_id
			INNER JOIN user_skills as us on js.skill_id = us.skill_id
            INNER JOIN users as u on us.user_id = u.id
            
		WHERE u.id = userId;
    
	END//



















SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS subscriptions;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS job_location;
DROP TABLE IF EXISTS job_requests;
DROP TABLE IF EXISTS user_jobs;
DROP TABLE IF EXISTS map_icons;
DROP TABLE IF EXISTS user_skills;
DROP TABLE IF EXISTS job_skills;
DROP TABLE IF EXISTS skills;
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS user_permissions;
DROP TABLE IF EXISTS community_requests;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS communities;

DROP PROCEDURE IF EXISTS getJobRecommendations;

SET FOREIGN_KEY_CHECKS = 1;


CREATE TABLE communities (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    area VARCHAR(100) NOT NULL,
    description VARCHAR(500) NOT NULL,
    profile_picture VARCHAR(1000),
    lat DECIMAL(9,6) NULL,
    lng DECIMAL(9,6) NULL

);

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    type VARCHAR(12) NOT NULL,
    work_area VARCHAR(100) NULL, 
    specialism VARCHAR(100) NULL,
    rating INT NULL, 
    private_key BLOB NULL,
    public_key BLOB NULL,
    profile_picture VARCHAR(1000) NULL,
    verified BOOLEAN NULL,
    verification_accuracy DECIMAL(5,2) NULL,
    community_id INT NULL,
    FOREIGN KEY (community_id) REFERENCES communities(id)
);

CREATE TABLE community_requests (
    id INT PRIMARY KEY AUTO_INCREMENT,
    status VARCHAR(1) NOT NULL,
    created_date DATE NOT NULL,
    confirmed_date DATE,
    user_id INT NOT NULL,
    community_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (community_id) REFERENCES communities(id)
);

CREATE TABLE user_permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    accepted_terms BOOLEAN NOT NULL,
    accepted_gdpr BOOLEAN NOT NULL,
    accepted_health_safety BOOLEAN NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE messages (
    id INT PRIMARY KEY AUTO_INCREMENT,
    content VARCHAR(1000) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (receiver_id) REFERENCES users(id)
);

CREATE TABLE projects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_title VARCHAR(100) NOT NULL,
    project_description VARCHAR(1000) NOT NULL,
    project_type VARCHAR(20) NOT NULL,
    status VARCHAR(3) NOT NULL DEFAULT 'D',
    number_of_helpers INT NOT NULL,
    start_date DATETIME,
    end_date DATETIME,
    community_id INT NOT NULL,
    FOREIGN KEY (community_id) REFERENCES communities(id)
);

CREATE TABLE jobs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    job_title VARCHAR(100) NOT NULL,
    job_description VARCHAR(500) NOT NULL,
    short_title VARCHAR(50),
    short_type VARCHAR(20),
    status VARCHAR(3) NOT NULL DEFAULT 'D',
    area VARCHAR(100) NOT NULL,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    start_date DATETIME,
    end_date DATETIME,
    project_id INT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

CREATE TABLE skills (
    id INT PRIMARY KEY AUTO_INCREMENT,
    skill VARCHAR(100) NOT NULL
);

CREATE TABLE job_skills (
    id INT PRIMARY KEY AUTO_INCREMENT,
    job_id INT NOT NULL,
    skill_id INT NOT NULL,
    FOREIGN KEY (job_id) REFERENCES jobs (id),
    FOREIGN KEY (skill_id) REFERENCES skills (id),
    UNIQUE (job_id, skill_id)
);

CREATE TABLE user_skills (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    skill_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (skill_id) REFERENCES skills (id)
);

CREATE TABLE map_icons (
    id INT PRIMARY KEY AUTO_INCREMENT,
    icon_url VARCHAR(200) NOT NULL,
    description VARCHAR(100) NOT NULL
);


CREATE TABLE user_jobs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    job_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (job_id) REFERENCES jobs(id)
);


CREATE TABLE job_requests (
    id INT PRIMARY KEY AUTO_INCREMENT,
    status VARCHAR(1) NOT NULL,
    created_date DATE NOT NULL,
    confirmed_date DATE,
    user_id INT NOT NULL,
    job_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (job_id) REFERENCES jobs(id)
);

CREATE TABLE job_location (
    id INT PRIMARY KEY AUTO_INCREMENT,
    lat DECIMAL(9,6) NOT NULL,
    lng DECIMAL(9,6) NOT NULL,
    job_id INT NOT NULL, 
    icon_id INT NOT NULL, 
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    FOREIGN KEY (icon_id) REFERENCES map_icons(id)
);

CREATE TABLE reviews (
    id INT PRIMARY KEY AUTO_INCREMENT,
    star_rating INT NOT NULL,
    review VARCHAR(500) NOT NULL,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    reviewer_id INT NOT NULL, 
    helper_id INT NOT NULL, 
    job_id INT NOT NULL,
    FOREIGN KEY (reviewer_id) REFERENCES users(id),
    FOREIGN KEY (helper_id) REFERENCES users(id),
    FOREIGN KEY (job_id) REFERENCES jobs(id)
);

CREATE TABLE subscriptions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    subscription_json VARCHAR(1000) NOT NULL
);



INSERT INTO communities (id, name, area, description, profile_picture, lat, lng)
VALUES
(1, 'Mens Shed Dundalk', 'Dundalk, Co.Louth', 'Mens Shed Dundalk provides a supportive environment for men to connect, share skills, and work on projects that benefit the local community.', '/static/images/community_image.png', 54.00593713587985, -6.395891788845103),
(2, 'Ardee Tidy Towns', 'Ardee, Co.Louth', 'Ardee Tidy Towns is dedicated to enhancing the beauty and cleanliness of Ardee through community involvement and sustainable practices.', NULL, 53.857960295207874, -6.540589690340175),
(3, 'Dundalk Tidy Towns', 'Dundalk, Co.Louth', 'Dundalk Tidy Towns is committed to creating a cleaner and greener environment for the people of Dundalk. Working with the local community and businesses alike to improve the aesthetic appearance of the town.', NULL, 54.004786472339056, -6.401217344308929);

INSERT INTO users (id, name, email, password, type, work_area, specialism, rating, private_key, public_key, profile_picture, verified, verification_accuracy, community_id)
VALUES 
(1, 'Leo Fitz', 'leofitz@gmail.com', 'scrypt:32768:8:1$HGyAqImmePvDxpyt$a5f9fba484d19c468001450f5eff5721110daa6d042d0a5930cac070cb7783f34d1c7e0e87396d0a008381f2aba2bd3e09898e77b8e90f279a6a121d8c810fdc', 'helper', 'Dundalk', 'Electrician', 4, NULL, NULL, NULL, FALSE, 0.0, NULL),
(2, 'Ryan O''Hare', 'ryanohare@gmail.com', 'scrypt:32768:8:1$HGyAqImmePvDxpyt$a5f9fba484d19c468001450f5eff5721110daa6d042d0a5930cac070cb7783f34d1c7e0e87396d0a008381f2aba2bd3e09898e77b8e90f279a6a121d8c810fdc', 'helper', 'Crossmaglen', 'Contractor', 3, NULL, NULL, '/static/images/user_image_2.png', FALSE, 0.0, 1),
(3, 'John Johnson', 'johnjohnson@gmail.com', 'scrypt:32768:8:1$HGyAqImmePvDxpyt$a5f9fba484d19c468001450f5eff5721110daa6d042d0a5930cac070cb7783f34d1c7e0e87396d0a008381f2aba2bd3e09898e77b8e90f279a6a121d8c810fdc', 'chairperson', 'Dundalk', 'Chairperson', 0, NULL, NULL, NULL, FALSE, 0.0, 1),
(4, 'Daisy Johnson', 'daisyjohnson@gmail.com', 'scrypt:32768:8:1$HGyAqImmePvDxpyt$a5f9fba484d19c468001450f5eff5721110daa6d042d0a5930cac070cb7783f34d1c7e0e87396d0a008381f2aba2bd3e09898e77b8e90f279a6a121d8c810fdc', 'helper', 'Dundalk', 'Local Helper', 4, NULL, NULL, NULL, FALSE, 0.0, 1),
(5, 'Jemma Simmons', 'jemmasimmons@gmail.com', 'scrypt:32768:8:1$HGyAqImmePvDxpyt$a5f9fba484d19c468001450f5eff5721110daa6d042d0a5930cac070cb7783f34d1c7e0e87396d0a008381f2aba2bd3e09898e77b8e90f279a6a121d8c810fdc', 'helper', 'Ardee', 'Local Helper', 3, NULL, NULL, NULL, FALSE, 0.0, 2);


INSERT INTO user_permissions (id, accepted_terms, accepted_gdpr, accepted_health_safety, user_id)
VALUES
(1, FALSE, FALSE, FALSE, 5),
(2, FALSE, FALSE, FALSE, 4),
(3, FALSE, FALSE, FALSE, 3),
(4, FALSE, FALSE, FALSE, 2),
(5, FALSE, FALSE, FALSE, 1);

INSERT INTO messages (id, content, timestamp, sender_id, receiver_id)
VALUES
(1, 'Hi, I would love to work with Tidy Towns. What projects are available?', CURRENT_TIMESTAMP, 2, 1),
(2,'That''s great Ryan. We have lots of projects waiting to kick off, is there anything in particular you would be interested in?', CURRENT_TIMESTAMP, 1, 2);

INSERT INTO projects (id, project_title, project_description, project_type, number_of_helpers, start_date, end_date, community_id)
VALUES
(1, 'Build new community park', 'Building a new park for the community of Dundalk', 'Environment', 5, '2026-01-08', '2026-07-21', 1),
(2, 'Build new Social club', 'Building a social space for the local community of Dundalk', 'social_and_events', 6, '2026-07-01', '2026-12-19', 1),
(3, 'Food drive', 'Help distributing food to those in need in Dundalk', 'Environment', 9, '2026-01-25', '2027-01-25', 1),
(4, 'Build community play park', 'Building a new play park for the community of Monaghan', 'Environment', 5, '2026-01-08', '2026-07-21', 2),
(5, 'Community Garden Restoration', 'Restore unused land into a community vegetable and flower garden.', 'environment', 6, '2026-03-01', '2026-06-01', 3),
(6, 'Repair Community Hall Roof', 'Repair damaged roof panels on the local community hall.', 'construction', 4, '2026-03-10', '2026-03-20', 1),
(7, 'Town Clean Up Initiative', 'Organised town clean up including litter collection and recycling.', 'environment', 10, '2026-04-05', '2026-04-06', 2),
(8, 'Build Outdoor Seating Area', 'Construct a wooden seating and social area for local residents.', 'construction', 5, '2026-04-15', '2026-05-20', 1);

INSERT INTO jobs (id, job_title, job_description, short_title, short_type, status, area, created_date, start_date, end_date, project_id)
VALUES
(1, 'Install park benches and picnic tables','Help assemble and install benches/tables in the new park. Basic tools helpful. Outdoor work.','Benches install', 'environment', 'A', 'Dundalk', '2026-01-10 10:00:00', '2026-02-01 09:00:00', '2026-02-01 13:00:00',1),
(2, 'Repair and paint perimeter fencing','Sand, repair and repaint park fencing to improve safety and appearance. PPE recommended.','Fence paint', 'general_maintenance', 'A','Dundalk', '2026-01-11 14:00:00', '2026-02-05 10:00:00', '2026-02-05 16:00:00',1),
(3, 'Outdoor lighting check and minor fixes','Check existing lighting points around the park area and complete minor electrical fixes where safe.', 'Lighting', 'safety', 'D', 'Dundalk', '2026-01-12 09:30:00', '2026-02-10 10:00:00', '2026-02-10 12:30:00',1),
(4, 'Build a small raised planter bed','Construct a raised wooden planter bed for flowers near the entrance. Carpentry help needed.','Planter bed', 'construction', 'A','Dundalk', '2026-01-13 12:00:00', '2026-02-12 09:00:00', '2026-02-12 14:00:00',1),
(5, 'Assemble raised garden beds', 'Help construct and install wooden raised beds for the new community garden.', 'Garden beds', 'construction', 'A', 'Dundalk', CURRENT_TIMESTAMP, '2026-03-10 09:00:00', '2026-03-10 14:00:00', 5),
(6, 'Plant flowers and vegetables', 'Assist with planting vegetables and flowers in the restored garden.', 'Planting', 'environment', 'A', 'Dundalk', CURRENT_TIMESTAMP, '2026-03-15 10:00:00', '2026-03-15 13:00:00', 5),
(7, 'Repair roof panels', 'Replace damaged roof panels and secure new fittings on the community hall.', 'Roof repair', 'construction', 'A', 'Dundalk', CURRENT_TIMESTAMP, '2026-03-12 09:00:00', '2026-03-12 16:00:00', 6),
(8, 'Electrical lighting inspection', 'Inspect and repair outdoor lighting around the hall entrance.', 'Lighting check', 'safety', 'A', 'Dundalk', CURRENT_TIMESTAMP, '2026-03-13 10:00:00', '2026-03-13 12:00:00', 6),
(9, 'Collect litter and recycling', 'Walk through assigned streets collecting litter and recyclables.', 'Town clean up', 'environment', 'A', 'Ardee', CURRENT_TIMESTAMP, '2026-04-05 09:00:00', '2026-04-05 13:00:00', 7),
(10, 'Sort collected waste', 'Help organise waste into recycling and disposal categories.', 'Waste sorting', 'environment', 'A', 'Ardee', CURRENT_TIMESTAMP, '2026-04-05 13:30:00', '2026-04-05 16:00:00', 7),
(11, 'Build wooden seating benches', 'Construct wooden benches for the outdoor seating area.', 'Bench build', 'construction', 'A', 'Dundalk', CURRENT_TIMESTAMP, '2026-04-20 09:00:00', '2026-04-20 15:00:00', 8),
(12, 'Sand and treat wooden surfaces', 'Sand and weatherproof newly built seating structures.', 'Wood treatment', 'general_maintenance', 'A', 'Dundalk', CURRENT_TIMESTAMP, '2026-04-21 10:00:00', '2026-04-21 14:00:00', 8);

INSERT INTO skills (id, skill)
VALUES
(1, 'Carpentry'),
(2, 'Painting'),
(3, 'General DIY'),
(4, 'Plumbing'),
(5, 'Electrical Repair'),
(6, 'Furniture Repair'),
(7, 'Bike Repair'),
(8, 'Tool Maintenance'),
(9, 'Gardening'),
(10, 'Landscaping'),
(11, 'Tree Planting'),
(12, 'Litter Picking'),
(13, 'Grass Cutting'),
(14, 'Hedge Trimming'),
(15, 'Community Garden Work'),
(16, 'House Cleaning'),
(17, 'Community Cleaning'),
(18, 'Basic Maintenance'),
(19, 'Furniture Moving'),
(20, 'Cooking'),
(21, 'Baking'),
(22, 'Event Setup'),
(23, 'Event Stewarding'),
(24, 'Fundraising Support'),
(25, 'Event Organisation'),
(26, 'IT Support'),
(27, 'Smartphone Help'),
(28, 'Computer Basics'),
(29, 'Website Help'),
(30, 'Music Teaching'),
(31, 'Tutoring'),
(32, 'Youth Support'),
(33, 'Community Outreach'),
(34, 'Companionship Visits');

INSERT INTO user_skills (id, user_id, skill_id)
VALUES
-- Leo Fitz
(1, 1, 1),
(2, 1, 2),
(3, 1, 3),
(4, 1, 6),
(5, 1, 8),
-- Ryan O'Hare
(6, 2, 9),
(7, 2, 10),
(8, 2, 12),
(9, 2, 13),
(10, 2, 14),
-- John Johnson
(11, 3, 20),
(12, 3, 21),
(13, 3, 22),
(14, 3, 24),
(15, 3, 25),
-- Daisy Johnson
(16, 4, 26),
(17, 4, 27),
(18, 4, 28),
(19, 4, 29),
(20, 4, 30),
-- Jemma Simmons
(21, 5, 33),
(22, 5, 32),
(23, 5, 31),
(24, 5, 34),
(25, 5, 23);

INSERT INTO job_skills (job_id, skill_id)
VALUES
(1, 1),
(1, 3),
(1, 8),
(1, 18),
(2, 2),
(2, 3),
(2, 8),
(2, 18),
(3, 5),
(3, 18),
(3, 3),
(4, 1),
(4, 3),
(4, 6),
(4, 8),
(5, 1),
(5, 3),
(5, 8),
(5, 15),
(6, 9),
(6, 10),
(6, 11),
(6, 15),
(7, 3),
(7, 18),
(7, 19),
(7, 5),
(8, 5),
(8, 18),
(8, 3),
(9, 12),
(9, 17),
(9, 33),
(10, 12),
(10, 17),
(10, 18),
(11, 1),
(11, 3),
(11, 6),
(11, 8),
(12, 2),
(12, 3),
(12, 8),
(12, 18);

INSERT INTO user_jobs (id, user_id, job_id)
VALUES 
(1, 1, 1),
(2, 2, 1),
(3, 1, 2),
(4, 2, 3),
(5, 2, 4),
(6, 3, 4),
(7, 1, 8),  
(8, 1, 7), 
(9, 2, 5),  
(10, 2, 11),
(11, 4, 6), 
(12, 4, 9), 
(13, 5, 9), 
(14, 5, 10);

INSERT INTO map_icons (id, icon_url, description)
VALUES
(1, '', '');

INSERT INTO job_location (id, lat, lng, job_id, icon_id)
VALUES
(1, 54.0023, -6.4037, 1, 1),  
(2, 54.0015, -6.4055, 2, 1),  
(3, 54.0030, -6.4020, 3, 1),  
(4, 54.0045, -6.3985, 4, 1),
(5, 54.0065, -6.4100, 5, 1),
(6, 54.0078, -6.3995, 6, 1),
(7, 54.0008, -6.4030, 7, 1),
(8, 53.9985, -6.3950, 8, 1),
(9, 53.8590, -6.5400, 9, 1),
(10, 53.8605, -6.5380, 10, 1),
(11, 53.9970, -6.3900, 11, 1),
(12, 54.0005, -6.4105, 12, 1); 

INSERT INTO reviews (id, star_rating, review, created_date, reviewer_id, helper_id, job_id)
VALUES
(1, 5, 'Ryan was fantastic! He helped me with my home repairs and was very professional.', CURRENT_TIMESTAMP, 3, 1, 1),
(2, 4, 'Leo did a great job with the electrical work in the park. Highly recommend!', CURRENT_TIMESTAMP, 4, 2, 3),
(3, 5, 'Bridget was very helpful and friendly while assisting with the park setup.', CURRENT_TIMESTAMP, 5, 3, 2);







DELIMITER //
	CREATE PROCEDURE getJobRecommendations (
		IN userId INT
    )
       BEGIN
        SELECT
            j.*,
            u.id AS user_id,
            u.name,
            COUNT(DISTINCT js.skill_id) AS match_score
        FROM jobs AS j
            INNER JOIN job_skills AS js ON j.id = js.job_id
            INNER JOIN user_skills AS us ON js.skill_id = us.skill_id
            INNER JOIN users AS u ON us.user_id = u.id
        WHERE
            u.id = userId
        GROUP BY
            j.id,
            j.job_title,
            j.job_description,
            j.short_title,
            j.short_type,
            j.status,
            j.area,
            j.created_date,
            j.start_date,
            j.end_date,
            j.project_id,
            u.id
        ORDER BY
            match_score DESC,
            j.id;
	END//

DELIMITER ;
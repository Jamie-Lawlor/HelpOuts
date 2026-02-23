SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS job_location;
DROP TABLE IF EXISTS user_jobs;
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS user_permissions;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS map_icons;
DROP TABLE IF EXISTS communities;
DROP TABLE IF EXISTS subscriptions;

SET FOREIGN_KEY_CHECKS = 1;


CREATE TABLE communities (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    area VARCHAR(100) NOT NULL,
    description VARCHAR(500) NOT NULL,
    profile_picture VARCHAR(1000)
);

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    type VARCHAR(15) NOT NULL,
    work_area VARCHAR(100), 
    specialism VARCHAR(100),
    skills VARCHAR(200),
    rating INT, 
    private_key BLOB,
    public_key BLOB,
    profile_picture VARCHAR(1000),
    verified BOOLEAN DEFAULT FALSE,
    verification_accuracy DECIMAL(5,2),
    community_id INT,
    FOREIGN KEY (community_id) REFERENCES communities(id)
);

CREATE TABLE subscriptions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    subscription_json VARCHAR(1000) NOT NULL
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

CREATE TABLE user_jobs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    job_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (job_id) REFERENCES jobs(id)
);

CREATE TABLE map_icons (
    id INT PRIMARY KEY AUTO_INCREMENT,
    icon_url VARCHAR(200) NOT NULL,
    description VARCHAR(100) NOT NULL
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




INSERT INTO communities (id, name, area, description, profile_picture)
VALUES
(1, 'Mens Shed Dundalk', 'Dundalk, Co.Louth', 'Mens Shed Dundalk provides a supportive environment for men to connect, share skills, and work on projects that benefit the local community.', '/static/images/community_image.png'),
(2, 'Ardee Tidy Towns', 'Ardee, Co.Louth', 'Ardee Tidy Towns is dedicated to enhancing the beauty and cleanliness of Ardee through community involvement and sustainable practices.', NULL),
(3, 'Dundalk Tidy Towns', 'Dundalk, Co.Louth', 'Dundalk Tidy Towns is committed to creating a cleaner and greener environment for the people of Dundalk. Working with the local community and businesses alike to improve the aesthetic appearance of the town.', NULL);

INSERT INTO users (id, name, email, password, type, work_area, specialism, skills, rating, private_key, public_key, profile_picture, verified, verification_accuracy, community_id)
VALUES 
(1, 'Leo Fitz', 'leofitz@gmail.com', 'Test1234567!', 'helper', 'Dundalk', 'Electrician', 'Carpentry, Home Maintenance, General Maintenance,', 4, NULL, NULL, NULL, FALSE, 0.0, 1),
(2, 'Ryan O''Hare', 'ryanohare@gmail.com', 'scrypt:32768:8:1$iRcIx60EXd2ZTtdh$5ae8152f4e262d7fa18af26847fe3d34e25c6c733f48751dab25a3dcc97fa1c86f7116ccbc7dacde12a98ae45ff4dd0f947c4c4a3a49627c9f01916d78cac029', 'helper', 'Crossmaglen', 'Contractor', 'Carpentry, Home Maintenance, General Maintenance,', 3, NULL, NULL, '/static/images/user_image_2.png', FALSE, 0.0, 1),
(3, 'Bridget Muckian', 'bridgetm1@gmail.com', 'Test1234567!', 'helper', 'Crossmaglen', 'Local Helper', '', 0, NULL, NULL, NULL, FALSE, 0.0, 1),
(4, 'Daisy Johnson', 'daisyjohnson@gmail.com', 'Test1234567!', 'helper', 'Dundalk', 'Local Helper', '', 4, NULL, NULL, NULL, FALSE, 0.0, 1),
(5, 'Jemma Simmons', 'jemmasimmons@gmail.com', 'Test1234567!', 'helper', 'Ardee', 'Local Helper', '', 3, NULL, NULL, NULL, FALSE, 0.0, 2);


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
(4, 'Build community play park', 'Building a new play park for the community of Monaghan', 'Environment', 5, '2026-01-08', '2026-07-21', 2);

INSERT INTO jobs (id, job_title, job_description, short_title, short_type, status, area, created_date, start_date, end_date, project_id)
VALUES
(1, 'Install park benches and picnic tables','Help assemble and install benches/tables in the new park. Basic tools helpful. Outdoor work.','Benches install', 'environment', 'A', 'Dundalk', '2026-01-10 10:00:00', '2026-02-01 09:00:00', '2026-02-01 13:00:00',1),
(2, 'Repair and paint perimeter fencing','Sand, repair and repaint park fencing to improve safety and appearance. PPE recommended.','Fence paint', 'maintenance', 'A','Dundalk', '2026-01-11 14:00:00', '2026-02-05 10:00:00', '2026-02-05 16:00:00',1),
(3, 'Outdoor lighting check and minor fixes','Check existing lighting points around the park area and complete minor electrical fixes where safe.', 'Lighting', 'electrical', 'D', 'Dundalk', '2026-01-12 09:30:00', '2026-02-10 10:00:00', '2026-02-10 12:30:00',1),
(4, 'Build a small raised planter bed','Construct a raised wooden planter bed for flowers near the entrance. Carpentry help needed.','Planter bed', 'carpentry', 'A','Dundalk', '2026-01-13 12:00:00', '2026-02-12 09:00:00', '2026-02-12 14:00:00',1);

INSERT INTO user_jobs (id, user_id, job_id)
VALUES 
(1, 1, 1),
(2, 2, 1),
(3, 1, 2),
(4, 2, 3),
(5, 2, 4),
(6, 3, 4);

INSERT INTO map_icons (id, icon_url, description)
VALUES
(1, '', '');

INSERT INTO job_location (id, lat, lng, job_id, icon_id)
VALUES
(1, 54.002345, -6.404321, 1, 1),
(2, 54.002567, -6.405678, 2, 1),
(3, 54.002789, -6.406789, 3, 1),
(4, 54.003012, -6.407890, 4, 1);

INSERT INTO reviews (id, star_rating, review, created_date, reviewer_id, helper_id, job_id)
VALUES
(1, 5, 'Ryan was fantastic! He helped me with my home repairs and was very professional.', CURRENT_TIMESTAMP, 3, 1, 1),
(2, 4, 'Leo did a great job with the electrical work in the park. Highly recommend!', CURRENT_TIMESTAMP, 4, 2, 3),
(3, 5, 'Bridget was very helpful and friendly while assisting with the park setup.', CURRENT_TIMESTAMP, 5, 3, 2);
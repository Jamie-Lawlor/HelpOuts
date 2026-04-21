SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS logs;
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
    lng DECIMAL(9,6) NULL,
    private_key BLOB NULL,
    public_key BLOB NULL

);

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    type VARCHAR(12) NOT NULL,
    work_area VARCHAR(100) NULL, 
    specialism VARCHAR(100) NULL,
    availability VARCHAR(18) NULL,
    experience VARCHAR(4000) NULL,
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
    start_date DATE,
    end_date DATE,
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
    number_of_helpers INT NOT NULL,
    area VARCHAR(100) NOT NULL,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    start_date DATE,
    end_date DATE,
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

CREATE TABLE logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    action VARCHAR(250) NOT NULL,
    target VARCHAR(250) NOT NULL,
    time_stamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);



INSERT INTO communities (id, name, area, description, profile_picture, lat, lng, private_key, public_key)
VALUES
(1, 'Mens Shed Dundalk', 'Dundalk, Co.Louth', 'Mens Shed Dundalk provides a supportive environment for men to connect, share skills, and work on projects that benefit the local community.', '/static/images/community_image.png', 54.00593713587985, -6.395891788845103, NULL, NULL),
(2, 'Ardee Tidy Towns', 'Ardee, Co.Louth', 'Ardee Tidy Towns is dedicated to enhancing the beauty and cleanliness of Ardee through community involvement and sustainable practices.', NULL, 53.857960295207874, -6.540589690340175, NULL, NULL),
(3, 'Dundalk Tidy Towns', 'Dundalk, Co.Louth', 'Dundalk Tidy Towns is committed to creating a cleaner and greener environment for the people of Dundalk. Working with the local community and businesses alike to improve the aesthetic appearance of the town.', NULL, 54.004786472339056, -6.401217344308929, NULL, NULL),
(4, 'Pieta', 'Monaghan Town', 'Since then we have seen and helped over 70,000 people in suicidal distress or engaging in self-harm. We now operate 20 locations across Ireland. Pieta now employs over 300 therapists and support staff, and the demand for our service is increasing.', '/static/images/pieta.png', 54.287256, -6.975038, NULL, NULL),
(5, 'Mullaghbawn Football Club', 'Mullaghbawn, Co. Armagh', '', NULL, 54.109034822153404, -6.487326525650774, NULL, NULL);

INSERT INTO users (id, name, email, password, type, work_area, specialism, rating, private_key, public_key, profile_picture, verified, verification_accuracy, community_id)
VALUES 
(1, 'Leo Fitz', 'leofitz@gmail.com', 'scrypt:32768:8:1$HGyAqImmePvDxpyt$a5f9fba484d19c468001450f5eff5721110daa6d042d0a5930cac070cb7783f34d1c7e0e87396d0a008381f2aba2bd3e09898e77b8e90f279a6a121d8c810fdc', 'helper', 'Dundalk', 'Electrician', 4, NULL, NULL,  NULL, FALSE, 0.0, 5),
(2, 'Ryan O''Hare', 'ryanohare@gmail.com', 'scrypt:32768:8:1$HGyAqImmePvDxpyt$a5f9fba484d19c468001450f5eff5721110daa6d042d0a5930cac070cb7783f34d1c7e0e87396d0a008381f2aba2bd3e09898e77b8e90f279a6a121d8c810fdc', 'helper', 'Crossmaglen', 'Contractor', 3, NULL, NULL,  '/static/images/user_image_2.png', FALSE, 0.0, 5),
(3, 'John Johnson', 'johnjohnson@gmail.com', 'scrypt:32768:8:1$HGyAqImmePvDxpyt$a5f9fba484d19c468001450f5eff5721110daa6d042d0a5930cac070cb7783f34d1c7e0e87396d0a008381f2aba2bd3e09898e77b8e90f279a6a121d8c810fdc', 'helper', 'Dundalk', 'Chairperson', 0, NULL, NULL,  NULL, FALSE, 0.0, 5),
(4, 'Daisy Johnson', 'daisyjohnson@gmail.com', 'scrypt:32768:8:1$HGyAqImmePvDxpyt$a5f9fba484d19c468001450f5eff5721110daa6d042d0a5930cac070cb7783f34d1c7e0e87396d0a008381f2aba2bd3e09898e77b8e90f279a6a121d8c810fdc', 'helper', 'Dundalk', 'Local Helper', 4, NULL, NULL,  NULL, FALSE, 0.0, 5),
(5, 'Jemma Simmons', 'jemmasimmons@gmail.com', 'scrypt:32768:8:1$HGyAqImmePvDxpyt$a5f9fba484d19c468001450f5eff5721110daa6d042d0a5930cac070cb7783f34d1c7e0e87396d0a008381f2aba2bd3e09898e77b8e90f279a6a121d8c810fdc', 'helper', 'Ardee', 'Local Helper', 3, NULL, NULL,  NULL, FALSE, 0.0, 5),
(6, 'Kerrie McLoughlin', 'kerriemcloughin@gmail.com', 'scrypt:32768:8:1$HGyAqImmePvDxpyt$a5f9fba484d19c468001450f5eff5721110daa6d042d0a5930cac070cb7783f34d1c7e0e87396d0a008381f2aba2bd3e09898e77b8e90f279a6a121d8c810fdc', 'chairperson', 'Monaghan', 'Chairperson', 0, '-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----', '-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAvPuP9ypp9SDyHnkKM+wM
vN8L8GMN65lPIXvibz3oubRX7ZY0UwBXvFzilUitXnAFbljd5MYJYLAlS1r2l4/j
hdf/Ag5cZdZApOmai5FpvnjnTsh6AAjn1pU8FrMbngvqQY5ddpIv18MOHB8VBnUi
wKTQjdp4t5EnlW2k9FuH8UqKE4lARs3bgz5slJlmsdPrcNLXJOyrQ+TvBWN6ia8S
IoPpaqvThT1x+PvYHSsQ/c6dWYKxi+HnOWY98mPa7VJqznNDsVkjVVBqxRP/kt+l
1e+F77dPOF+vhzEuBK7ysZ3TnZFTRkUfF/MIUX2CS1Osr66y41TETzL99S2EM1/R
28K3tTENY+bJHaAFOi2LV/iSmT2ljzYCU1Jtym1JbBMv7L9NRkU282T8ACVs/uJU
ecO3E32LGXf+fTmS/gF465gh3RLmqeN8HMV5culsJ3yE9zCHodI0S+05lkomVftU
3okVWdjQ7tFUME9bmUIdsH5+tSCfbsEA8SMUKD6RYbxYpLhPtEjsIJFFickI77zL
Fap0VqqwT3oM6nKPiG/wlI2jchWCjWkdPkabMIVh3ohpa6AbRYPRHXNhJTiwRWIz
Kta2a6OeCmdGOg2ziteK1AcvDpDhb1z/Oalaou3oS1OiFxw8UQeZN7oWgU/r6dow
Ru6p6aPuXT8FMQ1wvM72hBcCAwEAAQ==
-----END PUBLIC KEY-----', NULL, FALSE, 0.0, 5),
(7, 'Steven Rodgers', 'stevenrodgers@gmail.com', 'scrypt:32768:8:1$HGyAqImmePvDxpyt$a5f9fba484d19c468001450f5eff5721110daa6d042d0a5930cac070cb7783f34d1c7e0e87396d0a008381f2aba2bd3e09898e77b8e90f279a6a121d8c810fdc', 'helper', 'Monaghan', 'Local Helper', 0, '-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----', '-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA8XC+RK1WoF2j027ctd6w
SGBzoPGZCIaZo/po9pU3g3StVyFFpq6QxV6UOG0MDyVkEIxt8Pw5DyRmONFsSl6e
4oRH6VnFvl7L7PMOnktHijOug5+nMU/Dj/psVYrqwuncJPaPgN7c5TQEzUOwZUFx
gwKx2F7oyIljLv0Zn7C05FCrh64q8AKBZ7aZ7GKyv9AXlq5yHqsvZWu5orhp87oT
uQ3ltcuwciZUk5QJDPwBKK6Vvde0y+Fv9rWC27HU2ohY4ayHai7jvQBvjTfquVIa
Es2W/PeuZT8eFDwXElGPuddw3AWOx6CCQljwglPYi+3XmwR9BKrWqqlhI3p1McQ+
dz7a+NIZwkhNYNF86cf4SkZuw1Ufc3nqaaoUyGdYcpFNdg8+d2bF/y7PBOL+90QB
dSmfgTeA9p/1JJjgriX5PKwzKiKxHX6F8gz7uOTXUsPRMoXif2GpRfWs/xHu7YyT
ItzJebUzU5APSDbpvkwA6BXsMVWvDHiWG691DShtkSzuqggUVAk7SKJg7tjuVudm
8fNiy1x5r3Z0bhPbdOjFnmWX5PPztIG+9TqjOG3x3hRhUuWnAAjW2W+71FzSpwrt
psVm2HA68MuEXIzruKX0la0FpcgePTkDlvoDLR0Wx3VRH+pmHOmQN/Td1qSkFNZD
9nCaY/1ORcKDu19M0OnuPPsCAwEAAQ==
-----END PUBLIC KEY-----', '/static/images/steven_rodgers.png', FALSE, 0.0, 5);

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

INSERT INTO projects (id, project_title, project_description, project_type, start_date, end_date, community_id)
VALUES
(1, 'Build new community park', 'Building a new park for the community of Dundalk', 'Environment', '2026-01-08', '2026-07-21', 1),
(2, 'Build new Social club', 'Building a social space for the local community of Dundalk', 'social_and_events', '2026-07-01', '2026-12-19', 1),
(3, 'Food drive', 'Help distributing food to those in need in Dundalk', 'Environment', '2026-01-25', '2027-01-25', 1),
(4, 'Build community play park', 'Building a new play park for the community of Monaghan', 'Environment', '2026-01-08', '2026-07-21', 2),
(5, 'Community Garden Restoration', 'Restore unused land into a community vegetable and flower garden.', 'environment', '2026-03-01', '2026-06-01', 3),
(6, 'Repair Community Hall Roof', 'Repair damaged roof panels on the local community hall.', 'construction', '2026-03-10', '2026-03-20', 1),
(7, 'Town Clean Up Initiative', 'Organised town clean up including litter collection and recycling.', 'environment', '2026-04-05', '2026-04-06', 2),
(8, 'Build Outdoor Seating Area', 'Construct a wooden seating and social area for local residents.', 'construction', '2026-04-15', '2026-05-20', 1),
(9, 'Darkness into light Monaghan', 'Darkness Into Light 2026, is Pieta’s biggest fundraiser, the 5km walk will take place at 4:15 a.m. on Saturday, 9th of May, 2026. The funds raised through Darkness Into Light supports Pieta’s lifesaving free services to people in your community that have been affected by suicide or self-harm. This inspiring event also symbolises hope, as communities come together to support mental health, suicide and self-harm prevention.', 'social_and_events', '2026-04-16', '2026-05-09', 4);

INSERT INTO jobs (id, job_title, job_description, short_title, short_type, status, number_of_helpers, area, created_date, start_date, end_date, project_id)
VALUES
(1, 'Install park benches and picnic tables','Help assemble and install benches/tables in the new park. Basic tools helpful. Outdoor work.','Benches install', 'environment', 'A', 5, 'Dundalk', CURRENT_TIMESTAMP, '2026-02-01', '2026-02-01',1),
(2, 'Repair and paint perimeter fencing','Sand, repair and repaint park fencing to improve safety and appearance. PPE recommended.','Fence paint', 'general_maintenance', 'A', 6, 'Dundalk', CURRENT_TIMESTAMP, '2026-02-05', '2026-02-05',1),
(3, 'Outdoor lighting check and minor fixes','Check existing lighting points around the park area and complete minor electrical fixes where safe.', 'Lighting', 'safety', 'D', 9, 'Dundalk', CURRENT_TIMESTAMP, '2026-02-10', '2026-02-10',1),
(4, 'Build a small raised planter bed','Construct a raised wooden planter bed for flowers near the entrance. Carpentry help needed.','Planter bed', 'construction', 'A', 5, 'Dundalk', CURRENT_TIMESTAMP, '2026-02-12', '2026-02-12',1),
(5, 'Assemble raised garden beds', 'Help construct and install wooden raised beds for the new community garden.', 'Garden beds', 'construction', 'A', 6, 'Dundalk', CURRENT_TIMESTAMP, '2026-03-10', '2026-03-10', 5),
(6, 'Plant flowers and vegetables', 'Assist with planting vegetables and flowers in the restored garden.', 'Planting', 'environment', 'A', 4, 'Dundalk', CURRENT_TIMESTAMP, '2026-03-15', '2026-03-15', 5),
(7, 'Repair roof panels', 'Replace damaged roof panels and secure new fittings on the community hall.', 'Roof repair', 'construction', 'A', 10, 'Dundalk', CURRENT_TIMESTAMP, '2026-03-12', '2026-03-12', 6),
(8, 'Electrical lighting inspection', 'Inspect and repair outdoor lighting around the hall entrance.', 'Lighting check', 'safety', 'A', 5, 'Dundalk', CURRENT_TIMESTAMP, '2026-03-13', '2026-03-13', 6),
(9, 'Collect litter and recycling', 'Walk through assigned streets collecting litter and recyclables.', 'Town clean up', 'environment', 'A', 10, 'Ardee', CURRENT_TIMESTAMP, '2026-04-05', '2026-04-05', 7),
(10, 'Sort collected waste', 'Help organise waste into recycling and disposal categories.', 'Waste sorting', 'environment', 'A', 1, 'Ardee', CURRENT_TIMESTAMP, '2026-04-05', '2026-04-05', 7),
(11, 'Build wooden seating benches', 'Construct wooden benches for the outdoor seating area.', 'Bench build', 'construction', 'A', 9, 'Dundalk', CURRENT_TIMESTAMP, '2026-04-20', '2026-04-20', 8),
(12, 'Sand and treat wooden surfaces', 'Sand and weatherproof newly built seating structures.', 'Wood treatment', 'general_maintenance', 'A', 3, 'Dundalk', CURRENT_TIMESTAMP, '2026-04-21', '2026-04-21', 8),
(13, 'Posting t-shirts','Organise the posting of t-shirts for people in Monaghan who have registered for the event','Posting t-shirts','social_and_events', 'NA', 4, 'Monaghan', CURRENT_TIMESTAMP, '2026-04-17', '2026-05-09', 9),
(14, 'Setup banners','Setting up banners for the event','Setup banners','environment', 'NA', 5, 'Monaghan', CURRENT_TIMESTAMP, '2026-05-09', '2026-05-09', 9),
(15,'Tea and coffee stand','Organise tea and coffee stand after the walk is finished','Tea & Coffee','social_and_events', 'NA', 6, 'Monaghan', CURRENT_TIMESTAMP, '2026-04-17', '2026-05-09', 9),
(16, 'Stewards','Give people directions to the correct path so no one gets lost along the walk','Stewards','social_and_events', 'NA', 7, 'Monaghan', CURRENT_TIMESTAMP, '2026-04-17', '2026-05-09', 9);

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
(25, 5, 23),
-- Steve Rodgers
(26, 7, 1),
(27, 7, 8),
(28, 7, 12),
(29, 7, 17),
(30, 7, 18),
(31, 7, 19),
(32, 7, 23);

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
(13, 24), 
(13, 33), 
(13, 18),
(14, 22), 
(14, 3),  
(14, 18),
(15, 20),
(15, 21),
(15, 24),
(16, 23), 
(16, 33),
(16, 32),
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
(12, 54.0005, -6.4105, 12, 1),
(13, 54.287261, -6.975044, 13, 1),
(14, 54.287261, -6.975044, 14, 1),
(15, 54.287261, -6.975044, 15, 1),
(16, 54.287261, -6.975044, 16, 1); 

INSERT INTO reviews (id, star_rating, review, created_date, reviewer_id, helper_id, job_id)
VALUES
(1, 5, 'Ryan was fantastic! He helped me with my home repairs and was very professional.', CURRENT_TIMESTAMP, 3, 1, 1),
(2, 4, 'Leo did a great job with the electrical work in the park. Highly recommend!', CURRENT_TIMESTAMP, 4, 2, 3),
(3, 5, 'Bridget was very helpful and friendly while assisting with the park setup.', CURRENT_TIMESTAMP, 5, 3, 2);







DELIMITER //
	CREATE PROCEDURE getJobRecommendations ( IN userId INT)
       BEGIN
        SELECT
            j.*,
            u.id AS user_id,
            u.name,
            COUNT(DISTINCT js.skill_id) AS match_score
        FROM jobs AS j
            INNER JOIN projects AS p ON j.project_id = p.id
            INNER JOIN job_skills AS js ON j.id = js.job_id
            INNER JOIN user_skills AS us ON js.skill_id = us.skill_id
            INNER JOIN users AS u ON us.user_id = u.id
        WHERE
            u.id = userId
            AND p.community_id = u.community_id
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
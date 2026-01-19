
INSERT INTO communities (id, name, area, description)
VALUES
(1, 'Dundalk Tidy Towns', 'Dundalk, Co.Louth', 'Dundalk Tidy Towns is committed to creating a cleaner and greener environment for the people of Dundalk. Working with the local community and businesses alike to improve the aesthetic appearance of the town. ');

INSERT INTO projects(community_id, project_title, project_description, project_type, number_of_helpers, start_date, end_date)
VALUES
(1, "Build new park", "Building a new park for the community of Dundalk", "Environment", 5, "2026-01-08", "2026-07-21");

INSERT INTO community_projects(project_id, community_id)
VALUES
(1, 1);

INSERT INTO users (name, email, password, type, work_area, specialism, skills, rating, community_id)
VALUES
("Bridget Muckian", "bridgetm1@gmail.com", "Test1234567!", "helpee", "Crossmaglen", "", "", 0, 1),
("Ryan O'Hare", "ryanohare@gmail.com", "Test1234567!", "helper", "Crossmaglen", "Contractor", " Carpentry, Home Maintenance, General Maintenance,", 3, 1);


INSERT INTO user_permissions (user_id, accepted_terms, accepted_gdpr, accepted_health_safety)
VALUES
(1, FALSE, FALSE, FALSE),
(2, FALSE, FALSE, FALSE);


INSERT INTO jobs (helper_id, helpee_id, project_id, status, area, job_title, job_description, short_title, short_type, created_date, start_date, end_date)
VALUES
(1, 2, 1, "C", "Crossmaglen", "Home Repairs", "If anyone out there would be nice enough to come to my house and change a few of my outside lightbulbs. I can provide the LED spotlight bulbs required but just need a capable person to put them in!",
 "Home Repairs", "Home", CURRENT_DATE, "2026-01-21", "2026-01-21");

INSERT INTO project_jobs(project_id, job_id)
VALUES
(1, 1);
 
INSERT INTO reviews (helper_id, reviewer_id, job_id, star_rating, review)
VALUES
(2, 1, 1, 5, 'Ryan was fantastic! He helped me with my home repairs and was very professional.');

INSERT INTO messages (sender_id, receiver_id, content)
VALUES
(2, 1, "Hi, I would love to work with Tidy Towns. What projects are available?"),
(1, 2,"That's great Ryan. We have lots of projects waiting to kick off, is there anything in particular you would be interested in?");
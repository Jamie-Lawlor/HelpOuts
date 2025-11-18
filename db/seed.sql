
INSERT INTO users (name, email, password, type, work_area, specialism, skills, rating)
VALUES
("Bridget Muckian", "bridgetm1@gmail.com", "Test1234567!", "helpee", "Crosmaglen", "", "", 0),
("Ryan O'Hare", "ryanohare@gmail.com", "Test1234567!", "helper", "Crossmaglen", "Contractor", " Carpentry, Home Maintinance, General Maintinance,", 3);


INSERT INTO user_permissions (user_id, accepted_terms, accepted_gdpr, accepted_health_safety)
VALUES
(1, FALSE, FALSE, FALSE),
(2, FALSE, FALSE, FALSE);

INSERT INTO reviews (helper_id, reviewer_id, job_id, star_rating, review)
VALUES
(2, 1, 1, 5, 'Ryan was fantastic! He helped me with my home repairs and was very professional.');

INSERT INTO jobs ( helper_id, helpee_id, status, area, job_title, job_description, short_title, short_type, created_date, start_date, end_date)
VALUES
(2, 1, "C", "Crossmaglen", "Home Repairs", "If anyone out there would be nice enough to come to my house and change a few of my outside lightbulbs. I can provide the LED spotlight bulbs required but just need a capable person to put them in!",
 "Home Repairs", "Home", CURRENT_DATE, "2026-01-21", "2026-01-21");
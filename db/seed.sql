INSERT INTO communities (id, name, area, description, profile_picture)
VALUES
(1, 'Dundalk Tidy Towns', 'Dundalk, Co.Louth', 'Dundalk Tidy Towns is committed to creating a cleaner and greener environment for the people of Dundalk. Working with the local community and businesses alike to improve the aesthetic appearance of the town. ', "/static/images/community_image.png"),
(2, "Monaghan Tidy Towns", "Monaghan, Co.Monaghan", "Monaghan Tidy Towns is committed to creating a cleaner and greener environment for the people of Monaghan. Working with the local community and businesses alike to improve the aesthetic appearance of the town. ", "");

INSERT INTO projects(community_id, project_title, project_description, project_type, number_of_helpers, start_date, end_date)
VALUES
(1, "Build new community park", "Building a new park for the community of Dundalk", "Environment", 5, "2026-01-08", "2026-07-21"),
(2, "Build new Social club", "Building a social space for the local community of Dundalk", "social_and_events", 6, "2026-07-01", "2026-12-19");



INSERT INTO community_projects(project_id, community_id)
VALUES
(1, 1);

INSERT INTO users (name, email, password, type, work_area, specialism, skills, rating, private_key, public_key, community_id, profile_picture)
VALUES
("Bridget Muckian", "bridgetm1@gmail.com", "Test1234567!", "helpee", "Crossmaglen", "", "", 0, "", "", 1, ""),
("Ryan O'Hare", "ryanohare@gmail.com", "Test1234567!", "helper", "Crossmaglen", "Contractor", " Carpentry, Home Maintenance, General Maintenance,", 3,"MIIEpAIBAAKCAQEAmUDCAdU/+Fv4HWRMQ51jZcQuu/Wgc7h00qe2L7wNbKSHLD8IQoaKOYJ6ugzNNVggvfpKTAAi+MXvL6uQBzH/hjeYwq7f+etVtUJvj3nVdNtAMK+nIofj3xsqGhiPHDq7TU5DtDPxbpLgRJuXpySSj2eh8iksyrO01NsV/K5J0R6Ws0wrLUHxfdboKleJ/laCIgJxBTbtPBKNv7BTViOb3XIcASsdeLiV7JDbTEUw5vBEYvs5lwTyewOa379fO3tq3rYMQer9GWzKVb/6xls1nCie7Fj5iMaW/StYB4S58TPO3MJDgl22oIPlm3G5nd6gqsu3vNtgdlYskqSUeZ3t+wIDAQABAoIBAB6Jk98Poi6YDOm2aafzfbHylKlpeW51q/mp55i9bSNf6Xt8l+XBr1tkT5YxJNbjV6rja9iXEmDl+BJUql90rAkPnQX2GLVRGoQC1/4L9efSJIlPBwvPbi2v2QTYLfQfE+GEneMTkqFI7R1er6pjlDy1FsUNRVqi0n6zpT7zb8wWcEOU4k2aA0MLzGRBaNyzDHBBYKuZ9NlUvUNzdrcbJW8nMYrctcf7nGKlw7UhX2Mtp9KmGXK5n022RABbhlJQBZxxI57DY4A3m7vOhQbsqMpRMCXBcm42zbCbV8Utdg019fz4TYHCMPHauSmXSdnjtialTvqkEWKPaudXzCaI84kCgYEAz9cj9bHAeDqdeK5le68gIsVDpnSo2fD50k/edZ6SaKXMljxuup0kqnPBa9Xi3gCCaVF9p2SOQKJKTafuHXVBW2Ry22YYlVb24Efp3lyOoCZrzItBH2UkwFVD7oApW5VeL5TRC8ShAbxDUkPi2y2H6E3hHoA2/KXwx7NQy1R2mvUCgYEAvMONTjtghezZ0kivy1efvN0/r0b4q2PYFpuyiWRViVk8APRtBOyvEC8URn5Xagp1j1CnbBx8p1Ai3wj5h0p72ctn1AntxDJzzE7B9katFjwVp68uZG2DOE/JS0pJuJlti0576+8Qp2dToTIHSJZgt5Jiox4yfnZXmpITjjYCry8CgYAg4wf7no63935nVCEWuxU4q0ITGq6FHc5J6v1mWxsLmACRXSqgOLFOj1Zxu7xUKHx6MbzSOeUQcR2UwBe7bYxT68cI1FTbfJE/1+E3oCmpSasRCI/baeOw000Wdg0VQsNOgBu74vcfES0N3VQOHlw88+XFL8CDpbY9wy/rnIfP6QKBgQC6KECa/oPakBLhBz4XU3r9T1UXDu7+V6Er6rDQPlr88Tvz1RoO2TxswYFFZCPhOB9oDyqNvCpS9vzs6HTtr88koyzqOEB8VSVOP/2ZW2onm2nfzSv7buUSC92AmurJWsZltCkSLNpHvecD+cqlE2ieoYcVRxqVDTCoB5exkCJlkQKBgQCWGGWi1wdrptKX3OQ+muOLJT+gjbOGPmV2bmPX5cHSfGPVx88/wbwTdksM9S8l705WQ3ZRT4mLTr4q/+FYZE2kgvHH41mVvWnJ0CmFcPmiOQrOqWQSfl/Yp8sYdJuZUwG15AY9KDaTwinOXIYd5sfhKPYRjfjEFP6oCKWjsY6Obw==", "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmUDCAdU/+Fv4HWRMQ51jZcQuu/Wgc7h00qe2L7wNbKSHLD8IQoaKOYJ6ugzNNVggvfpKTAAi+MXvL6uQBzH/hjeYwq7f+etVtUJvj3nVdNtAMK+nIofj3xsqGhiPHDq7TU5DtDPxbpLgRJuXpySSj2eh8iksyrO01NsV/K5J0R6Ws0wrLUHxfdboKleJ/laCIgJxBTbtPBKNv7BTViOb3XIcASsdeLiV7JDbTEUw5vBEYvs5lwTyewOa379fO3tq3rYMQer9GWzKVb/6xls1nCie7Fj5iMaW/StYB4S58TPO3MJDgl22oIPlm3G5nd6gqsu3vNtgdlYskqSUeZ3t+wIDAQAB", 1, "/static/images/user_image_2.png");

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

INSERT INTO messages (sender_id, receiver_id, content, timestamp)
VALUES
(2, 1, "Hi, I would love to work with Tidy Towns. What projects are available?", CURRENT_DATE),
(1, 2,"That's great Ryan. We have lots of projects waiting to kick off, is there anything in particular you would be interested in?", CURRENT_DATE);

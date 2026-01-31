INSERT INTO communities (id, name, area, description, profile_picture)
VALUES
(1, 'Dundalk Tidy Towns', 'Dundalk, Co.Louth', 'Dundalk Tidy Towns is committed to creating a cleaner and greener environment for the people of Dundalk. Working with the local community and businesses alike to improve the aesthetic appearance of the town.', '/static/images/community_image.png'),
(2, 'Ardee Tidy Towns', 'Ardee, Co.Louth', 'Ardee Tidy Towns is dedicated to enhancing the beauty and cleanliness of Ardee through community involvement and sustainable practices.', NULL),
(3, 'Mens Shed Dundalk', 'Dundalk, Co.Louth', 'Mens Shed Dundalk provides a supportive environment for men to connect, share skills, and work on projects that benefit the local community.', NULL);

INSERT INTO users (id, name, email, password, type, work_area, specialism, skills, rating, private_key, public_key, profile_picture, community_id)
VALUES 
(1, 'Leo Fitz', 'leofitz@gmail.com', 'Test1234567!', 'helper', 'Dundalk', 'Electrician', 'Carpentry, Home Maintenance, General Maintenance,', 4, NULL, NULL, NULL, 1),
(2, 'Ryan O''Hare', 'ryanohare@gmail.com', 'Test1234567!', 'helper', 'Crossmaglen', 'Contractor', 'Carpentry, Home Maintenance, General Maintenance,', 3,'-----BEGIN RSA PRIVATE KEY-----
    MIIEoQIBAAKCAQBzJWO7XCVJ07F0WxghUiYhK4YRSWH2q8PcdEpGjTBwUsIt2cRK
    0fMMLPHlvESqfdttuhmpZ1PSGviOxJMDutG60fWIT/xFsRNi+eSlE5EnLYR1V87b
    8GuIczk8sMot5+pPFlQ5mY8yElCnkmtq6SJf5GUvqWhqEv+psgY6eGF7foEj6xL/
    7F16v75tNZjidU3pZ3gwErLLUUZr6lYd9k17hrgcYmVPSEqY6WsEX8brCk2xsSaM
    PxC51HOddgT/w6Aw7bWkk1wCDLpV3cl/ypZ4H8puRZhYu/anfebotzFMvJB+jqh/
    v0swxasah1tdCdjttKB5KfUd5+I5QE2zNzivAgMBAAECggEANvPYJfmy/gnevcYf
    vP9EnT31TNi1vRB6eAKz0/nb7S9B5rnwGTkbgmsMwvRX3PoVt8dCKfvbIAGpMBGW
    jAgjwcIkKPrrTaNVuj3Cphmxg34QoiPW4FZcK5G59kH1K3Vr+HSSm66yjVX6Ug7p
    3usGcbdBpz51S3Jnu2fv2wXKmDG+ZkHhSdjZmWFum+knkyas8uZO+3aO54+07pmU
    SQmy+RnoNclIhSsxGqBWCDwrX4XiWdGphYsNyQZud9oBgJIC7/DjCm4Ui8miZYnq
    unqmLgioawOaQvk22Pa3po5ytJeZc37ftAtOfmXSm0S0S64GBj6GnFAPo8Vvmvzq
    Q8aKQQKBgQDX1cqsO5CUQnW/S3z2aE6c+VOdENkMmp3aG0U668y8EIIn0OP8Ep5O
    NIhDCgQlTkl6KUqOFXKuVN0pJX0cZ141tUwC+aIn7vuGYvskQmxN9R61GzGdumQj
    CmI0ZRVnRJ3/W1Ij/e5RJLoeGhK65lB8a/mBrIdnpAB1AxZYU/w9YQKBgQCIktpm
    QwToVDML0MhL8Y8bAGeF85QntSLdc+jcrKZjWtqD32hkIDlG92sL3cIV0w7g+ZLb
    W5hbtwByH08swTGeGPSgtRlE0mm4rq2BuNnpRC2UwAs4Bnv006Gt+CTFPCo0n2QS
    4Fw/QMcsgkhI0QBPjD57PcL1CISAH5wznvOgDwKBgEKNOaFB/KK6m3QQ4sdYAmWE
    u7OCrmqkgmfuYLp6WvbiYD/GuYXQd9/Fcv645+5Y5W81rDeDhYkbwdYeKSXI+dO1
    w2pnbwjBN+2IN8hGcv7WxlExwWrRPm9PlFhzktX04oMKtZlDg2ih2oHNqFjZC5hR
    8u15NYdPmpR6DznNK8oBAoGABZl3yN+QkPH60c4ymCKESogetnhBJ8uebVP2RS3y
    +HneIbAEOK61inpUcj0aWwi3QHQbGFFOEtyS8RrlhSE6po/BX+Fs8sxptz+6L2pj
    zNOVxtaE3zws0uHmbBqTb17DIDs0wC1gutsuD14cFpgzGg/W8/iZSLCbtiEVp2wp
    8vMCgYBSfkyvqE/x7SiB6pyNwXgpTZnyd70jxR+p8ZgBpW0Ki0bRY3EJuMJuVlqU
    Rsyid93hKk17nVD5pT2CHYohgVqHoLvmEwa2IsR6sSwU2/FHJbNniaNjHh1soXmZ
    hw4eWDdHDO91iasVphg6oHOfAbYgjMwFEYnOqvo9GuDrcxn7Wg==
    -----END RSA PRIVATE KEY-----', '-----BEGIN PUBLIC KEY-----
    MIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBzJWO7XCVJ07F0WxghUiYh
    K4YRSWH2q8PcdEpGjTBwUsIt2cRK0fMMLPHlvESqfdttuhmpZ1PSGviOxJMDutG6
    0fWIT/xFsRNi+eSlE5EnLYR1V87b8GuIczk8sMot5+pPFlQ5mY8yElCnkmtq6SJf
    5GUvqWhqEv+psgY6eGF7foEj6xL/7F16v75tNZjidU3pZ3gwErLLUUZr6lYd9k17
    hrgcYmVPSEqY6WsEX8brCk2xsSaMPxC51HOddgT/w6Aw7bWkk1wCDLpV3cl/ypZ4
    H8puRZhYu/anfebotzFMvJB+jqh/v0swxasah1tdCdjttKB5KfUd5+I5QE2zNziv
    AgMBAAE=
    -----END PUBLIC KEY-----','/static/images/user_image_2.png', 1),
(3, 'Bridget Muckian', 'bridgetm1@gmail.com', 'Test1234567!', 'helper', 'Crossmaglen', 'Local Helper', '', 0, NULL, NULL, NULL, 1),
(4, 'Daisy Johnson', 'daisyjohnson@gmail.com', 'Test1234567!', 'helper', 'Dundalk', 'Local Helper', '', 4, NULL, NULL, NULL, 1),
(5, 'Jemma Simmons', 'jemmasimmons@gmail.com', 'Test1234567!', 'helper', 'Ardee', 'Local Helper', '', 3, NULL, NULL, NULL, 2);


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
    INSERT INTO communities (id, name, area, description, profile_picture)
    VALUES
    (1, 'Dundalk Tidy Towns', 'Dundalk, Co.Louth', 'Dundalk Tidy Towns is committed to creating a cleaner and greener environment for the people of Dundalk. Working with the local community and businesses alike to improve the aesthetic appearance of the town. ', "/static/images/community_image.png"),
    (2, "Monaghan Tidy Towns", "Monaghan, Co.Monaghan", "Monaghan Tidy Towns is committed to creating a cleaner and greener environment for the people of Monaghan. Working with the local community and businesses alike to improve the aesthetic appearance of the town. ", "");

    INSERT INTO projects(community_id, project_title, project_description, project_type, number_of_helpers, start_date, end_date)
    VALUES
    (1, "Build new community park", "Building a new park for the community of Dundalk", "Environment", 5, "2026-01-08", "2026-07-21"),
    (1, "Build new Social club", "Building a social space for the local community of Dundalk", "social_and_events", 6, "2026-07-01", "2026-12-19"),
    (1, "Food drive", "Help distributing food to those in need in Dundalk", "Environment", 9, "2026-01-25", "2027-01-25"),
    (2, "Build community play park", "Building a new play park for the community of Monaghan", "Environment", 5, "2026-01-08", "2026-07-21");


    INSERT INTO users (name, email, password, type, work_area, specialism, skills, rating, private_key, public_key, community_id, profile_picture)
    VALUES
    ("Bridget Muckian", "bridgetm1@gmail.com", "Test1234567!", "helpee", "Crossmaglen", "", "", 0, "-----BEGIN RSA PRIVATE KEY-----
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
    -----END RSA PRIVATE KEY-----", "-----BEGIN PUBLIC KEY-----
    MIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBzJWO7XCVJ07F0WxghUiYh
    K4YRSWH2q8PcdEpGjTBwUsIt2cRK0fMMLPHlvESqfdttuhmpZ1PSGviOxJMDutG6
    0fWIT/xFsRNi+eSlE5EnLYR1V87b8GuIczk8sMot5+pPFlQ5mY8yElCnkmtq6SJf
    5GUvqWhqEv+psgY6eGF7foEj6xL/7F16v75tNZjidU3pZ3gwErLLUUZr6lYd9k17
    hrgcYmVPSEqY6WsEX8brCk2xsSaMPxC51HOddgT/w6Aw7bWkk1wCDLpV3cl/ypZ4
    H8puRZhYu/anfebotzFMvJB+jqh/v0swxasah1tdCdjttKB5KfUd5+I5QE2zNziv
    AgMBAAE=
    -----END PUBLIC KEY-----", 1, ""),
    ("Ryan O'Hare", "ryanohare@gmail.com", "Test1234567!", "helper", "Crossmaglen", "Contractor", " Carpentry, Home Maintenance, General Maintenance,", 3,"-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAkGRS4bvOW56qC0Ph4kRsGOF9sqGnO1m5+EdURNO+FBee8pX3
whaXWHtM4NeD1PTGlKCt8LbLcyPNXOKNkFMojEbUBeTKmJUjQNxg5b9yvoFGWGC3
67K+3ws1PYkQrJhaKDq1Sy65Vo7HLNsVWpl3+2QFnPSsUL2BAqYcmgkQTO8eUynn
mWvkYSF+E6bXGfotWqTGiSfTffHxqge/MVYtbw5x+JdjKO5zZG2e76ItsDEQpojR
N89NzoyMK/IftoTVJaaDUPx+VQjuqkCQ/OOSZgSTJ9Nwq891Np5W0TAoBerXQXn8
hOp62CkxzXhBZ+GcXW3yy5Y5JUqKahP6FtbYQQIDAQABAoIBAFGBcA+gNdId9Bq7
zMwul15MGuo0ufOUqJdvnC/l3ov08XI6GUrj+bamkzTwMqiJK3dGZClW5e0uroPa
FtL7Pg5BBPn2ti3/MZExVTkbIqhKzOyiW++eTIQXDYyYzGLA9VN0IFY6H8Cug9vc
J2em7cVoJor8yjAhaKuYHNkOeLcT/fLWxwHY/+K1BGdkawBg4/scndkDHXaXGRW0
80SXQWMryA+LZLUcBl5S5k4hUx64Gf0Sn9xgZkgAo8PhFJdEFB/h+E+hZinpxGgn
byU6a3ntwttEUx2b1NXSgK/NSsUW+RmLQyeo7dCKzWCZ08oeruYGRuCKoxEDouz5
yl6PC4kCgYEA6xOTnChK5MoMy3c2+ApOiu2e0EdNqR+GCnlfdHEsSu4+YAFoUd3v
8YbBNsrcfr9tXanazpsxwiszLUAxUFwlnOWP3k0ooDXdOPLpaT2kVPXyRqMYdTEe
gqiqemDrVvIxVfljQtBxmptLdQEM45Wjlc1eAS95t6j8EzoclnZMwXcCgYEAnT5r
ZDmk2s4k8DJVTzrE6vYzuXXXvX2urwkIcjY+Wrqg6JMVEvpbVhnlj98Te9CejChQ
MhcVoZ0Ej3RZUw2G9XVYLRDTUMOQT6jyp0dhjvsrach7t3g1D9Qj5YBvJkmsz/V5
jXc3I6D3muwQNoeV6r1Bf7bP7mxbnTOrqShCYgcCgYBl2c6Lyx1f8XcHtPhZEcYk
BX5YyXwJecIOybWk8t/4+y6FVDbJubobUIJoZg6Q0Annmg9WkwFFGoiK45Q6OCKH
zyK9c3rVp2DZKs4crfuEYCd/mWygYg7RF5j9ev6cZkUf9fSe30dJcF2KLVFTTeNZ
pWhEZTh8bbgB8JywSENLUwKBgQCP9hLaOtBMpwk4g8yI8jRRLcFjXZl8WjHw/KMn
9bOW22DwLaDQtDelF6aN1t1+sRxHE62AfpQGV7xSHmKdYDgcSCfHcq0VN0bLN9GZ
BwgxoJE5kxx5d+uUp1OKDdE1S6SU7JgxxWDNFNU8mD2rvuypckYiSFwMXFZwEVtr
TnmgRwKBgQC5MioOtHFwkqpf2qy7BfhtgOsPEcKCGjHZ6rcRG0KrVSLewUfFogiK
LE8bZLFUxSaPXMViXMemxXVmI1AwiGDkYaTphsN+YcvkevHZ6QGXPZ+x4uI4/Yba
Rw81ncb07XBqvMhYDf7FkBqZGYar/Kgkbj0VuijucMy2C88Z5FnSyg==
-----END RSA PRIVATE KEY-----","-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkGRS4bvOW56qC0Ph4kRs
GOF9sqGnO1m5+EdURNO+FBee8pX3whaXWHtM4NeD1PTGlKCt8LbLcyPNXOKNkFMo
jEbUBeTKmJUjQNxg5b9yvoFGWGC367K+3ws1PYkQrJhaKDq1Sy65Vo7HLNsVWpl3
+2QFnPSsUL2BAqYcmgkQTO8eUynnmWvkYSF+E6bXGfotWqTGiSfTffHxqge/MVYt
bw5x+JdjKO5zZG2e76ItsDEQpojRN89NzoyMK/IftoTVJaaDUPx+VQjuqkCQ/OOS
ZgSTJ9Nwq891Np5W0TAoBerXQXn8hOp62CkxzXhBZ+GcXW3yy5Y5JUqKahP6FtbY
QQIDAQAB
-----END PUBLIC KEY-----", 1, "/static/images/user_image_2.png");

    INSERT INTO user_permissions (user_id, accepted_terms, accepted_gdpr, accepted_health_safety)
    VALUES
    (1, FALSE, FALSE, FALSE),
    (2, FALSE, FALSE, FALSE);


    INSERT INTO jobs (helper_id, helpee_id, project_id, status, area, job_title, job_description, short_title, short_type, created_date, start_date, end_date)
    VALUES
    (1, 2, 1, "C", "Crossmaglen", "Home Repairs", "If anyone out there would be nice enough to come to my house and change a few of my outside lightbulbs. I can provide the LED spotlight bulbs required but just need a capable person to put them in!",
    "Home Repairs", "Home", CURRENT_DATE, "2026-01-21", "2026-01-21");

    
    INSERT INTO reviews (helper_id, reviewer_id, job_id, star_rating, review)
    VALUES
    (2, 1, 1, 5, 'Ryan was fantastic! He helped me with my home repairs and was very professional.');

    INSERT INTO messages (sender_id, receiver_id, content, timestamp)
    VALUES
    (2, 1, "Hi, I would love to work with Tidy Towns. What projects are available?", CURRENT_DATE),
    (1, 2,"That's great Ryan. We have lots of projects waiting to kick off, is there anything in particular you would be interested in?", CURRENT_DATE);

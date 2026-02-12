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
    password VARCHAR(100) NOT NULL,
    type VARCHAR(6) NOT NULL,
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



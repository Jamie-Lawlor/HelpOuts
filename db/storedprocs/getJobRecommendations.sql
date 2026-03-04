DELIMITER //
	CREATE PROCEDURE getJobRecommendations (
		IN userId INT
    )
       BEGIN
		SELECT j.job_title, s.skill, u.name from jobs as j
			INNER JOIN job_skills as js on j.id = js.job_id
			INNER JOIN skills as s on s.id = js.skill_id
			INNER JOIN user_skills as us on js.skill_id = us.skill_id
            INNER JOIN users as u on us.user_id = u.id
            
		WHERE u.id = userId;
    
	END//
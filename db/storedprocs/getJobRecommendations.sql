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
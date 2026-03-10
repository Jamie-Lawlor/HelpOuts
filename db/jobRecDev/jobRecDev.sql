-- u -> users, s -> skills, us -> user_skill
select u.name as name, s.skill from users as u
inner join user_skills as us on u.id = us.user_id
inner join skills as s on us.skill_id = s.id;

-- j -> jobs, s -> skills, us -> user_skill
select j.job_title as name, s.skill from jobs as j
inner join job_skills as js on j.id = js.job_id
inner join skills as s on js.skill_id = s.id;



-- all jobs from a project with their skill
select j.job_title, p.project_title, s.skill as js from jobs as j
inner join projects as p on j.project_id = p.id
inner join job_skills as js on j.id = js.job_id
inner join skills as s on js.skill_id = s.id;


select u.name as name, s.skill from users as u 
inner join user_skills as us on u.id = us.user_id
inner join skills as s on us.skill_id = s.id
where name = "Leo";


-- select j.job_title, u.name, s.skill from users as u
-- inner join user_skills as us on u.id = us.user_id
-- inner join job_skills as js on j.id = js.job_id;

select j.job_title, s.skill, u.name from jobs as j
inner join job_skills as js on j.id = js.job_id
inner join skills as s on s.id = js.skill_id
inner join user_skills as us on js.skill_id = us.skill_id
inner join users as u on us.user_id = u.id;


select j.job_title, s.skill, u.name from jobs as j
inner join job_skills as js on j.id = js.job_id
inner join skills as s on s.id = js.skill_id
inner join user_skills as us on js.skill_id = us.skill_id
inner join users as u on us.user_id = u.id;



SELECT
  j.id,
  j.job_title,
  j.status,
  j.area,
  u.id AS user_id,
  u.name,
  COUNT(DISTINCT js.skill_id) AS match_score
FROM jobs AS j
INNER JOIN job_skills AS js ON j.id = js.job_id
INNER JOIN user_skills AS us ON js.skill_id = us.skill_id
INNER JOIN users AS u ON us.user_id = u.id
WHERE u.id = 3
GROUP BY
  j.id, j.job_title, j.status, j.area, u.id, u.name
ORDER BY match_score DESC, j.id;
        

DELIMITER //
	CREATE PROCEDURE getJobRecommendations (
		IN userId INT
    )
       BEGIN
		SELECT
			  j.id,
			  j.job_title,
			  j.status,
			  j.area,
			  u.id AS user_id,
			  u.name,
			  COUNT(DISTINCT js.skill_id) AS match_score
			FROM jobs
	
			INNER JOIN job_skills as js on j.id = js.job_id
			INNER JOIN skills as s on s.id = js.skill_id
			INNER JOIN user_skills as us on js.skill_id = us.skill_id
            INNER JOIN users as u on us.user_id = u.id
            
		WHERE u.id = userId;
    
	END//



















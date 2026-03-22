from db.database import db
from db.models import Users, Communities, Projects, Jobs

def test_delete_post_deletes_job(client, app):
    app.config["LOGIN_DISABLED"] = True

    with app.app_context():
        community = Communities(
            name="Test Community",
            area="Dundalk",
            description="Test description",
            profile_picture="",
        )
        db.session.add(community)
        db.session.commit()

        user = Users(
            name="Chair User",
            email="chair@example.com",
            password="Test1234567!",
            type="chairperson",
            work_area="Dundalk",
            rating=0,
            private_key=b"123",
            public_key=b"456",
            profile_picture="",
            verified=True,
            verification_accuracy=99,
            community_id=community.id,
        )
        db.session.add(user)
        db.session.commit()

        project = Projects(
            project_title="Test Project",
            project_description="Test project description",
            project_type="Painting",
            status="A",
            number_of_helpers=1,
            community_id=community.id,
        )
        db.session.add(project)
        db.session.commit()

        job = Jobs(
            project_id=project.id,
            status="A",
            area="Dundalk",
            job_title="Test Job",
            job_description="Test job description",
            short_title="Test",
            short_type="painting",
        )
        db.session.add(job)
        db.session.commit()

        user_id = user.id
        community_id = community.id
        job_id = job.id

    with client.session_transaction() as sess:
        sess["user_id"] = user_id
        sess["type"] = "chairperson"
        sess["community_id"] = community_id

    resp = client.post("/delete_post", json={"post_id": job_id})

    assert resp.status_code == 200, resp.get_data(as_text=True)

    with app.app_context():
        assert Jobs.query.get(job_id) is None
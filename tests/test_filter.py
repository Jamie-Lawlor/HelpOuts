from uuid import uuid4

from db.database import db
from db.models import Users, Communities, Projects, Jobs


def unique_email(prefix="user"):
    return f"{prefix}_{uuid4().hex[:8]}@example.com"


def create_test_data():
    community = Communities(
        name=f"Test Community {uuid4().hex[:6]}",
        area="Dundalk",
        description="Test description",
        profile_picture="",
    )
    db.session.add(community)
    db.session.commit()

    chairperson = Users(
        name="Chair User",
        email=unique_email("chair"),
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

    helper = Users(
        name="Helper User",
        email=unique_email("helper"),
        password="Test1234567!",
        type="helper",
        work_area="Dundalk",
        rating=0,
        private_key=b"123",
        public_key=b"456",
        profile_picture="",
        verified=True,
        verification_accuracy=99,
        community_id=community.id,
    )

    db.session.add_all([chairperson, helper])
    db.session.commit()

    project = Projects(
        project_title=f"Test Project {uuid4().hex[:6]}",
        project_description="Test project description",
        project_type="Community",
        status="A",
        number_of_helpers=2,
        community_id=community.id,
    )
    db.session.add(project)
    db.session.commit()

    job1 = Jobs(
        project_id=project.id,
        status="A",
        area="Dundalk",
        job_title=f"Build Shed {uuid4().hex[:6]}",
        job_description="Construction job",
        short_title="Build",
        short_type="construction",
    )

    job2 = Jobs(
        project_id=project.id,
        status="A",
        area="Dundalk",
        job_title=f"Plant Trees {uuid4().hex[:6]}",
        job_description="Environment job",
        short_title="Trees",
        short_type="environment",
    )

    db.session.add_all([job1, job2])
    db.session.commit()

    return {
        "community_id": community.id,
        "chairperson_id": chairperson.id,
        "helper_id": helper.id,
        "project_id": project.id,
        "job1_id": job1.id,
        "job2_id": job2.id,
        "job1_title": job1.job_title,
        "job2_title": job2.job_title,
    }


def login_test_user(client, user_id, community_id, user_type="helper"):
    with client.session_transaction() as sess:
        sess["user_id"] = user_id
        sess["type"] = user_type
        sess["community_id"] = community_id


def create_home_page_user():
    community = Communities(
        name=f"Home Community {uuid4().hex[:6]}",
        area="Dundalk",
        description="Home page test description",
        profile_picture="",
    )
    db.session.add(community)
    db.session.commit()

    user = Users(
        name="Home Page User",
        email=unique_email("homepage"),
        password="Test1234567!",
        type="helper",
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

    return user.id, community.id

def test_home_page_shows_job_filters(client, app):
    with app.app_context():
        user_id, community_id = create_home_page_user()

    login_test_user(client, user_id, community_id, "helper")

    resp = client.get("/home_page/")
    assert resp.status_code == 200, resp.get_data(as_text=True)

    html = resp.get_data(as_text=True)
    assert "Explore Jobs" in html
    assert "Environment" in html
    assert "Social &amp; Events" in html or "Social & Events" in html
    assert "Construction" in html
    assert "General Maintenance" in html
    assert "Safety" in html


def test_home_page_shows_construction_filter_card(client, app):
    with app.app_context():
        user_id, community_id = create_home_page_user()

    login_test_user(client, user_id, community_id, "helper")

    resp = client.get("/home_page/")
    assert resp.status_code == 200, resp.get_data(as_text=True)

    html = resp.get_data(as_text=True)
    assert 'id="filter-construction"' in html
    assert "Construction" in html
    assert "filter_jobs('construction')" in html
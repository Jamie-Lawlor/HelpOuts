from db.database import db
from db.models import Communities, Projects

def test_add_project_to_dundalk_tidy_towns(client, app):
    with app.app_context():
        c = Communities(
            name="Dundalk Tidy Towns",
            area="Dundalk, Co.Louth",
            description="Test community",
            profile_picture="/static/images/community_image.png",
        )
        db.session.add(c)
        db.session.commit()
        community_id = c.id

    with client.session_transaction() as sess:
        sess["community_id"] = community_id
        sess["type"] = "chairperson" 

    resp = client.post(
        "/create_project",
        data={
            "title": "New Dundalk Clean-Up",
            "description": "Community clean-up event",
            "type": "Environment",
            "helpers": "10",
            "start_date": "2026-06-01",
            "end_date": "2026-06-30",
        },
    )

    assert resp.status_code == 200

    data = resp.get_json()
    assert data["project_title"] == "New Dundalk Clean-Up"
    assert data["project_description"] == "Community clean-up event"
    assert data["project_type"] == "Environment"
    assert int(data["number_of_helpers"]) == 10
    assert data["community_id"] == community_id

    # Confirm it really hit the DB
    with app.app_context():
        saved = Projects.query.filter_by(project_title="New Dundalk Clean-Up").first()
        assert saved is not None
        assert saved.community_id == community_id
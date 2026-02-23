from db.database import db
from db.models import Communities, Projects

def test_add_project_to_dundalk_tidy_towns(client, app):
    # create the community row first (because project references it)
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

    resp = client.post(
        "/create_project",
        data={
            "title": "New Dundalk Clean-Up",
            "description": "Community clean-up event",
            "type": "Environment",
            "helpers": "10",
            "start_date": "2026-03-01",
            "end_date": "2026-03-30",
        },
    )

    assert resp.status_code == 200

    with app.app_context():
        p = Projects.query.filter_by(project_title="New Dundalk Clean-Up").first()
        assert p is not None
        assert p.community_id == community_id
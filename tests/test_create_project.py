from db.models import Projects

def test_add_project_to_dundalk_tidy_towns(client, app, community):
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
    assert resp.is_json

    data = resp.get_json()
    assert data["project_title"] == "New Dundalk Clean-Up"
    assert data["community_id"] == 1

    with app.app_context():
        p = Projects.query.filter_by(project_title="New Dundalk Clean-Up").first()
        assert p is not None
        assert p.community_id == 1

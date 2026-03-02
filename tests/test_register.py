from db.database import db
from db.models import Users


def test_register_helper_currently_fails_due_to_missing_required_fields(client, app):
    """
    The /register route does NOT supply required Users fields:
    - private_key (nullable=False)
    - public_key  (nullable=False)
    - profile_picture (nullable=False)

    So the request should fail until the route is updated.
    """
    resp = client.post(
        "/register",
        data={
            "first_name": "Rory",
            "last_name": "OGorman",
            "email": "rorytest123@gmail.com",
            "location": "Dundalk",
            "password": "Test1234567!",
            "confirm_password": "Test1234567!",
            "user_type": "helper",
        },
        follow_redirects=False,
    )

    assert resp.status_code == 400

    with app.app_context():
        assert Users.query.filter_by(email="rorytest123@gmail.com").first() is None
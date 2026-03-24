from db.database import db
from db.models import Users


def test_job_recommendations_based_on_membership(client, app, monkeypatch):
    with app.app_context():
        member_user = Users(
            name="Member User",
            email="member@example.com",
            password="Test1234567!",
            type="helper",
            work_area="Dundalk",
            rating=0,
            private_key=b"123",
            public_key=b"456",
            profile_picture="",
            verified=True,
            verification_accuracy=99,
            community_id=1,
        )

        non_member_user = Users(
            name="Non Member User",
            email="nonmember@example.com",
            password="Test1234567!",
            type="helper",
            work_area="Dundalk",
            rating=0,
            private_key=b"123",
            public_key=b"456",
            profile_picture="",
            verified=True,
            verification_accuracy=99,
            community_id=None,
        )

        db.session.add_all([member_user, non_member_user])
        db.session.commit()

        member_id = member_user.id
        non_member_id = non_member_user.id

    class FakeCursor:
        def __init__(self):
            self.called_user_id = None

        def callproc(self, procname, args):
            self.called_user_id = args[0]

        def fetchall(self):
            if self.called_user_id == member_id:
                return [
                    (1, "Paint fence", "A", "Dundalk", member_id, "Member User", 3)
                ]
            return []

        def close(self):
            pass

    class FakeConnection:
        def __init__(self):
            self.cursor_obj = FakeCursor()

        def cursor(self):
            return self.cursor_obj

        def commit(self):
            pass

        def close(self):
            pass

    class FakeEngine:
        def raw_connection(self):
            return FakeConnection()

    class FakeDB:
        engine = FakeEngine()

    import routes.posts as posts_module
    monkeypatch.setattr(posts_module, "db", FakeDB())

    with client.session_transaction() as sess:
        sess["user_id"] = member_id

    resp = client.get("/getJobRecommendations")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data is not None
    assert any("Paint fence" in str(item) for item in data)

    with client.session_transaction() as sess:
        sess["user_id"] = non_member_id

    resp = client.get("/getJobRecommendations")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data is not None
    assert not any("Paint fence" in str(item) for item in data)
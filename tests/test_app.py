import tempfile
import unittest

from app import Database, create_app


class FakePostgresCursor:
    def __init__(self):
        self.executed_many = None

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def executemany(self, query, params):
        self.executed_many = (query, params)


class FakePostgresConnection:
    def __init__(self):
        self.executed = None
        self.cursor_instance = FakePostgresCursor()

    def execute(self, query, params):
        self.executed = (query, params)

    def cursor(self):
        return self.cursor_instance


class AppointmentBoardTests(unittest.TestCase):
    def setUp(self):
        self.database = tempfile.NamedTemporaryFile(suffix=".sqlite3", delete=False)
        self.database.close()
        self.app = create_app(
            {"TESTING": True, "DATABASE": self.database.name, "DATABASE_URL": "", "SECRET_KEY": "test"}
        )
        self.client = self.app.test_client()

    def test_board_shows_seeded_appointments(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Design review", response.data)

    def test_stylesheet_is_served(self):
        response = self.client.get("/style.css", buffered=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"--teal", response.data)

    def test_postgres_adapter_uses_psycopg_parameters(self):
        connection = FakePostgresConnection()
        database = Database(connection, is_postgres=True)
        database.execute("SELECT * FROM appointments WHERE id = ?", (7,))
        database.executemany("INSERT INTO appointments (title) VALUES (?)", [("Review",)])

        self.assertEqual(connection.executed[0], "SELECT * FROM appointments WHERE id = %s")
        self.assertEqual(
            connection.cursor_instance.executed_many,
            ("INSERT INTO appointments (title) VALUES (%s)", [("Review",)]),
        )

    def test_overlapping_active_appointment_is_rejected(self):
        response = self.client.post(
            "/appointments/new",
            data={
                "title": "Conflicting call",
                "description": "",
                "appointment_date": "2026-09-14",
                "start_time": "09:45",
                "end_time": "10:30",
            },
            follow_redirects=True,
        )
        self.assertIn(b"overlaps an existing active appointment", response.data)

    def test_cancelled_appointment_does_not_reserve_its_slot(self):
        response = self.client.post(
            "/appointments/new",
            data={
                "title": "Replacement planning",
                "description": "",
                "appointment_date": "2026-09-15",
                "start_time": "14:00",
                "end_time": "14:45",
            },
            follow_redirects=True,
        )
        self.assertIn(b"Appointment added to the board", response.data)


if __name__ == "__main__":
    unittest.main()

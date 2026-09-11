import tempfile
import unittest

from app import create_app


class AppointmentBoardTests(unittest.TestCase):
    def setUp(self):
        self.database = tempfile.NamedTemporaryFile(suffix=".sqlite3", delete=False)
        self.database.close()
        self.app = create_app({"TESTING": True, "DATABASE": self.database.name, "SECRET_KEY": "test"})
        self.client = self.app.test_client()

    def test_board_shows_seeded_appointments(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Design review", response.data)

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

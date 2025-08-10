import unittest
from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

from fastapi.testclient import TestClient
from models import Command
from settings import API_TOKEN

from app import app

client = TestClient(app)


class TestGetStatusEndpoint(unittest.TestCase):

    @patch("app.get_current_position", new_callable=AsyncMock)
    def test_get_status(self, mock_get_position):
        uid = str(uuid4())
        mock_get_position.return_value = (5, 10, "W", "C", uid)

        response = client.get(
            "/status", headers={"Authorization": f"Bearer {API_TOKEN}"}
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["x"], 5)
        self.assertEqual(data["y"], 10)
        self.assertEqual(data["direction"], "W")
        self.assertEqual(data["status"], "C")
        self.assertEqual(data["command_id"], uid)

        mock_get_position.assert_awaited_once()

    def test_get_status_error(self):
        response = client.get(
            "/status", headers={"Authorization": "Bearer wrong-token"}
        )
        self.assertEqual(response.status_code, 401)


class TestRegisterCommandEndpoint(unittest.TestCase):

    @patch("app.add_command", new_callable=AsyncMock)
    def test_register_command(self, mock_add_command):
        command = Mock(spec=Command)
        command.id = str(uuid4())
        mock_add_command.return_value = command

        response = client.post(
            "/command",
            json={"command": "FFF"},
            headers={"Authorization": f"Bearer {API_TOKEN}"},
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["id"], str(command.id))

        mock_add_command.assert_awaited_once()

    def test_register_command_error(self):
        response = client.post(
            "/command",
            json={"command": "FFF"},
            headers={"Authorization": "Bearer wrong-token"},
        )
        self.assertEqual(response.status_code, 401)

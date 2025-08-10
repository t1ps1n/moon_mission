import time

import requests
from settings import API_TOKEN


def get_status():
    r = requests.get(
        "http://127.0.0.1:8000/status",
        headers={"Authorization": f"Bearer {API_TOKEN}"}
    )

    assert r.status_code == 200

    data = r.json()
    assert "x" in data
    assert "y" in data
    assert "direction" in data
    assert "status" in data
    assert "command_id" in data

    return data


def create_command(command):
    r = requests.post(
        "http://127.0.0.1:8000/command",
        json={"command": command},
        headers={"Authorization": f"Bearer {API_TOKEN}"},
    )
    assert r.status_code == 200
    data = r.json()
    assert "id" in data

    return data


def test_commands_execution():
    # 1. Check the robot's initial state
    status = get_status()
    assert status["x"] == 4              # initial X coordinate
    assert status["y"] == 2              # initial Y coordinate
    assert status["direction"] == "W"    # facing West
    assert status["status"] == "C"       # status: waiting for commands
    assert status["command_id"] is None  # no active command

    # 2. Send the first command: move forward 4 steps
    data = create_command("FFFF")
    command_id = data["id"]

    # 3. Wait for the command to finish executing (2 minutes)
    time.sleep(120)

    # 4. Check state after executing the first command
    status = get_status()
    assert status["x"] == 0               # moved 4 cells to the West
    assert status["y"] == 2               # Y coordinate unchanged
    assert status["direction"] == "W"     # still facing West
    assert status["status"] == "C"        # back to idle
    assert status["command_id"] == command_id  # matches the executed command

    # 5. Send the second command: move forward 4 steps
    data = create_command("FFFF")
    command_id = data["id"]

    # 6. Wait for the second command to finish
    time.sleep(120)

    # 7. Check state after executing the second command
    status = get_status()
    assert status["x"] == -4              # moved another 4 cells to the West
    assert status["y"] == 2               # Y coordinate unchanged
    assert status["direction"] == "W"     # still facing West
    assert status["status"] == "C"        # back to idle
    assert status["command_id"] == command_id  # matches the second command


def test_face_obstacle():
    # 1. Check the robot's initial state
    status = get_status()
    assert status["x"] == 4              # initial X coordinate
    assert status["y"] == 2              # initial Y coordinate
    assert status["direction"] == "W"    # facing West
    assert status["status"] == "C"       # status: waiting for commands
    assert status["command_id"] is None  # no active command

    # 2. Send the first command: move forward 3 steps, turn right, move forward 2 steps
    # Expected to face an obstacle before completing the full path
    data = create_command("FFFRFF")
    command_id = data["id"]

    # 3. Wait for the command to finish (or stop due to an obstacle)
    time.sleep(120)

    # 4. Check state after facing the obstacle
    status = get_status()
    assert status["x"] == 1               # stopped at X=1
    assert status["y"] == 3               # moved to Y=3
    assert status["direction"] == "N"     # now facing North
    assert status["status"] == "F"        # status: failure/obstacle detected
    assert status["command_id"] == command_id  # matches the command that failed

    # 5. Send the second command: turn left, move forward 3 steps
    # This should avoid the obstacle and succeed
    data = create_command("LFFF")
    command_id = data["id"]

    # 6. Wait for the second command to finish
    time.sleep(120)

    # 7. Check state after successfully executing the second command
    status = get_status()
    assert status["x"] == -2              # moved further West
    assert status["y"] == 3               # Y coordinate unchanged
    assert status["direction"] == "W"     # facing West again
    assert status["status"] == "C"        # status: waiting for commands
    assert status["command_id"] == command_id  # matches the successfully executed command


if __name__ == "__main__":
    # test_commands_execution()
    test_face_obstacle()

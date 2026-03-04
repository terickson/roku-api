def test_list_systems(client):
    resp = client.get("/systems/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["id"] == "living-room"
    assert data[0]["host"] == "192.168.1.10"


def test_list_systems_shape(client):
    resp = client.get("/systems/")
    data = resp.json()
    for device in data:
        assert set(device.keys()) == {"id", "host"}


def test_get_system(client):
    resp = client.get("/systems/living-room")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == "living-room"
    assert data["host"] == "192.168.1.10"
    assert isinstance(data["apps"], list)
    assert data["apps"][0]["id"] == "12345"
    assert data["apps"][0]["name"] == "Netflix"


def test_get_system_not_found(client):
    resp = client.get("/systems/invalid")
    assert resp.status_code == 404


def test_create_action_home(client, mock_roku_class):
    resp = client.post("/systems/living-room/actions", json={"command": "HOME"})
    assert resp.status_code == 201
    assert resp.json()["message"] == "success"
    mock_roku_class.return_value.home.assert_called_once()


def test_create_action_search(client, mock_roku_class):
    resp = client.post(
        "/systems/living-room/actions",
        json={"command": "SEARCH", "value": "netflix"},
    )
    assert resp.status_code == 201
    mock_roku_class.return_value.search.assert_called_once()
    mock_roku_class.return_value.literal.assert_called_once_with("netflix")


def test_create_action_input(client, mock_roku_class):
    resp = client.post(
        "/systems/living-room/actions",
        json={"command": "INPUT", "value": "12345"},
    )
    assert resp.status_code == 201


def test_create_action_direction_repeat(client, mock_roku_class):
    resp = client.post(
        "/systems/bedroom/actions",
        json={"command": "UP", "value": "3"},
    )
    assert resp.status_code == 201
    assert mock_roku_class.return_value.up.call_count == 3


def test_create_action_unknown_command(client):
    resp = client.post(
        "/systems/living-room/actions",
        json={"command": "INVALID"},
    )
    assert resp.status_code == 412
    assert "INVALID" in resp.json()["message"]


def test_create_action_device_not_found(client):
    resp = client.post("/systems/invalid/actions", json={"command": "HOME"})
    assert resp.status_code == 404

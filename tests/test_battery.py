from modules.battery import battery_status

def test_status():
    assert '100%' in battery_status(100, True)

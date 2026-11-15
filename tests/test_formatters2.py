from modules.formatters import bytes_to_mb

def test_zero():
    assert bytes_to_mb(0) == 0

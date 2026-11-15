from modules.formatters import bytes_to_mb, percent_bar

def test_bytes():
    assert bytes_to_mb(1048576) == 1.0

def test_bar():
    assert len(percent_bar(50)) == 12

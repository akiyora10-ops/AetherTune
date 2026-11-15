from modules.validators import is_hex_color

def test_short():
    assert is_hex_color('#abc')

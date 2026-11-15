from modules.validators import is_hex_color

def test_hex():
    assert is_hex_color('#ff00aa')
    assert not is_hex_color('zzz')

from modules.temperatures import c_to_f

def test_convert():
    assert c_to_f(0) == 32

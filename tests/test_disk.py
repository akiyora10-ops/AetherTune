from modules.disk import free_gb

def test_free():
    assert free_gb('.') >= 0

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from modules.utils import is_admin, get_ram

def test_ram():
    total, avail, pct = get_ram()
    assert total > 0
    assert 0 <= pct <= 100

def test_is_admin_bool():
    assert isinstance(is_admin(), bool)

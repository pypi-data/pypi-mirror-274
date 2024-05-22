from agi_med_utils.dig_ass.db import make_session_id

def test_session_id():
    out = make_session_id()
    assert isinstance(out, str)
    assert len(out) == 12

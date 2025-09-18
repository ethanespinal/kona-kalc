from kona_kalc.planner import compute_leave_time

def test_basic_open_mode():
    h, m, ampm, br = compute_leave_time(
        shift_hour=5, shift_minute=30, shift_ampm="PM",
        truck_packed=False, to_job_location=25,
        ice_mode="open", shift_hours=6, shift_minutes=0
    )
    # just smoke checks
    assert ampm in ("AM", "PM")
    assert isinstance(h, int) and isinstance(m, int)
    assert br["freezers"] >= 1
    assert br["total"] > 0

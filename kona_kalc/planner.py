import math

def convert_to_24(hour: int, ampm: str) -> int:
    ampm = ampm.strip().lower()
    if ampm == "am":
        return 0 if hour == 12 else hour
    return 12 if hour == 12 else hour + 12

def compute_leave_time(
    shift_hour: int,
    shift_minute: int,
    shift_ampm: str,
    truck_packed: bool,
    to_job_location: int,
    ice_mode: str,
    shift_hours: int = 0,
    shift_minutes: int = 0,
    num_cups: int = 0,
    *,
    travel_to_warehouse: int = 15,
    pack_truck_time: int = 20,
    ice_time_per_freezer: int = 10,
    max_freezers: int = 3,
    arrive_early_minutes: int = 5,
    cups_per_freezer: int = 200,
):
    # target arrival = shift start - arrive_early
    target_hour = convert_to_24(shift_hour, shift_ampm)
    target_minute = shift_minute - arrive_early_minutes
    if target_minute < 0:
        target_minute += 60
        target_hour -= 1
        if target_hour < 0:
            target_hour += 24

    # how many freezers?
    ice_mode = (ice_mode or "").strip().lower()
    if ice_mode == "open":
        total_shift_hours = shift_hours + (shift_minutes / 60.0)
        num_freezers = min(math.ceil(total_shift_hours), max_freezers)
    elif ice_mode == "predetermined":
        num_freezers = min(math.ceil(num_cups / cups_per_freezer), max_freezers)
    else:
        num_freezers = 0

    ice_prep_time = num_freezers * ice_time_per_freezer

    total_time = travel_to_warehouse + to_job_location + ice_prep_time
    if not truck_packed:
        total_time += pack_truck_time

    # subtract from target
    leave_hour = target_hour
    leave_minute = target_minute - total_time
    while leave_minute < 0:
        leave_minute += 60
        leave_hour -= 1
        if leave_hour < 0:
            leave_hour += 24

    # format 12h output
    leave_ampm = "PM" if leave_hour >= 12 else "AM"
    display_hour = leave_hour % 12 or 12

    breakdown = {
        "warehouse": travel_to_warehouse,
        "pack": (0 if truck_packed else pack_truck_time),
        "to_job": to_job_location,
        "ice": ice_prep_time,
        "freezers": num_freezers,
        "total": total_time,
    }
    return display_hour, leave_minute, leave_ampm, breakdown

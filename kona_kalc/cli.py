import os
import sys
from .planner import compute_leave_time

# ---------- helpers ----------
def ask_int(prompt: str, min_val: int | None = None, max_val: int | None = None) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
            if min_val is not None and val < min_val:
                print(f"Enter ≥ {min_val}."); continue
            if max_val is not None and val > max_val:
                print(f"Enter ≤ {max_val}."); continue
            return val
        except ValueError:
            print("Please enter a whole number.")

def ask_choice(prompt: str, choices: list[str]) -> str:
    choices_norm = [c.lower() for c in choices]
    label = "/".join(choices)
    while True:
        v = input(f"{prompt} ({label}): ").strip().lower()
        if v in choices_norm:
            return v
        print(f"Choose one of: {', '.join(choices)}")

# ---------- cli ----------
def main():
    print("=== Kona Kalc (Shift Timing) ===")

    # shift start
    shift_hour = ask_int("Shift start hour (1-12): ", 1, 12)
    shift_minute = ask_int("Shift start minute (0-59): ", 0, 59)
    shift_ampm = ask_choice("AM or PM", ["AM", "PM"]).upper()

    # personal drive times
    minutes_home_to_warehouse = ask_int("Minutes from home to warehouse: ", 0, 600)

    # logistics
    packed_choice = ask_choice("Is the truck already packed?", ["y", "n"])
    truck_packed = (packed_choice == "y")

    to_job_location = ask_int("Minutes from warehouse to job site: ", 0, 600)

    # ice plan
    ice_mode = ask_choice("Ice mode", ["open", "predetermined"])
    shift_hours = shift_minutes = num_cups = 0
    if ice_mode == "open":
        shift_hours = ask_int("Shift length hours: ", 0, 24)
        shift_minutes = ask_int("Shift length minutes: ", 0, 59)
    else:  # predetermined
        num_cups = ask_int("How many cups are needed? ", 0, 1000000)

    # compute (override travel_to_warehouse with per-user input)
    h, m, ampm, br = compute_leave_time(
        shift_hour, shift_minute, shift_ampm,
        truck_packed, to_job_location, ice_mode,
        shift_hours, shift_minutes, num_cups,
        travel_to_warehouse=minutes_home_to_warehouse,
    )

    # output
    print("\nTime Breakdown:")
    print(f"• Drive to warehouse: {br['warehouse']} min")
    print(f"• Truck packing: {br['pack']} min")
    print(f"• Drive to job site: {br['to_job']} min")
    print(f"• Ice prep: {br['ice']} min ({br['freezers']} freezer(s))")
    print(f"• Total prep time: {br['total']} min")
    print(f"\nYou should leave your house at: {h}:{m:02d} {ampm}")

    # keep window open when double-clicking the PyInstaller .exe
    if getattr(sys, "frozen", False) and os.name == "nt" and not os.environ.get("KONA_KALC_NO_PAUSE"):
        try:
            input("\nPress Enter to exit...")
        except EOFError:
            pass

if __name__ == "__main__":
    main()

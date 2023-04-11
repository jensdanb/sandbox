import datetime as dt
from dataclasses import dataclass, field


@dataclass
class Shift:
    shift_day: dt.date
    start_time: dt.datetime
    end_time: dt.datetime
    duration: dt.timedelta = field(init=False)

    def __post_init__(self):
        self.duration = self.end_time - self.start_time


start_of_period = dt.datetime(2023, 5, 1, 0, 0)
end_of_period = start_of_period + dt.timedelta(weeks=4)


working_days = list(range(1, 28 + 1))
free_days = [5, 10, 13, 21, 23, 26, 28]
for free_day in free_days:
    working_days.remove(free_day)

shift_starts = [
    [16, 4], [16, 4], [10, 15], [10, 15], [16, 4], [16, 4],
    [11, 18], [11, 18], [16, 4], [16, 4], [10, 15],
    [5, 15], [5, 15], [16, 4], [11, 10], [11, 10], [10, 15],
    [4, 32], [4, 32], [5, 15], [5, 15]
]

shift_ends = [
    [24, 14], [24, 14], [17, 35], [17, 35], [24, 14], [24, 14],
    [21, 23], [21, 23], [24, 14], [24, 14], [17, 35],
    [11, 20], [11, 20], [24, 14], [11, 10], [11, 10], [17, 35],
    [10, 8], [10, 8], [11, 20], [11, 20]
]

shifts = {}  # day: shift  # day is number from 1 to 28. shift is a Shift object

for i in range(len(working_days)):
    day = working_days[i]
    start_time = start_of_period + dt.timedelta(days=day-1, hours=shift_starts[i][0], minutes=shift_starts[i][1])
    end_time = start_of_period + dt.timedelta(days=day-1, hours=shift_ends[i][0], minutes=shift_ends[i][1])
    shift_day = start_of_period + dt.timedelta(days=day-1)

    shifts[i] = Shift(shift_day=shift_day, start_time=start_time, end_time=end_time)
    # print(f'i: {i}, day: {day}, shift: {shifts[i]}')

# Rules
allowed_shift_duration = dt.timedelta(hours=9)
min_time_between_shifts = dt.timedelta(hours=11)
min_holiday_time = dt.timedelta(hours=35)
allowed_consecutive_days = 6
allowed_weekly_hours = dt.timedelta(hours=48)
allowed_consecutive_weekends = 1
average_workdays_per_week_shall_be = 5

if __name__ == '__main__':
    print(f'Working days: {working_days}')
    print(f'All shifts: {shifts}')
    print('-------------')

    print('-------------')
    print('Rule 1 violations: ')
    for s in shifts:
        shift = shifts[s]
        if shift.duration > allowed_shift_duration:
            print(f'Violation on shift {s} on day {shift.shift_day}: Duration {shift.duration} exceeds 9 hours')

    print('-------------')
    print('Rule 2 violations: ')
    for s in shifts:
        if s == 0:
            pass
        else:
            shift = shifts[s]
            last_shift = shifts[s-1]
            time_since_last_shift = shift.start_time - last_shift.end_time

            if time_since_last_shift < min_time_between_shifts:
                print(f'Violation on shift {s} on day {shift.shift_day}: Time since last shift {time_since_last_shift} is less than 11 hours')

    print('-------------')
    print('Rule 3 violations: ')
    for f in range(len(free_days) - 1):
        next_working_day = free_days[f] + 1
        next_shift = shifts[working_days.index(next_working_day)]
        last_shift = shifts[working_days.index(next_working_day) - 1]

        time_since_last_shift = next_shift.start_time - last_shift.end_time
        if time_since_last_shift < min_holiday_time:
            print(f'Violation on shift {next_working_day}: Time since start of holiday {time_since_last_shift} is less than 35 hours.')

    print('-------------')
    print('Rule 4 violations: ')
    for d in working_days[6:]:
        previous_6_days = range(d-6, d)
        if set(previous_6_days).isdisjoint(set(free_days)):
            print(f'Violation on day {d}: No holiday in the previous 6 days.')

    print('-------------')
    print('Rule 5 violations: ')
    week_start = start_of_period
    week_end = week_start + dt.timedelta(weeks=1)
    weekly_shifts = [shifts[s] for s in shifts if week_start <= shifts[s].shift_day < week_end]
    for w in range(4):

        weekly_shifts = [shifts[s] for s in shifts if week_start <= shifts[s].shift_day < week_end]
        durations = [shift.duration for shift in weekly_shifts]
        total_weekly_duration = dt.timedelta()
        for duration in durations:
            total_weekly_duration += duration
        # print(f'Work hours in week {w}: {total_weekly_duration}')
        if total_weekly_duration > allowed_weekly_hours:
            print(f'Violation found: Weekly hours {total_weekly_duration} exceed 48 hours')
        week_start = week_end
        week_end = week_start + dt.timedelta(weeks=1)

    print('-------------')
    print('Rule 6 violations: ')

    """
    shift_calendar = calendar.Calendar()
    for day in shift_calendar.iterweekdays():
        print(f'Day is {day}')
    
    print(f'Calendar is {shift_calendar}')
    """
from datetime import date, datetime, timedelta
from dataclasses import dataclass, field


@dataclass
class Shift:
    shift_day: date
    start_time: datetime
    end_time: datetime
    duration: timedelta = field(init=False)

    def __post_init__(self):
        self.duration = self.end_time - self.start_time


# Shift calendar setup
start_of_period = datetime(2023, 5, 1, 0, 0)
end_of_period = start_of_period + timedelta(weeks=4)

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
    [11, 20], [11, 20], [24, 14], [21, 23], [21, 23], [17, 35],
    [10, 8], [10, 8], [11, 20], [11, 20]
]

shifts = {}
for i in range(len(working_days)):
    day = working_days[i]
    start_time = start_of_period + timedelta(days=day-1, hours=shift_starts[i][0], minutes=shift_starts[i][1])
    end_time = start_of_period + timedelta(days=day-1, hours=shift_ends[i][0], minutes=shift_ends[i][1])
    shift_day = start_of_period + timedelta(days=day-1)

    shifts[i] = Shift(shift_day=shift_day, start_time=start_time, end_time=end_time)
    # print(f'i: {i}, day: {day}, shift: {shifts[i]}')

# Rules
allowed_shift_duration = timedelta(hours=9)
min_time_between_shifts = timedelta(hours=11)
min_holiday_time = timedelta(hours=35)
allowed_consecutive_days = 6
allowed_weekly_hours = timedelta(hours=48)
allowed_consecutive_weekends = 1
average_workdays_per_week_shall_be = 5


def rule_1(allowed_shift_duration, shifts):
    print('-------------')
    print('Regel 1 brudd: ')
    for s in shifts:
        shift = shifts[s]
        if shift.duration > allowed_shift_duration:
            print(f'Regelbrudd på skift {s + 1}: Varighet {shift.duration} overstiger 9 timer.')


def rule_2(min_time_between_shifts, shifts):
    print('-------------')
    print('Regel 2 brudd: ')
    for s in shifts:
        if s == 0:
            pass
        else:
            shift = shifts[s]
            previous_shift = shifts[s - 1]
            time_since_last_shift = shift.start_time - previous_shift.end_time

            if time_since_last_shift < min_time_between_shifts:
                print(f'Regelbrudd på skift {s + 1}: Tid siden forrige skift; {time_since_last_shift}, er under 11 timer')


def rule_3(min_holiday_time, free_days, working_days):
    print('-------------')
    print('Regel 3 brudd: ')
    for f in range(len(free_days) - 1):
        next_working_day = free_days[f] + 1
        next_shift = shifts[working_days.index(next_working_day)]
        previous_shift = shifts[working_days.index(next_working_day) - 1]
        time_since_last_shift = next_shift.start_time - previous_shift.end_time

        if time_since_last_shift < min_holiday_time:
            print(f'Regelbrudd på dag {next_working_day}: Tid siden forrige skift; {time_since_last_shift}, er under 35 timer.')


def rule_4(allowed_consecutive_days, working_days):
    print('-------------')
    print('Regel 4 brudd: ')
    for d in working_days[allowed_consecutive_days:]:
        previous_6_days = range(d-allowed_consecutive_days, d)
        if set(previous_6_days).isdisjoint(set(free_days)):
            print(f'Regelbrudd på dag {d}: Arbeidsdag uten noen fridag de foregående {allowed_consecutive_days} dagene.')


def rule_5(allowed_weekly_hours, week_start, shifts):
    print('-------------')
    print('Regel 5 brudd: ')
    week_end = week_start + timedelta(weeks=1)
    for w in range(4):
        weekly_shifts = [shifts[s] for s in shifts if week_start <= shifts[s].shift_day < week_end]
        durations = [shift.duration for shift in weekly_shifts]
        total_weekly_duration = timedelta()
        for duration in durations:
            total_weekly_duration += duration
        if total_weekly_duration > allowed_weekly_hours:
            print(f'Regelbrudd på uke {w + 1}: Arbeidstid {total_weekly_duration.total_seconds()/3600} timer overstiger 48 timer.')
        week_start = week_end
        week_end = week_start + timedelta(weeks=1)


def rule_6(working_days):
    print('-------------')
    print('Regel 6 brudd: ')
    weekend_days = [6, 7]
    working_weekends = []
    for w in range(4):
        if not set(weekend_days).isdisjoint(set(working_days)):
            if working_weekends and working_weekends[-1] is True:
                print(f'Regelbrudd på uke {w + 1}: Jobber helg både uke {w} og uke {w + 1}.')
            working_weekends.append(True)
        else:
            print(f'Ingen helgejobbing uke {w}')
            working_weekends.append(False)
        weekend_days = [old_value + 7 for old_value in weekend_days]


def rule_7(average_workdays_per_week_shall_be, working_days, allowed_deviance=0.0):
    print('-------------')
    print('Regel 7 brudd: ')
    average_workdays_per_week = len(working_days) / 4
    allowed_range = [average_workdays_per_week_shall_be * (1-allowed_deviance), average_workdays_per_week_shall_be * (1+allowed_deviance)]
    if not allowed_range[0] <= average_workdays_per_week <= allowed_range[1]:
        print(f'Regelbrudd på gjennomsnittlig arbeidsdager! Gjennomsnittet på {average_workdays_per_week} per uke er utenfor tillatte grenser: {allowed_range}.')

if __name__ == '__main__':
    rule_1(allowed_shift_duration, shifts)
    rule_2(min_time_between_shifts, shifts)
    rule_3(min_holiday_time, free_days, working_days)
    rule_4(allowed_consecutive_days, working_days)
    rule_5(allowed_weekly_hours, start_of_period, shifts)
    rule_6(working_days)
    rule_7(average_workdays_per_week_shall_be, working_days, allowed_deviance=0.1)
import random

minutes = 40

for i in range(100):
    time_in_seconds = minutes * 60

    time_sleep = (time_in_seconds * 0.333)

    min_time = 300

    max_time = time_sleep + random.choice([-180, 180])

    if time_sleep > max_time:
        time_sleep, max_time = max_time, time_sleep

    time_end = random.randint(int(time_sleep), int(max_time))

    if time_end < min_time:
        time_end = 300 + random.randint(1, 180)

    print(time_end / 60, "минут")

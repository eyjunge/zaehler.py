import datetime as dt
def time_calc():
    now = dt.datetime.now()
    for i in range(1000000000):
        n = i + i
    then = dt.datetime.now()
    return(then-now).total_seconds()

print(time_calc())
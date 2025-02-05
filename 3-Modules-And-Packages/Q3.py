import datetime
from dateutil.relativedelta import relativedelta
import itertools

def datecount(start, step):
    
    step = step.lower()
    
    # For Monthly, Quarterly & Yearly, using relativedelta to calculate months instead of days.
    step_dict = {
        'alternative': 2,
        'daily': 1,
        'weekly': 7,
        'monthly': 1,  # 1 month = month
        'quarterly': 3,  # 3 months = quarter
        'yearly': 12 # 12 months = year
    }
    
    if step not in step_dict:
        raise ValueError("Invalid step. Choose from 'alternative', 'daily', 'weekly', 'monthly', 'quarterly', or 'yearly'.")
    
    Days=['daily','weekly','alternative']

    if step in Days:
        step_days = step_dict[step]
        while True:
            yield start
            start += datetime.timedelta(days=step_days)
    else:
        step_days=step_dict[step]
        while True:
            yield start
            start+=relativedelta(months=step_days)


step=str(input("Enter the step: "))
dc = datecount(start=datetime.date.today(), step=step)

for _ in range(10):
    print(next(dc))


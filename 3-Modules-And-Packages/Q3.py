import datetime
import itertools

def datecount(start, step):
    
    step = step.lower()
    
    step_dict = {
        'alternative': 2,
        'daily': 1,
        'weekly': 7,
        'monthly': 30,  # Approximation
        'quarterly': 91,  # Approximate 3 months
        'yearly': 365
    }
    
    if step not in step_dict:
        raise ValueError("Invalid step. Choose from 'alternative', 'daily', 'weekly', 'monthly', 'quarterly', or 'yearly'.")

    step_days = step_dict[step]
    while True:
        yield start
        start += datetime.timedelta(days=step_days)

step=str(input("Enter the step: "))
dc = datecount(start=datetime.date.today(), step=step)

for _ in range(10):
    print(next(dc))


"""Q3) Read about itertools.count(start=0, step=1) function which accepts options arguments  
start and end.
Based on this, implement a similar `datecount(start, step)`
where start is a  `datetime.date`  object and 
step  can we string values 'alternative', 'daily',  'weekly', 'monthly',   'Quarterly', 'yearly' 
(ignore case)

example execution:
>> dc = datecount(step='weekly')
>> for i in range(10):
    	print (next(dc))"""


import datetime
from dateutil.relativedelta import relativedelta
import itertools

def datecount(start, step):

    #To streamline word-casing
    step = step.lower()
    
    # For Monthly, Quarterly & Yearly, using relativedelta to calculate months instead of days.
    step_dict = {
        'alternative': 2,
        'daily': 1,
        'weekly': 7,
        'monthly': 1,  # 1 month = month //for relativedelta
        'quarterly': 3,  # 3 months = quarter //for relativedelta
        'yearly': 12 # 12 months = year //for relativedelta
    }
    #Edge-case to raise error if appropriate step not specified
    if step not in step_dict:
        raise ValueError("Invalid step. Choose from 'alternative', 'daily', 'weekly', 'monthly', 'quarterly', or 'yearly'.")
    
    Days=['daily','weekly','alternative']

    #Iterating to check if steps specified can be calculated using timedelta or relativedelta
    if step in Days:
        step_days = step_dict[step]
        while True:
            yield start
            start += datetime.timedelta(days=step_days)

    #Used relativedelta to ensure proper dates are taken, if days are hard-coded, it is prone to errors like leap-years
    else:
        step_days=step_dict[step]
        while True:
            yield start
            start+=relativedelta(months=step_days)


step=str(input("Enter the step: "))
dc = datecount(start=datetime.date.today(), step=step)

for _ in range(10):
    print(next(dc))


from datetime import datetime, timedelta, date
month_now = date.today()
one_month_ago = date.today() - timedelta(days=30)

print(one_month_ago, month_now)
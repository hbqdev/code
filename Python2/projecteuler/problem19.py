30month = [April, June, September, November]
31month = [Jan, March, May, July, August, October, December]
months = [Jan, Feb, March, April, May, June, July, August, September, October, November, Decemter]

def numdays(year, month) :
  days = 0;
  if month in 30month:
    days = 30
  elif month in 31month:
    days = 31
  elif month == "Feb" and year/4 ==0:
    days = 29
  else:
    days = 28
  return days

sunday = 0;
ndays = 1;

for i in range(1900, 2000):
  for x in len(months):
    days = numdays(i,months[x])
    
      
    
 

import grequests
import itertools
import re
import json

file_handle = open('session.txt', 'r')

if file_handle:
    cookies = json.loads(file_handle.read())

else:
    print('Error logging in.')
    exit()

file_handle.close()

rs = (grequests.get(f'https://mbasic.facebook.com/events/ajax/dashboard/calendar/birthdays/?cursor=2020-{month:02d}-01'
                    , cookies=cookies)
      for month in range(1, 13))

birthdays_requests = grequests.map(rs)
birthdays_string = ''.join([request.text for request in birthdays_requests])

dates = re.findall('[a-zA-Z]+, [a-zA-Z]+ [0-9]+, [0-9]{4}', birthdays_string)
persons = re.findall(r'alt=\\"(.*?)\\"', birthdays_string)

for (date, person) in itertools.zip_longest(dates, persons):
    print(f'{date} - {person}')
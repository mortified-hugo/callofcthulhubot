import re
import requests
from bs4 import BeautifulSoup


def check_date(log_date):
    if int(log_date[0]) <= 0 or int(log_date[0]) > 12:
        return True
    elif int(log_date[1]) <= 0 or int(log_date[1]) > 31:
        return True
    elif int(log_date[0]) in [2, 4, 6, 9, 11] and int(log_date[1]) == 31:
        return True
    elif int(log_date[0]) == 2 and int(log_date[1]) == 30:
        return True
    else:
        return False


def check_end_month(log_date):
    if int(log_date[0]) in [1, 3, 7, 8, 10, 12]:
        if int(log_date[1]) == 31:
            return True
        else:
            return False
    elif int(log_date[0]) in [4, 6, 9, 11]:
        if int(log_date[1]) == 30:
            return True
        else:
            return False
    elif int(log_date[0]) == 2:
        if int(log_date[2]) % 4 == 0 and (int(log_date[2]) % 100 != 0 or int(log_date[2]) % 400 == 0):
            if log_date[1] == 29:
                return True
            else:
                return False
        else:
            if log_date[1] == 28:
                return True
            else:
                return False


def get_date(date):
    rex = re.compile("^[0-9]{2}[/][0-9]{2}[/][0-9]{4}$")
    if not rex.match(date):
        response = 'Wrong Format for the date, please enter MM/DD/YYYY'
    else:
        log = date.split('/')
        months = {'01': 'January', '02': 'February', '03': 'March', '04': 'April',
                  '05': 'May', '06': 'June', '07': 'July', '08': 'August',
                  '09': 'September', '10': 'October', '11': 'November', '12': 'December'}
        if check_date(log):
            response = 'Wrong date, be sure to use the MM/DD/YYYY format'
        else:
            log[1] = (str(int(log[1])))
            next_day = str(int(log[1]) + 1)
            url = f"https://en.wikipedia.org/wiki/{months[log[0]]}_{log[2]}"
            r = requests.get(url)
            soup = BeautifulSoup(r.text, features='html.parser')
            if check_end_month(log):
                end_point = 'References'
            else:
                end_point = f"{months[log[0]]} {next_day}, {log[2]} ("
            info = soup.text[soup.text.rfind(f"{months[log[0]]} {log[1]}, {log[2]} (")
                             : soup.text.rfind(end_point)]
            response = re.sub("[\[].*?[\]]", "", info)
            if response == '':
                response = "Something odd happened, maybe wikipedia does't have info on that month or that day"
            elif len(response) > 2000:
                response = response[:1990] + '...'
    return response


success = []
failure = []

for year in range(1900, 2001):
    response = get_date(f'01/01/{str(year)}')
    if response == "Something odd happened, maybe wikipedia does't have info on that month or that day":
        failure.append(year)
    else:
        success.append(year)

print(success)
print(len(success))
print(failure)
print(len(failure))

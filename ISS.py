import smtplib
import threading
import requests
import datetime
import time
import os

# Watch the ISS live while you wait! https://www.youtube.com/watch?v=jPTD2gnZFUw

# I am currently running this on the free tier of https://www.pythonanywhere.com/
# crazy easy and simple to set up.

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# if your going to use the email function create a burner email that you wont use for other shit.
my_email = 'A EMAIL'
password = 'A PASSWORD'
# Lat and Long go here
my_lat = 'YOUR LAT'
my_long = 'YOUR LONG'
# constantly compare position using ISS API
def check_position():
    clear_console()
    response_iss = requests.get(url='http://api.open-notify.org/iss-now.json')
    response_iss.raise_for_status()

    data = response_iss.json()

    iss_lng = float(data['iss_position']['longitude'])
    iss_lat = float(data['iss_position']['latitude'])
    time_now = datetime.datetime.now()
    # nested function to send email when close
    def send_email(position):
        connection = smtplib.SMTP('smtp.gmail.com')
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            # Below put the email it will send to, probably yourself.
            to_addrs='The email you will send it to',
            msg=f'Subject:ISS Space Station Is Close\n\n{position}.\n ISS Position: Current'
                f' lng = {iss_lng}, Current lat = {iss_lat}\n Your Position: Home lng = {my_long}, Home lat = {my_lat}'
        )
        print('EMAIL HAS BEEN SENT')

# where it checks
    if my_lat - 5 <= iss_lat <= my_lat + 5 and my_long - 5 <= iss_lng <= my_long + 5:
        print(f'She is getting close. {time_now}')
        print(f'ISS Position: Current lng = {iss_lng}, Current lat = {iss_lat}')
        print(f'Your Position: Home lng = {my_long}, Home lat = {my_lat}')
        send_email('The ISS Space Station is Close')
    elif my_lat - 2 <= iss_lat <= my_lat + 2 and my_long - 2 <= iss_lng <= my_long + 2:
        print(f'She is right above you! {time_now}')
        print(f'ISS Position: Current lng = {iss_lng}, Current lat = {iss_lat}')
        print(f'Your Position: Home lng = {my_long}, Home lat = {my_lat}')
        send_email('The ISS Space Station is Right Above You')
    elif iss_lng == my_long and iss_lat == my_lat:
        print(f'She is DIRECTLY above you! {time_now}')
        print(f'ISS Position: Current lng = {iss_lng}, Current lat = {iss_lat}')
        print(f'Your Position: Home lng = {my_long}, Home lat = {my_lat}')
        send_email('The ISS Space Station is DIRECTLY Above You')
    else:
        print(f'Keep Waiting! {time_now}')
        print(f'ISS Position: Current lng = {iss_lng}, Current lat = {iss_lat}')
        print(f'Your Position: Home lng = {my_long}, Home lat = {my_lat}')
#keeps it checking over and over
def run_at_intervals():
    threading.Timer(10.0, run_at_intervals).start()
    check_position()

run_at_intervals()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")




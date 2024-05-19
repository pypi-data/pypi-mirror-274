import time as tmi
import os
import subprocess as sp
from tkinter import messagebox as mb

# time_type - sec || mlsec
# language - en || ru

def stop_of_time(stop_time, time_type='sec'):
    if time_type == 'sec':
        tmi.sleep(stop_time)
    elif time_type == 'mlsec':
        tmi.sleep(stop_time / 1000)

def stop_of_key():
    os.system('pause')

def fake_loading(process=100, time=0.5, symbol="|", language='en'):
    if language == 'ru':
        for i in range(process+1):
            stop_of_time(time)
            print(f"\rЗагрузка: {i*symbol} {i}%", end='')

    elif language == 'en':
        for i in range(process+1):
            stop_of_time(time)
            print(f"\rLoading: {i*symbol} {i}%", end='')

def shell(command):
    sp.run(command, shell=True)

def error_message(title, text):
    mb.showerror(str(title), str(text))

def info_message(title, text):
    mb.showinfo(str(title), str(text))

def register(language='ru', loading=True, message=True, count=1):
    array_login = []
    array_password = []
    all_return = {}

    if language == 'ru':
        for i in range(count):
            login = input('Введите логин: ')
            password = input('Введите пароль: ')

            array_login.append(login)
            array_password.append(password)

            if loading: fake_loading(language='ru')
            if message: print('Регитрация успешно завершена.')

    elif language == 'en':
        for i in range(count):
            login = input('Enter the login: ')
            password = input('Enter the password: ')

            array_login.append(login)
            array_password.append(password)

            if loading: fake_loading(language='en')
            if message: print('Registration completed successfully.')

    all_return['logins'] = array_login
    all_return['passwords'] = array_password
    return all_return

def login(logins, language='ru', loading=True, count=1): 
    array_login = logins["login"]
    array_password = logins["password"]

    array_loginf = []
    array_passwordf = []

    all_return = {}

    if language == 'ru':
        for i in range(count):
            login = str(input('Введите логин: '))
            password = str(input('Введите пароль: '))
            if login in array_login:
                passwordf = array_password[array_login.index(login)]
                # найти пароль по логину
                if password == passwordf:
                    array_loginf.append(login)
                    array_passwordf.append(password)
                    print('Вы успешно вошли.')
                    print()
                else:
                    array_loginf.append('False')
                    array_passwordf.append('False')
                    print('Неправильный логин или пароль.')
                    print()
            else:
                array_loginf.append('False')
                array_passwordf.append('False')
                print('Неправильный логин или пароль.')

            if loading: fake_loading(language='ru')

    if language == 'en':
        for i in range(count):
            login = input('Enter the login: ')
            password = input('Enter the password: ')

            if login in array_login:
                # найти пароль по логину
                find_password = array_password[array_login.index(login)]
                if password == find_password:
                    array_loginf.append(login)
                    array_passwordf.append(password)
                    print('You have successfully logged in.')
                    print()

                else:
                    array_loginf.append('False')
                    array_passwordf.append('False')
                    print('Incorrect username or password.')
                    print()

            else:
                array_loginf.append('False')
                array_passwordf.append('False')
                print('Incorrect username or password.')

            if loading: fake_loading(language='ru')

    all_return['logins'] = array_loginf
    all_return['passwords'] = array_passwordf

    return all_return
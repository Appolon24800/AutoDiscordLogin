import os
import traceback

import requests
import json
import os
import getpass



def discordapierror(data) -> str:
    errors = data.get('errors')
    if not errors:
        return "Invalid data"

    login = errors.get('login', {"_errors": "Invalid responce from discord"}).get('_errors', [])
    if not login:
        return "Invalid data"

    if errors.get('login', {}).get('_errors', []):
        return f"{login[0].get('message')}"


while True:
    os.system('cls')
    print('\n  This software was made by Appolon for get your discord token.\n  If you don\'t trust this file or the person that give it to you, you can find the source code here\n  --> https://github.com/Appolon24800/AutoDiscordLogin\n')
    mail = input('Mail> ')
    if '@' not in mail:
        print('Invalid mail')
        input()
        break
    password = getpass.getpass(prompt='Password> ')

    r = requests.post('https://discord.com/api/v9/auth/login', headers={'Content-Type': 'application/json'}, data=json.dumps({"login": mail, "password": password, "undelete": False, "login_source": None, "gift_code_sku_id": None}))
    if r.status_code == 200:
        if r.json().get("token"):
            print(f'Token: {r.json().get("token")}')
            input()
            break
        if r.json().get('totp', False) and r.json().get('sms', False):
            otp = str(input('(avoid sms) TOTP or SMS> '))
            if otp.lower() == 'sms':
                smsotpsend = requests.post('https://discord.com/api/v9/auth/mfa/sms/send', headers={'Content-Type': 'application/json'}, data=json.dumps({"ticket": r.json().get('ticket')}))
                while True:
                    totp = input(f'{smsotpsend.json()["phone"]} SMS> ')
                    if not totp or len(str(totp)) != 6 or not totp.isdigit():
                        print('Invalid code')
                        break

                smsotp = requests.post('https://discord.com/api/v9/auth/mfa/sms', headers={'Content-Type': 'application/json'}, data=json.dumps({"code": int(totp), "ticket": r.json().get("ticket"), "login_source": None, "gift_code_sku_id": None}))

                if smsotp.status_code == 200:
                    print(f'Token: {smsotp.json().get("token")}')
                    input()
                    break
                elif smsotp.status_code == 400:
                    print(discordapierror(smsotp.json()))
                    input()
                else:
                    print(smsotp.text)
            elif otp.lower() == 'totp':
                while True:
                    totp = input('TOTP> ')
                    if not totp or len(str(totp)) != 6 or not totp.isdigit():
                        print('Invalid code')
                    break

                rtotp = requests.post('https://discord.com/api/v9/auth/mfa/totp',
                                      headers={'Content-Type': 'application/json'}, data=json.dumps(
                        {"code": totp, "ticket": r.json().get('ticket'), "login_source": None,
                         "gift_code_sku_id": None}))

                if rtotp.status_code == 200:
                    print(f'Token: {rtotp.json().get("token")}')
                    input()
                    break
                elif rtotp.status_code == 400:
                    print(discordapierror(rtotp.json()))
                    input()
                else:
                    print(rtotp.text)


            else:
                print(r.text)
                print('You have a security key')
                print('Please remove it if you want to continue')
                input()


        elif r.json().get('totp'):

            while True:
                totp = input('TOTP> ')
                if not totp.isdigit() or len(str(totp)) != 6:
                    print('Invalid code')
                break

            rtotp = requests.post('https://discord.com/api/v9/auth/mfa/totp', headers={'Content-Type': 'application/json'}, data=json.dumps({"code": totp, "ticket": r.json().get('ticket'), "login_source": None, "gift_code_sku_id": None}))

            if rtotp.status_code == 200:
                print(f'Token: {rtotp.json().get("token")}')
                input()
                break
            elif rtotp.status_code == 400:
                print(discordapierror(rtotp.json()))
                input()

        elif r.json().get('sms'):
            print('SMS')

        else:
            print(r.text)
            print('You have a security key')
            print('Please remove it if you want to continue')
            input()

    elif r.status_code == 400:
        print(discordapierror(r.json()))
        input()

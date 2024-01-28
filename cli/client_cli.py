### Libery
import os
import time
import socket
import random
from unidecode import unidecode
import re
import string
from random_username.generate import generate_username
import sys
import errno
import platform


### Config
main_server_ip = "localhost"
main_server_port = 12345
chat_server_ip = "localhost"
chat_server_port = 12346
app_version = "1.0.0"
header_lenght = 999999
notify_time = 2


### Functions
# Password/Username Ruls Check
def pass_user_check(_username, _password):
    _final = False
    if _username != None:
        if len(_username) >= 3 and unidecode(_username) == _username:
            _final = True
        else:
            _final = False
    if _password != None:
        if len(_password) >= 10 and unidecode(_password) == _password and re.search(r'\d', _password) and re.search(r'[A-Z]', _password) and re.search(r'[a-z]', _password) and re.search(r'[^\w\s]', _password):
            _final = True
        else:
            _final = False
    return _final
# Server Contact
def server_contact(send_msg):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_connect:
        server_connect.connect((main_server_ip, main_server_port))
        server_connect.sendall((send_msg).encode())
        time.sleep(2)
        global server_data
        server_data = server_connect.recv(1024).decode()
        time.sleep(1)
# Reset
def reset(log_panel, funkcie, ucet):
    global server_data, _verify_gen, verify, hl_prompt, sl_prompt, server_data_list, _link, _aprove, _password, _username, _password_cur, _password_new, _password_aga, _od, _do, __lenght, _lenght, username_list, publick_ip, private_ip, log_prompt, reg_user, reg_pass, _reg_pass, reg_invite
    if log_panel: log_prompt = reg_user = reg_pass = _reg_pass = reg_invite = None
    if funkcie: _od = _do = __lenght = _lenght = username_list = publick_ip = private_ip = None
    if ucet: _password = _username = _password_cur = _password_new = _password_aga = None
    server_data = _verify_gen = verify = hl_prompt = sl_prompt = server_data_list = _link = _aprove = None
# Web Ping
def web_ping(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except:
        return False
# Clear
def clear():
    if platform.system() == "Linux": os.system("clear")
    elif platform.system() == "Windows": os.system("cls")
    else: exit()


### Server and update checker
print(f"Atomic Private Comunity - Chat\nLoading...")
server_contact(f"VERSION,{app_version}")
if not "TRUE" in server_data:
    clear()
    print(f"Atomic Private Comunity - {app_version}\nYou don't have the current version of the app!\nThe new version can be found at {server_data}")
    input()
    exit()


### Log Panel
while True:
    reset(True, False, False)
    clear()
    print(f"Atomic Private Comunity - {app_version}\n1|Login\n2|Register\n3|Exit")
    log_prompt = input("Choose an option: ")
    clear()
    ### Login
    if log_prompt == "1":
        print(f"Atomic Private Comunity - Login")
        log_user = input("Username: ")
        log_pass = input("Password: ")
        _verify_gen = random.randint(11111111, 99999999)
        verify = input(f"Verification code ({_verify_gen}): ")
        if verify == str(_verify_gen):
            if pass_user_check(log_user, log_pass):
                server_contact(f"LOGIN,{log_user},{log_pass}")
                if server_data in "TRUE":
                    print("You were logged in!")
                    time.sleep(notify_time)
                    break
                else:
                    print("Password or username is incorrect!")
                    time.sleep(notify_time)
            else:
                print("Password or username is incorrect!")
                time.sleep(notify_time)
        else:
            print("Verification code is not correct!")
            time.sleep(notify_time)
        reset(True, False, False)

    ### Register
    elif log_prompt == "2":
        print(f"Atomic Private Comunity - Register\nThe name must contain at least 3 characters\nThe password must contain:\n    - Minimum 10 characters\n    - No diacritics\n    - 1 special character\n    - 1 capital letter\n    - 1 lowercase letter\n    - 1 number")
        reg_user = input("Username: ")
        reg_pass = input("Passowrd: ")
        _reg_pass = input("Password Again: ")
        reg_invite = input("Invitation: ")
        _verify_gen = random.randint(11111111, 99999999)
        verify = input(f"Verification Code ({_verify_gen}): ")
        if verify == str(_verify_gen):
            if len(reg_invite) == 20 and reg_pass == _reg_pass and pass_user_check(reg_user, reg_pass):
                server_contact(f"REGISTER,{reg_user},{reg_pass},{reg_invite}")
                if server_data in "TRUE":
                    print("You have been registered!")
                elif server_data in "FALSE-USER":
                    print("The username is already registered!")
                elif server_data in "FALSE-INVITE":
                    print("Invitation does not exist!")
                time.sleep(notify_time)
            else:
                print("Password or username is incorrect!")
                time.sleep(notify_time)
        else:
            print("Verification code is not correct!")
            time.sleep(notify_time)
        reset(True, False, False)

    ### Exit
    elif log_prompt == "3": exit()


### Second Functions
# Publick Chat
def publik_chat():
    print("Connecting to a chat room...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_connect:
        server_connect.connect((chat_server_ip, chat_server_port))
        server_connect.setblocking(False)
        client_username = log_user.encode("utf-8")
        client_username_header = f"{len(client_username):<{header_lenght}}".encode("utf-8")
        server_connect.send(client_username_header + client_username)
        os.system("clear")
        print("Atomic Private Comunity - Chat\nTo refresh your chat messages, press ENTER\nTo exit the chat, type !ex")
        while True:
            _message = input(f"{client_username} > ")
            if _message == "!ex":
                break
            else:
                if _message:
                    _message = _message.encode("utf-8")
                    _message_header = f"{len(_message):<{header_lenght}}".encode("utf-8")
                    server_connect.send(_message_header + _message)
                try:
                    while True:
                        client_username_header = server_connect.recv(header_lenght)
                        if not len(client_username_header):
                            print("The connection was dropped by the server!")
                            time.sleep(notify_time)
                            sys.exit()
                        client_username_length = int(client_username_header.decode("utf-8").strip())
                        client_username = server_connect.recv(client_username_length).decode("utf-8")
                        _message_header = server_connect.recv(header_lenght)
                        _message_length = int(_message_header.decode("utf-8").strip())
                        _message = server_connect.recv(_message_length).decode("utf-8")
                        print(f"{client_username} > {_message}")
                except IOError as e:
                    if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                        print(f"Error readings: {str(e)}")
                        time.sleep(notify_time)
                        sys.exit()
                    continue
                except Exception as e:
                    print(f"Error readings: {str(e)}")
                    sys.exit()
                    time.sleep(notify_time)


### Hlavný Panel
reset(True, True, True)
while True:
    clear()
    print(f"Atomic Private Comunity - {app_version}\n1|Chat\n2|Data\n3|Features\n4|Information\n5|Account\n6|Exit")
    hl_prompt = input("> ")
    clear()
    ### Chat
    if hl_prompt == "1":
        reset(False, False, False)
        publik_chat()
    ### Data
    elif hl_prompt == "2":
        print("Atomic Private Comunity - Data\n1|Links\n2|Link Request\n3|Markets\n4|Market Request")
        sl_prompt = input("> ")
        clear()
        # Data - Links
        if sl_prompt == "1":
            print("Atomic Private Comunity - Links\nLoading links...")
            server_contact("LINK-SHOW")
            print("Links:")
            if server_data == "None":
                print("Nothing")
            else:
                server_data_list = list(map(lambda x: x[0], eval(server_data)))
                for i in range(len(server_data_list)):
                    print(f"{i}|{server_data_list[i]}")
            input()
            reset(False, False, False)
        # Data - Link Request
        elif sl_prompt == "2":
            print("Atomic Private Comunity - Link Request")
            _link = input("Link: ")
            _verify_gen = random.randint(11111111, 99999999)
            verify = input(f"Verification code ({_verify_gen}): ")
            _aprove = input("Would you like to send your application? [Y/n]: ")
            if _aprove == "Y" or _aprove == "y":
                print("Verification...")
                if verify == str(_verify_gen):
                    if _link != None or len(_link) <= 6 and web_ping(_link):
                        print("Verified by!")
                        print("I send...")
                        server_contact(f"LINK-REQ,{log_user},{_link}")
                        if server_data == "FALSE-R-EXIST":
                            print("This link has already been requested to be added!")
                        elif server_data == "FALSE-L-EXIST":
                            print("Link already exists!")
                        else:
                            print("Sent, you have to wait for approval before the link can be published.")
                        time.sleep(notify_time)
                    else:
                        print("Link does not exist!")
                        time.sleep(notify_time)
                else:
                    print("Verification code is not correct!")
                    time.sleep(notify_time)
            reset(False, False, False)
        # Data - Markets
        elif sl_prompt == "3":
            print("Atomic Private Comunity - Markets\nLoading markets...")
            server_contact("MARKET-SHOW")
            print("Markets:")
            if server_data == "None":
                print("Nothing")
            else:
                server_data_list = list(map(lambda x: x[0], eval(server_data)))
                for i in range(len(server_data_list)):
                    print(f"{i}|{server_data_list[i]}")
            input()
            reset(False, False, False)
        # Data - Market Request
        elif sl_prompt == "4":
            print("Atomic Private Comunity - Market Request")
            _link = input("Link: ")
            _verify_gen = random.randint(11111111, 99999999)
            verify = input(f"Verification code ({_verify_gen}): ")
            _aprove = input("Would you like to send your application? [Y/n]: ")
            if _aprove == "Y" or _aprove == "y":
                print("OveroVerificationvanie...")
                if verify == str(_verify_gen):
                    if _link != None or len(_link) <= 6 and web_ping(_link):
                        print("Verified by!")
                        print("I send...")
                        server_contact(f"MARKET-REQ,{log_user},{_link}")
                        if server_data == "FALSE-R-EXIST":
                            print("The addition of this market has already been requested!")
                        elif server_data == "FALSE-L-EXIST":
                            print("Market already exists!")
                        else:
                            print("Sent, you have to wait for approval before the market can be published.")
                        time.sleep(notify_time)
                    else:
                        print("Link does not exist!")
                        time.sleep(notify_time)
                else:
                    print("Verification code is not correct!")
                    time.sleep(notify_time)
            reset(False, False, False)
    ### Features
    elif hl_prompt == "3":
        print(f"Atomic Private Comunity - Features\n1|Number Generator\n2|Password Generator\n3|Username Generator\n4|IP Generator")
        sl_prompt = input("> ")
        clear()
        # Funkcie - Number Generator
        if sl_prompt == "1":
            print("Atomic Private Comunity - Number Generator")
            _od = input("From: ")
            _do = input("To: ")
            _lenght = input("How many numbers: ")
            if _od.isdigit() and _do.isdigit() and _lenght.isdigit():
                print("Generating...")
                for i in range(int(_lenght)):
                    print(f"{i}|{random.randint(int(_od), int(_do))}")
                print("Generated by!")
                input()
            else:
                print("You must enter the numbers!")
                time.sleep(3)
            reset(False, True, False)
        # Funkcie - Password Generator
        elif sl_prompt == "2":
            print("Atomic Private Comunity - Password Generator")
            _lenght = input("Length: ")
            __lenght = input("How many numbers: ")
            if _lenght.isdigit() and __lenght.isdigit():
                print("Generating...")
                for i in range(int(__lenght)):
                    pass_char = string.ascii_letters + string.digits
                    pass_gen = ''.join(random.choice(pass_char) for i in range(int(_lenght)))
                    print(f"{i}|{pass_gen}")
                print("Generated by!")
                input()
            else:
                print("You must enter the numbers!")
                time.sleep(3)
            reset(False, True, False)
        # Funkcie - Username Generator
        elif sl_prompt == "3":
            print("Atomic Private Comunity - Username Generator")
            _lenght = input("How many:")
            if _lenght.isdigit():
                print("Generating...")
                username_list = generate_username(int(_lenght))
                for i in range(len(username_list)):
                    print(f"{i}| {username_list[i]}")
                print("Generated by!")
                input()
            else:
                print("You must enter the numbers!")
                time.sleep(3)
            reset(False, True, False)
        # Funkcie - IP Generator
        elif sl_prompt == "4":
            print("Atomic Private Comunity - IP Generator")
            _lenght = input("Koľko:")
            if _lenght.isdigit():
                print("Generating...")
                for i in range(int(_lenght)):
                    publick_ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
                    private_ip = "10." + ".".join(str(random.randint(0, 255)) for _ in range(3))
                    print(f"{i}|Public: {publick_ip}, Private: {private_ip}")
                print(f"Generated by!")
                input()
            else:
                print("You must enter the numbers!")
                time.sleep(3)
            reset(False, True, False)
    ### Information
    elif hl_prompt == "4":
        print("Atomic Private Comunity - Information")
        print("1. Nothing")
        input()
        reset(False, False, False)
    ### Account
    elif hl_prompt == "5":
        print(f"Atomic Private Comunity - Account\n1|Change Username\n2|Change Password\n3|Generate invite\n4|Delete Account")
        sl_prompt = input("> ")
        clear()
        # Účet - Change Username
        if sl_prompt == "1":
            print(f"Atomic Private Comunity - Change Username\nThe name must contain at least 3 characters")
            _password = input("Password: ")
            _username = input("New usernamename: ")
            _verify_gen = random.randint(11111111, 99999999)
            verify = input(f"Verification code ({_verify_gen}): ")
            _aprove = input("Do you want to change your username? [Y/n]: ")
            if _aprove == "Y" or _aprove == "y":
                print("Verification...")
                if verify == str(_verify_gen):
                    if _password == log_pass and pass_user_check(_username, None):
                        print("Verified by!")
                        print("The username is changing...")
                        server_contact(f"USER-CHANGE,{log_user},{_username}")
                        if server_data == "TRUE":
                            print("The username is changed!")
                            time.sleep(notify_time)
                            exit()
                        else:
                            print("The username is taken!")
                            time.sleep(notify_time)
                    else:
                        print("Password or username is incorrect!")
                        time.sleep(notify_time)
                else:
                    print("Verification code is not correct!")
                    time.sleep(notify_time)
            reset(False, False, True)
        # Účet - Change Password
        elif sl_prompt == "2":
            print(f"Atomic Private Comunity - Change Password\nThe password must contain:\n- Minimum 10 characters\n- No diacritics\n- 1 special character\n- 1 capital letter\n- 1 lower case\n- 1 number")
            _password_cur = input("Current password: ")
            _password_new = input("New password: ")
            _password_aga = input("New password again: ")
            _verify_gen = random.randint(11111111, 99999999)
            verify = input(f"Verification code ({_verify_gen}): ")
            _aprove = input("Want to change your password? [Y/n]: ")
            if _aprove == "Y" or _aprove == "y":
                print("Verification...")
                if verify == str(_verify_gen):
                    if _password_cur == log_pass and _password_new == _password_aga and pass_user_check(None, _password_new):
                        print("Verified by!")
                        print("The password is changing...")
                        server_contact(f"PASS-CHANGE,{log_user},{_password_new}")
                        print("Password changed!")
                        time.sleep(notify_time)
                        exit()
                    else:
                        print("New or current password is incorrect!")
                        time.sleep(notify_time)
                else:
                    print("The verification code is not correct!")
                    time.sleep(notify_time)
            reset(False, False, True)
        # Účet - Generate invite
        elif sl_prompt == "3":
            print(f"Atomic Private Comunity - Generate invite\nAttention, you can only generate 1 invite!")
            _password = input("Password: ")
            _verify_gen = random.randint(11111111, 99999999)
            verify = input(f"Verification code ({_verify_gen}): ")
            _aprove = input("Do you want to generate an invite? [Y/n]: ")
            if _aprove == "Y" or _aprove == "y":
                print("Verification...")
                if verify == str(_verify_gen):
                    if _password == log_pass:
                        print("Verified by!")
                        print("Generating...")
                        server_contact(f"INVITE-GEN,{log_user}")
                        if server_data == "FALSE":
                            print("You have already generated 1 invite!")
                            time.sleep(notify_time)
                        else:
                            print(f"You have already generated 1 invite!\nInvitation: {server_data}")
                            input()
                    else:
                        print("Password is not correct!")
                        time.sleep(notify_time)
                else:
                    print("Verification code is not correct!")
                    time.sleep(notify_time)
            reset(False, False, True)
        # Účet - Delete Account
        elif sl_prompt == "4":
            print(f"Atomic Private Comunity - Delete Account\nAttention, you can only generate 1 invite!")
            _password = input("Password: ")
            _verify_gen = random.randint(11111111, 99999999)
            verify = input(f"Verification code ({_verify_gen}): ")
            _aprove = input("Want to delete your account? [Y/n]: ")
            if _aprove == "Y" or _aprove == "y":
                print("Verification...")
                if verify == str(_verify_gen):
                    if _password == log_pass:
                        print("Verified by!")
                        print("Deleting...")
                        server_contact(f"ACC-DELETE,{log_user}")
                        print("The account has been deleted!")
                        time.sleep(notify_time)
                        exit()
                    else:
                        print("Password is not correct!")
                        time.sleep(notify_time)
                else:
                    print("Verification code is not correct!")
                    time.sleep(notify_time)
            reset(False, False, True)
    ### Exit
    elif hl_prompt == "6": exit()
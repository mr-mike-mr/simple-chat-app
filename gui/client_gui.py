import tkinter as tk
from tkinter import ttk
import socket
from unidecode import unidecode
import re
import time
import random
import string
from random_username.generate import generate_username
import sys
import errno
import requests
import threading


### Config
global main_server_ip, main_server_port, chat_server_ip, chat_server_port, header_lenght
main_server_ip = "localhost"
main_server_port = 12345
chat_server_ip = "localhost"
chat_server_port = 12346
header_lenght = 999999


### Premenná
global docastne_username, docastne_password
docastne_username = ""
docastne_password = ""


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
        server_data = server_connect.recv(1024).decode()
        return server_data
# Web Ping
def web_ping(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except:
        return False


############ Client Panel ############
def client_panel():
    ### Login Panel Close
    window_login.destroy()

    ### Window - Setting
    window = tk.Tk()
    window.title("Atomic Private Comunity - Client")
    window.geometry("970x700")
    
    
    ### Notebook
    notebook = ttk.Notebook(window)
    # Notebook - Tabs
    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    tab3 = ttk.Frame(notebook)
    tab4 = ttk.Frame(notebook)
    tab5 = ttk.Frame(notebook)
    
    ### Tab1 - Chat
    notebook.add(tab1, text="Chat")
    # Chat
    text_chat = tk.Label(tab1, text="Chat", bg="white", height=20, width=107)
    text_chat.place(relx=0.0, rely=0.0)
    #message_text = tk.Text(tab1, height=20, width=107, state="disabled")
    #message_text.place(relx=0.0, rely=0.0)
    # Chat Send
    def chat_receive_data():
        while True:
            data = client_socket.recv(header_lenght).decode('utf-8')
            if not data:
                break
            #message_text.insert(tk.END, data + "\n")
            
            new_message = f"\n{data}"
            current_message = text_chat.cget("text")
            updated_message = current_message + new_message
            text_chat.config(text=updated_message)
    def chat_send(): client_socket.send(input_chat_send.get().encode('utf-8'))
    button_chat_send = tk.Button(tab1, text ="Chat Send", height=2, width=15, command=chat_send).place(x=3, y=450)
    input_chat_send = tk.Entry(tab1, bd =2, width=72, font=(10))
    input_chat_send.place(x=170, y=462)
    # Chat Connect
    def chat_connect():
        global client_socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((chat_server_ip, chat_server_port))
        receive_thread = threading.Thread(target=chat_receive_data)
        receive_thread.start()
    button_chat_connect = tk.Button(tab1, text ="Chat Connect", height=2, width=15, command=chat_connect).place(x=3, y=512)
    # Notify 1
    text_notify1 = tk.Label(tab1, font=(10))
    text_notify1.place(x=3, y=600)
    
    ### Tab2 - Data
    notebook.add(tab2, text="Data")
    # Links
    text_links = tk.Label(tab2, text="Links", bg="white", height=20, width=53)
    text_links.place(relx=0.0, rely=0.0)
    # Refresh Links
    def links_refresh():
        text_notify2.config(text="Loading links...")
        server_data = server_contact("LINK-SHOW")
        time.sleep(2)
        sql_link_help = "Links:"
        if server_data != "None":
            help_links = 0
            server_data_list = list(map(lambda x: x[0], eval(server_data)))
            for i in server_data_list:
                sql_link_help += f"\n{help_links}|{i}"
                help_links += 1
        text_links.config(text=(sql_link_help))
        text_notify2.config(text="Links loaded!")
    button_refresh_links = tk.Button(tab2, text ="Refresh Links", height=2, width=50, command=links_refresh).place(x=3, y=450)
    # Link Request
    def link_request():
        if input_link_request.get() != "" and len(input_link_request.get()) >= 5 and web_ping(input_link_request.get()):
            text_notify2.config(text="I send...")
            server_data = server_contact(f"LINK-REQ,{docastne_username},{input_link_request.get()}")
            time.sleep(2)
            if server_data == "FALSE-R-EXIST":
                text_notify2.config(text="This link has already been requested to be added!")
            elif server_data == "FALSE-L-EXIST":
                text_notify2.config(text="Link already exists!")
            else:
                text_notify2.config(text="Sent, you have to wait for approval before the link can be published.")
        else:
            text_notify2.config(text="Link does not exist!")
    button_link_request = tk.Button(tab2, text ="Link Request", height=2, width=15, command=link_request).place(x=3, y=510)
    text_link_request = tk.Label(tab2, text="Link", font=(10)).place(x=170, y=522)
    input_link_request = tk.Entry(tab2, bd =2, width=23, font=(10))
    input_link_request.place(x=220, y=522)
    # Markets
    text_markets = tk.Label(tab2, text="Markets", bg="white", height=20, width=53)
    text_markets.place(relx=0.5, rely=0.0)
    # Refresh Markets
    def markets_refresh():
        text_notify2.config(text="Loading markets...")
        server_data = server_contact("MARKET-SHOW")
        time.sleep(2)
        sql_market_help = "Markets:"
        if server_data != "None":
            help_markets = 0
            server_data_list = list(map(lambda x: x[0], eval(server_data)))
            for i in server_data_list:
                sql_market_help += f"\n{help_markets}|{i}"
                help_markets += 1
        text_markets.config(text=(sql_market_help))
        text_notify2.config(text="Markets loaded!")
    button_refresh_markets = tk.Button(tab2, text ="Refresh Markets", height=2, width=51, command=markets_refresh).place(x=485, y=450)
    # Market Request
    def market_request():
        if input_market_request.get() != "" and len(input_market_request.get()) >= 5 and web_ping(input_market_request.get()):
            text_notify2.config(text="I send...")
            server_data = server_contact(f"MARKET-REQ,{docastne_username},{input_market_request.get()}")
            time.sleep(2)
            if server_data == "FALSE-R-EXIST":
                text_notify2.config(text="This link has already been requested to be added!")
            elif server_data == "FALSE-L-EXIST":
                text_notify2.config(text="Link already exists!")
            else:
                text_notify2.config(text="Sent, you have to wait for approval before the link can be published.")
        else:
            text_notify2.config(text="Link does not exist!")
    button_market_request = tk.Button(tab2, text ="Market Request", height=2, width=15, command=market_request).place(x=485, y=510)
    text_market_request= tk.Label(tab2, text="Link", font=(10)).place(x=655, y=522)
    input_market_request = tk.Entry(tab2, bd =2, width=23, font=(10))
    input_market_request.place(x=705, y=522)
    # Notify 2
    text_notify2 = tk.Label(tab2, font=(10))
    text_notify2.place(x=3, y=600)
    
    ### Tab3 - Features
    notebook.add(tab3, text="Features")
    # Generate Number
    def generate_number():
        if input_gen_number_from.get().isdigit() and input_gen_number_to.get().isdigit():
            text_notify3.config(text="Generating...")
            input_gen_number.config(text=f"{random.randint(int(input_gen_number_from.get()), int(input_gen_number_to.get()))}")
            text_notify3.config(text="Generated by!")
        else:
            text_notify3.config(text="You must enter the numbers!")
    button_gen_number = tk.Button(tab3, text ="Generate number", height=2, width=15, command=generate_number).place(x=3, y=25)
    text_gen_number_from = tk.Label(tab3, text="From", font=(10)).place(x=170, y=18)
    input_gen_number_from = tk.Entry(tab3, bd =2, width=10, font=(10))
    input_gen_number_from.place(x=224, y=18)
    text_gen_number_to = tk.Label(tab3, text="To", font=(10)).place(x=170, y=52)
    input_gen_number_to = tk.Entry(tab3, bd =2, width=10, font=(10))
    input_gen_number_to.place(x=224, y=52)
    input_gen_number = tk.Label(tab3, text="Number", bg="white", height=1, width=69)
    input_gen_number.place(x=350, y=40)
    # Generate Password
    def generate_password():
        if input_gen_pass_much.get().isdigit():
            text_notify3.config(text="Generating...")
            pass_char = string.ascii_letters + string.digits
            pass_gen = ''.join(random.choice(pass_char) for i in range(int(input_gen_pass_much.get())))
            text_gen_pass.config(text=f"{pass_gen}")
            text_notify3.config(text="Generated by!")
        else:
            text_notify3.config(text="You must enter the numbers!")
    button_gen_pass = tk.Button(tab3, text ="Generate password", height=2, width=15, command=generate_password).place(x=3, y=115)
    text_gen_pass_much = tk.Label(tab3, text="Length", font=(10)).place(x=170, y=128)
    input_gen_pass_much = tk.Entry(tab3, bd =2, width=10, font=(10))
    input_gen_pass_much.place(x=240, y=126)
    text_gen_pass = tk.Label(tab3, text="Password", bg="white", height=1, width=67)
    text_gen_pass.place(x=365, y=130)
    # Generate Username
    def generate_name():
        text_notify3.config(text="Generating...")
        username_list = generate_username(1)
        text_gen_name.config(text=f"{username_list[0]}")
        text_notify3.config(text="Generated by!")
    button_gen_name = tk.Button(tab3, text ="Generate username", height=2, width=15,command=generate_name).place(x=3, y=205)
    text_gen_name = tk.Label(tab3, text="Password", bg="white", height=1, width=89)
    text_gen_name.place(x=170, y=220)  
    # Generate Ip
    def generating_ip():
        text_notify3.config(text="Generating...")
        publick_ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
        private_ip = "10." + ".".join(str(random.randint(0, 255)) for _ in range(3))
        text_gen_ip.config(text=f"Public IP: {publick_ip} | Private IP: {private_ip}")
        text_notify3.config(text="Generated by!")
    button_gen_ip = tk.Button(tab3, text ="Generate IP", height=2, width=15, command=generating_ip).place(x=3, y=295)
    text_gen_ip = tk.Label(tab3, text="IP", bg="white", height=1, width=89)
    text_gen_ip.place(x=170, y=310)  
    # Notify 3
    text_notify3 = tk.Label(tab3, font=(10))
    text_notify3.place(x=3, y=600)
    
    ### Tab4 - Information
    notebook.add(tab4, text="Information")
    # Information
    text_users = tk.Label(tab4, text="Information:\n1. Nothing", bg="white", height=30, width=107).place(relx=0.0, rely=0.0)
    
    ### Tab5 - Account
    notebook.add(tab5, text="Account")
    # Change Username
    def change_name():
        if input_change_name_pass.get() == docastne_password and pass_user_check(input_change_name_new.get(), None):
            text_notify4.config(text="The username is changing...")
            if server_contact(f"USER-CHANGE,{docastne_username},{input_change_name_new.get()}") == "TRUE":
                text_notify4.config(text="The username is changed!")
                time.sleep(3)
                exit()
            else:
                text_notify4.config(text="The username is taken!")
        else:
            text_notify4.config(text="Password or username is incorrect!")
    button_change_name = tk.Button(tab5, text ="Change number", height=2, width=15, command=change_name).place(x=3, y=25)
    text_change_name_new = tk.Label(tab5, text="New Username", font=(10)).place(x=170, y=40)
    input_change_name_new = tk.Entry(tab5, bd =2, width=20, font=(10))
    input_change_name_new.place(x=325, y=40)
    text_change_name_pass = tk.Label(tab5, text="Current password", font=(10)).place(x=550, y=40)
    input_change_name_pass = tk.Entry(tab5, bd =2, width=21, font=(10), show="*")
    input_change_name_pass.place(x=730, y=40)
    # Change Password
    def change_pass():
        if input_change_pass_curr.get() == docastne_password and pass_user_check(None, input_change_pass_new.get()):
            text_notify4.config(text="The password is changing...")
            server_contact(f"PASS-CHANGE,{docastne_username},{input_change_pass_new.get()}")
            text_notify4.config(text="Password changed!")
            time.sleep(3)
            exit()
        else:
            text_notify4.config(text="New or current password is incorrect!")
    button_change_pass = tk.Button(tab5, text ="Change password", height=2, width=15, command=change_pass).place(x=3, y=115)
    text_change_pass_new = tk.Label(tab5, text="New password", font=(10)).place(x=170, y=130)
    input_change_pass_new = tk.Entry(tab5, bd =2, width=21, font=(10), show="*")
    input_change_pass_new.place(x=315, y=130)
    text_change_pass_curr = tk.Label(tab5, text="Current password", font=(10)).place(x=550, y=130)
    input_change_pass_curr = tk.Entry(tab5, bd =2, width=21, font=(10), show="*")
    input_change_pass_curr.place(x=730, y=130)
    # Generate Invite
    def acc_generate_invite():
        text_notify4.config(text="Generating...")
        server_data = server_contact(f"INVITE-GEN,{docastne_username}")
        print(server_data)
        time.sleep(1)
        if server_data == "FALSE":
            text_notify4.config(text="You have already generated 1 invite!")
        else:
            text_notify4.config(text="Invite was generated!")
            text_gen_invite.config(text=f"{server_data}")
    button_gen_invite = tk.Button(tab5, text ="Generate invite", height=2, width=15, command=acc_generate_invite).place(x=3, y=205)
    text_gen_invite = tk.Label(tab5, text="Invite", bg="white", height=1, width=88)
    text_gen_invite.place(x=170, y=222)
    # Delete Account
    def acc_delete():
        if input_del_acc_pass.get() == docastne_password:
            text_notify4.config(text="Deleting...")
            server_contact(f"ACC-DELETE,{docastne_username}")
            text_notify4.config(text="The account has been deleted!")
            time.sleep(3)
            exit()
        else:
            text_notify4.config(text="Password is not correct!")
    button_del_acc = tk.Button(tab5, text ="Delete account", height=2, width=15, command=acc_delete).place(x=3, y=295)
    text_del_acc_pass = tk.Label(tab5, text="Current password", font=(10)).place(x=170, y=310)
    input_del_acc_pass = tk.Entry(tab5, bd =2, width=56, font=(10), show="*")
    input_del_acc_pass.place(x=350, y=310)
    # Notify 4
    text_notify4 = tk.Label(tab5, font=(10))
    text_notify4.place(x=3, y=600)
    
    # Notebook - Tabs Style
    style = ttk.Style()
    style.configure("TNotebook.Tab", padding=(10, 12))
    # Notebook - Tabs Place
    notebook.pack(fill="both", expand=True)
    
    
    ### Windows - Loop
    window.mainloop()




############ Login Panel ############
### Window - Setting
window_login = tk.Tk()
window_login.title("Atomic Private Comunity - Login")
window_login.geometry("970x700")


### Notebook
notebook = ttk.Notebook(window_login)
# Notebook - Tabs
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)

### Tab1 - Sign in
notebook.add(tab1, text="Sign in")
# Username
text_signin_name = tk.Label(tab1, text="Username", font=(10)).place(x=3, y=10)
input_signin_name = tk.Entry(tab1, bd =2, width=25, font=(10))
input_signin_name.place(x=115, y=10)
# Password
text_signin_pass = tk.Label(tab1, text="Password", font=(10)).place(x=3, y=60)
input_signin_pass = tk.Entry(tab1, bd =2, width=25, font=(10), show="*")
input_signin_pass.place(x=115, y=60)
# Sign In
def sign_in():
    if pass_user_check(input_signin_name.get(), input_signin_pass.get()):
        if "TRUE" in server_contact(f"LOGIN,{input_signin_name.get()},{input_signin_pass.get()}"):
            global docastne_password, docastne_username
            docastne_username = input_signin_name.get()
            docastne_password = input_signin_pass.get()
            text_notify1.config(text="You were logged in!")
            time.sleep(3)
            client_panel()
        else:
            text_notify1.config(text="Password or username is incorrect!")
    else:
        text_notify1.config(text="Password or username is incorrect!")
button_signin = tk.Button(tab1, text ="Sign in", height=2, width=15, command=sign_in).place(x=115, y=110)
# Notify1
text_notify1 = tk.Label(tab1, font=(10))
text_notify1.place(x=3, y=170)

### Tab2 - Sign up
notebook.add(tab2, text="Sign up")
# Username
text_signup_name = tk.Label(tab2, text="Username", font=(10)).place(x=3, y=10)
input_signup_name = tk.Entry(tab2, bd =2, width=25, font=(10))
input_signup_name.place(x=115, y=10)
# Password1
text_signup_pass1 = tk.Label(tab2, text="Password", font=(10)).place(x=3, y=60)
input_signup_pass1 = tk.Entry(tab2, bd =2, width=25, font=(10), show="*")
input_signup_pass1.place(x=115, y=60)
# Password2
text_signup_pass2 = tk.Label(tab2, text="Password", font=(10)).place(x=3, y=110)
input_signup_pass2 = tk.Entry(tab2, bd =2, width=25, font=(10), show="*")
input_signup_pass2.place(x=115, y=110)
# Invite
text_signup_invite = tk.Label(tab2, text="Invite", font=(10)).place(x=3, y=160)
input_signup_invite = tk.Entry(tab2, bd =2, width=25, font=(10))
input_signup_invite.place(x=115, y=160)
# Rules
text_signup_rules = tk.Label(tab2, text="The name must contain at least 3 characters\nThe password must contain:\n    - Minimum 10 characters\n    - No diacritics\n    - 1 special character\n    - 1 capital letter\n    - 1 lowercase letter\n    - 1 number", font=(10))
text_signup_rules.place(x=500, y=4)
# Sign up
def sign_up():
    if len(input_signup_invite.get()) == 20 and input_signup_pass1.get() == input_signup_pass2.get() and pass_user_check(input_signup_name.get(), input_signup_pass1.get()):
        server_data = server_contact(f"REGISTER,{input_signup_name.get()},{input_signup_pass1.get()},{input_signup_invite.get()}")
        if "TRUE" in server_data:
            text_notify2.config(text="You have been registered!")
        elif "FALSE-USER" in server_data:
            text_notify2.config(text="The username is already registered!")
        elif "FALSE-INVITE" in server_data:
            text_notify2.config(text="Invitation does not exist!")
    else:
        text_notify2.config(text="Password or username is incorrect!")
button_signup = tk.Button(tab2, text ="Sign up", height=2, width=15, command=sign_up).place(x=115, y=210)
# Notify2
text_notify2 = tk.Label(tab2, font=(10))
text_notify2.place(x=3, y=270)

# Notebook - Tabs Style
style = ttk.Style()
style.configure("TNotebook.Tab", padding=(10, 12))
# Notebook - Tabs Place
notebook.pack(fill="both", expand=True)


### Windows - Start
window_login.mainloop()
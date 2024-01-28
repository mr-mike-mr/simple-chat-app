### Libery
import tkinter as tk
from tkinter import ttk
import socket
from unidecode import unidecode
import re


### Config
main_server_ip = "localhost"
main_server_port = 12345


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

### Window - Setting
window = tk.Tk()
window.title("Atomic Private Comunity - Login")
window.geometry("970x700")


### Notebook
notebook = ttk.Notebook(window)
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
            text_notify1.config(text="You were logged in!")
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
window.mainloop()
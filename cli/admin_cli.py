### Libery
import os
import sqlite3
import time
import random
import requests
import platform


### Config
sql_path = "sqlite_database_cli.db"


### Functions
# Reset
def reset(sql):
    global _confirm, prompt, hl_prompt, __prompt, sql_row, sql_row_split, sl_prompt
    _confirm = _prompt = hl_prompt = __prompt = sql_row = sql_row_split = sl_prompt = None
    if sql == True:
        sql_cursor.close()
        sql_conn.close()
# Web Ping
def web_ping(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except:
        return False
# Sql Split
def sql_split(sql_row):
    global sql_row_split
    sql_row_split = []
    for data in sql_row: sql_row_split.append(str(data[0]).replace(",", "").replace("(", "").replace(")", "").replace("'", ""))
# Invites Show
def invite_show():
    sql_cursor.execute("SELECT * FROM invites")
    sql_row = sql_cursor.fetchall()
    print("Invitations:")
    for i in sql_row:
        print(i)
    sql_split(sql_row)
# Clear
def clear():
    if platform.system() == "Linux": os.system("clear")
    elif platform.system() == "Windows": os.system("cls")
    else: exit()


### Panel
while True:
    reset(False)
    clear()
    print("Atomic Private Comunity - Admin\n1|Links\n2|Markets\n3|Accounts\n4|Invitations\n5|Exit")
    hl_prompt = input("> ")
    clear()

    ### Links
    if hl_prompt == "1":
        print("Atomic Private Comunity - Links\n1|List Added\n2|List Requests\n3|Create")
        sl_prompt = input("> ")
        # Links - List Added
        if sl_prompt == "1":
            print("Atomic Private Comunity - List Added")
            sql_conn = sqlite3.connect(sql_path)
            sql_cursor = sql_conn.cursor()
            sql_cursor.execute("SELECT * FROM links")
            sql_row = sql_cursor.fetchall()
            print("List Added:")
            for i in sql_row:
                print(i)
            sql_split(sql_row)
            _prompt = input("Id you want to delete: ")
            if _prompt != "":
                _confirm = input(f"Do you really want to delete the link? [Y/n]:")
                if _confirm == "Y" or _confirm == "y":
                    if _prompt in sql_row_split:
                        print("Deleting...")
                        sql_cursor.execute("DELETE FROM links WHERE id=?", (_prompt,))
                        sql_conn.commit()
                        print("Deleted!")
                    else:
                        print("Id does not exist!")
                    time.sleep(2)
            reset(True)
        # Links - List Requests
        elif sl_prompt == "2":
            print("Atomic Private Comunity - List Requests")
            sql_conn = sqlite3.connect(sql_path)
            sql_cursor = sql_conn.cursor()
            sql_cursor.execute("SELECT * FROM link_requests")
            sql_row = sql_cursor.fetchall()
            print("List Requests:")
            for i in sql_row:
                print(i)
            sql_split(sql_row)
            _prompt = input("Id of the link: ")
            if _prompt != "":
                print("1|Delete\n2|Add")
                __prompt = input("> ")
                if _prompt in sql_row_split:
                    # Links - List Requests - Delete
                    if __prompt == "1":
                        _confirm = input("Do you really want to delete the link? [Y/n]:")
                        if _confirm == "Y" or _confirm == "y":
                            print("Deleting...")
                            sql_cursor.execute("DELETE FROM link_requests WHERE id=?", (_prompt,))
                            sql_conn.commit()
                            print("Deleted!")
                            time.sleep(2)
                    # Links - List Requests - Add
                    elif __prompt == "2":
                        _confirm = input("Do you really want to add a link? [Y/n]:")
                        if _confirm == "Y" or _confirm == "y":
                            print("Adding...")
                            sql_cursor.execute("SELECT link FROM link_requests WHERE id=?", (_prompt,))
                            sql_row = sql_cursor.fetchone()
                            sql_cursor.execute("INSERT INTO links (link) VALUES (?)", (sql_row[0],))
                            sql_cursor.execute("DELETE FROM link_requests WHERE id=?", (_prompt,))
                            sql_conn.commit()
                            print("Added!")
                            time.sleep(2)
                else:
                    print("Id does not exist!")
                    time.sleep(2)
            reset(True)
        # Links - Create
        elif sl_prompt == "3":
            print("Atomic Private Comunity - Create")
            sql_conn = sqlite3.connect(sql_path)
            sql_cursor = sql_conn.cursor()
            sql_cursor.execute("SELECT link FROM links")
            sql_row = sql_cursor.fetchall()
            sql_split(sql_row)
            _prompt = input("Link (https://www.link.com): ")
            if _prompt != "":
                _confirm = input("Do you really want to add a link? [Y/n]:")
                if _confirm == "Y" or _confirm == "y":
                    if len(_prompt) >= 5 and web_ping(_prompt):
                        if not _prompt in sql_row_split:
                            print("Creating...")
                            sql_cursor.execute("INSERT INTO links (link) VALUES (?)", (_prompt,))
                            sql_conn.commit()
                            print("Retrieved from!")
                        else:
                            print("Link already exists!")
                    else:
                        print("Link does not exist!")
                    time.sleep(2)
            reset(True)

    ### Markets
    elif hl_prompt == "2":
        print("Atomic Private Comunity - Markets\n1|List Added\n2|List Requests\n3|Create")
        sl_prompt = input("> ")
        clear()
        # Markets - List Added
        if sl_prompt == "1":
            print("Atomic Private Comunity - List Added")
            sql_conn = sqlite3.connect(sql_path)
            sql_cursor = sql_conn.cursor()
            sql_cursor.execute("SELECT * FROM markets")
            sql_row = sql_cursor.fetchall()
            print("Markets:")
            for i in sql_row:
                print(i)
            sql_split(sql_row)
            _prompt = input("Id of the market you want to delete: ")
            if _prompt != "":
                _confirm = input("Do you really want to delete the market? [Y/n]:")
                if _confirm == "Y" or _confirm == "y":
                    if not int(_prompt) in sql_row_split:
                        print("Deleting...")
                        sql_cursor.execute("DELETE FROM markets WHERE id=?", (_prompt,))
                        sql_conn.commit()
                        print("Deleted!")
                    else:
                        print("Id does not exist!")
                    time.sleep(2)
            reset(True)
        # Markets - List Requests
        if sl_prompt == "2":
            print("Atomic Private Comunity - List Requests")
            sql_conn = sqlite3.connect(sql_path)
            sql_cursor = sql_conn.cursor()
            sql_cursor.execute("SELECT * FROM market_requests")
            sql_row = sql_cursor.fetchall()
            print("List Requests:")
            for i in sql_row:
                print(i)
            sql_split(sql_row)
            _prompt = input("Id of the market: ")
            if _prompt != "":
                print("1|Delete\n2|Add")
                __prompt = input("> ")
                if _prompt in sql_row_split:
                    # Markets - List Requests - Delete
                    if __prompt == "1":
                        _confirm = input("Do you really want to delete the market? [Y/n]:")
                        if _confirm == "Y" or _confirm == "y":
                            print("Deleting...")
                            sql_cursor.execute("DELETE FROM market_requests WHERE id=?", (_prompt,))
                            sql_conn.commit()
                            print("Deleted!")
                            time.sleep(2)
                    # Markets - List Requests - Add
                    elif __prompt == "2":
                        _confirm = input("Do you really want to add a market? [Y/n]:")
                        if _confirm == "Y" or _confirm == "y":
                            print("Adding...")
                            sql_cursor.execute("SELECT link FROM market_requests WHERE id=?", (_prompt,))
                            sql_row = sql_cursor.fetchone()
                            sql_cursor.execute("INSERT INTO markets (link) VALUES (?)", (sql_row[0],))
                            sql_cursor.execute("DELETE FROM market_requests WHERE id=?", (_prompt,))
                            sql_conn.commit()
                            print("Added!")
                            time.sleep(2)
                else:
                    print("Id does not exist!")
                    time.sleep(2)
            reset(True)
        # Markets - Create
        if sl_prompt == "3":
            print("Atomic Private Comunity - Create")
            sql_conn = sqlite3.connect(sql_path)
            sql_cursor = sql_conn.cursor()
            sql_cursor.execute("SELECT link FROM markets")
            sql_row = sql_cursor.fetchall()
            sql_split(sql_row)
            _prompt = input("Link to the market: ")
            if _prompt != "":
                _confirm = input("Do you really want to add a market? [Y/n]:")
                if _confirm == "Y" or _confirm == "y":
                    if len(_prompt) >= 5 and web_ping(_prompt):
                        if not _prompt in sql_row_split:
                            print("Creating...")
                            sql_cursor.execute("INSERT INTO markets (link) VALUES (?)", (_prompt,))
                            sql_conn.commit()
                            print("Retrieved from!")
                        else:
                            print("Market already exists!")
                    else:
                        print("The market does not exist!")
                    time.sleep(2)
            reset(True)

    ### Accounts
    elif hl_prompt == "3":
        print("Atomic Private Comunity - Accounts")
        sql_conn = sqlite3.connect(sql_path)
        sql_cursor = sql_conn.cursor()
        sql_cursor.execute("SELECT id, username, invite FROM users")
        sql_row = sql_cursor.fetchall()
        print("Accounts:")
        for i in sql_row:
            print(i)
        sql_split(sql_row)
        _prompt = input("Account Id: ")
        if _prompt != "":
            if _prompt in sql_row_split:
                print("1|Delete\n2|Reset Invitation")
                __prompt = input(">")
                # Accounts - Delete
                if __prompt == "1":
                    _confirm = input("Do you really want to delete your account? [Y/n]:")
                    if _confirm == "Y" or _confirm == "y":
                        print("Deleting...")
                        sql_cursor.execute("DELETE FROM users WHERE id=?", (_prompt,))
                        sql_conn.commit()
                        print("Deleted!")
                        time.sleep(2)
                # Accounts - Reset Invitation
                elif __prompt == "2":
                    sql_cursor.execute("SELECT invite FROM users WHERE id=?", (_prompt))
                    sql_row = sql_cursor.fetchall()
                    sql_split(sql_row)
                    if "FALSE" in sql_row_split:
                        _confirm = input("Do you really want to reset the account invite? [Y/n]:")
                        if _confirm == "Y" or _confirm == "y":
                            print("Resetting...")
                            sql_cursor.execute("UPDATE users SET invite=? WHERE id=?", ("TRUE", _prompt))
                            sql_conn.commit()
                            print("Reset!")
                            time.sleep(2)
                    else:
                        print("The invit account still has!")
                        time.sleep(2)
            else:
                print("Id doesn't exist!")
                time.sleep(2)
        reset(True)

    ### Invitations
    elif hl_prompt == "4":
        print("Atomic Private Comunity - Invites\n1|List Added\n2|Delete\n3|Generate")
        sl_prompt = input("> ")
        clear()
        # Invitations - List Added
        if sl_prompt == "1":
            print("Atomic Private Comunity - List Added")
            sql_conn = sqlite3.connect(sql_path)
            sql_cursor = sql_conn.cursor()
            invite_show()
            input()
            reset(True)
        # Invitations - Delete
        if sl_prompt == "2":
            print("Atomic Private Comunity - Delete")
            sql_conn = sqlite3.connect(sql_path)
            sql_cursor = sql_conn.cursor()
            invite_show()
            _prompt = input("Invitation id you want to delete: ")
            _confirm = input("Do you really want to delete the invite? [Y/n]:")
            if _confirm == "Y" or _confirm == "y":
                if _prompt in sql_row_split:
                    print("Deleting...")
                    sql_cursor.execute("DELETE FROM invites WHERE id=?", (_prompt,))
                    sql_conn.commit()
                    print("Deleted!")
                else:
                    print("Id does not exist!")
                time.sleep(2)
            reset(True)
        # Invitations - Generate
        if sl_prompt == "3":
            print("Atomic Private Comunity - Generate")
            sql_conn = sqlite3.connect(sql_path)
            sql_cursor = sql_conn.cursor()
            _confirm = input("Do you really want to generate invitations? [Y/n]:")
            if _confirm == "Y" or _confirm == "y":
                print("Generating...")
                _invite = str(random.randint(1, 9)) + random.choice('aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ') + str(random.randint(1, 9)) + random.choice('aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ') + str(random.randint(1, 9)) + random.choice('aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ') + str(random.randint(1, 9)) + random.choice('aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ') + str(random.randint(1, 9)) + random.choice('aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ') + str(random.randint(1, 9)) + random.choice('aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ') + str(random.randint(1, 9)) + random.choice('aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ') + str(random.randint(1, 9)) + random.choice('aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ') + str(random.randint(1, 9)) + random.choice('aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ') + str(random.randint(1, 9)) + random.choice('aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ')
                sql_cursor.execute("INSERT INTO invites (invite) VALUES (?)", (_invite,))
                sql_conn.commit()
                print(f"Retrieved from!\nInvitation: {_invite}")
                input()
            reset(True)

    ### Exit
    elif hl_prompt == "5": exit()

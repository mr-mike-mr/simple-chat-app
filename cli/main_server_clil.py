### Libery
import sqlite3
import socket
import threading
import random
import time


### Config
server_ip = "localhost"
server_port = 12345
app_version = "1.0.0"
app_download = "https://github.com/mr-mike-eu/simple-chat-app"
sql_path = "sqlite_database_cli.db"
header_lenght = 9999999999


### Functions
# Client Handle
def handle_client(connection, address):
    print(f"New client connected!")
    while True:
        data = connection.recv(header_lenght).decode()
        if not data:
            print(f"Client disconnected")
            break
        data_split = data.split(",")
        sql_conn = sqlite3.connect(sql_path)
        sql_cursor = sql_conn.cursor()
        ### VERSION AND STATUS CHECK - "CHECK,{app_version}"
        if data_split[0] == "VERSION":
            if data_split[1] == app_version:
                connection.sendall(("TRUE").encode())
            else:
                connection.sendall((app_download).encode())
        ### LOGIN CHECKER - "LOGIN,{log_user},{log_pass}"
        elif data_split[0] == "LOGIN":
            sql_cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (data_split[1], data_split[2]))
            sql_row = sql_cursor.fetchone()
            if sql_row is not None:
                connection.sendall(("TRUE").encode())
            else:
                connection.sendall(("FALSE").encode())
        # REGISTER CHECKER - "REGISTER,{reg_user},{reg_pass},{reg_invite}"
        elif data_split[0] == "REGISTER":
            sql_cursor.execute("SELECT * FROM users WHERE username=?", (data_split[1],))
            sql_row = sql_cursor.fetchone()
            if sql_row:
                connection.sendall(("FALSE-USER").encode())
            else:
                sql_cursor.execute("SELECT * FROM invites WHERE invite=?", (data_split[3],))
                sql_row = sql_cursor.fetchone()
                if sql_row:
                    sql_cursor.execute("DELETE FROM invites WHERE invite=?", (data_split[3],))
                    sql_conn.commit()
                    sql_cursor.execute("INSERT INTO users (username, password, invite) VALUES (?, ?, ?)", (data_split[1], data_split[2], "FALSE",))
                    sql_conn.commit()
                    connection.sendall(("TRUE").encode())
                else:
                    connection.sendall(("FALSE-INVITE").encode())
        ### LINKS SEND - "LINK-SHOW"
        elif data_split[0] == "LINK-SHOW":
            sql_cursor.execute("SELECT link FROM links")
            sql_row = sql_cursor.fetchall()
            if len(sql_row) <= 0:
                connection.sendall(("None").encode())
            else:
                connection.sendall((str(sql_row)).encode())
        # LINK REQUEST - "LINK-REQ,{log_user},{_link}"
        elif data_split[0] == "LINK-REQ":
            sql_cursor.execute("SELECT link FROM links")
            sql_row = sql_cursor.fetchone()
            if sql_row != data_split[2]:
                sql_cursor.execute("SELECT link FROM link_requests")
                sql_row = sql_cursor.fetchone()
                if sql_row != data_split[2]:
                    sql_cursor.execute("INSERT INTO link_requests (link, user) VALUES (?, ?)", (data_split[2], data_split[1]))
                    sql_conn.commit()
                    connection.sendall(("TRUE").encode())
                else:
                    connection.sendall(("FALSE-R-EXIST").encode())
            connection.sendall(("FALSE-L-EXIST").encode())
        # MARKET SEND - "MARKET-SHOW"
        elif data_split[0] == "MARKET-SHOW":
            sql_cursor.execute("SELECT link FROM markets")
            sql_row = sql_cursor.fetchall()
            if len(sql_row) <= 0:
                connection.sendall(("None").encode())
            else:
                connection.sendall((str(sql_row)).encode())
        # MARKET REQUEST - "MARKET-REQ,{log_user},{_msg}"
        elif data_split[0] == "MARKET-REQ":
            sql_cursor.execute("SELECT link FROM markets")
            sql_row = sql_cursor.fetchone()
            if sql_row != data_split[2]:
                sql_cursor.execute("SELECT link FROM market_requests")
                sql_row = sql_cursor.fetchone()
                if sql_row != data_split[2]:
                    sql_cursor.execute("INSERT INTO market_requests (link, user) VALUES (?, ?)", (data_split[2], data_split[1]))
                    sql_conn.commit()
                    connection.sendall(("TRUE").encode())
                else:
                    connection.sendall(("FALSE-R-EXIST").encode())
            connection.sendall(("FALSE-L-EXIST").encode())
        # USERNAME CHANGE - "USER-CHANGE,{log_user},{_username}"
        elif data_split[0] == "USER-CHANGE":
            sql_cursor.execute("SELECT username FROM users WHERE username=?", (data_split[2],))
            sql_row = sql_cursor.fetchone()
            if sql_row == None:
                connection.sendall(("TRUE").encode())
                sql_cursor.execute("UPDATE users SET username=? WHERE username=?", (data_split[2], data_split[1]))
                sql_conn.commit()
            else:
                connection.sendall(("FALSE").encode())
        # PASSWORD CHANGE - "PASS-CHANGE,{log_user},{_password_new}"
        elif data_split[0] == "PASS-CHANGE":
            sql_cursor.execute("UPDATE users SET password=? WHERE username=?", (data_split[2], data_split[1]))
            sql_conn.commit()
            connection.sendall(("K").encode())
        # INVITE GEN - "INVITE-GEN,{log_user}"
        elif data_split[0] == "INVITE-GEN":
            sql_cursor.execute("SELECT invite FROM users WHERE username=?", (data_split[1],))
            sql_row = sql_cursor.fetchone()
            if "FALSE" == sql_row[0]:
                connection.sendall(("FALSE").encode())
            else:
                sql_cursor.execute("UPDATE users SET invite='FALSE' WHERE username=?", (data_split[1]))
                sql_conn.commit()
                _invite = str(random.randint(1, 9)) + random.choice('aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ') + str(random.randint(1, 9)) + random.choice('aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ') + str(random.randint(1, 9)) + random.choice('aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ') + str(random.randint(1, 9)) + random.choice('aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ') + str(random.randint(1, 9)) + random.choice('aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ') + str(random.randint(1, 9)) + random.choice('aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ') + str(random.randint(1, 9)) + random.choice('aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ') + str(random.randint(1, 9)) + random.choice('aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ') + str(random.randint(1, 9)) + random.choice('aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ') + str(random.randint(1, 9)) + random.choice('aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ')
                sql_cursor.execute("INSERT INTO invites (invite) VALUES (?)", (_invite,))
                sql_conn.commit()
                connection.sendall((_invite).encode())
        # ACCOUNT DELETE - "ACC-DELETE,{log_user}"
        elif data_split[0] == "ACC-DELETE":
            sql_cursor.execute("DELETE FROM users WHERE username=?", (data_split[1],))
            sql_conn.commit()
            connection.sendall(("K").encode())
    sql_cursor.close()
    sql_conn.close()
    connection.close()


### Server Setting
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (server_ip, server_port)
server_socket.bind(server_address)

### Waiting For Client
while True:
    print("Atomic Private Comunity - Main Server\nWaiting for a client...")
    server_socket.listen(5)
    connection, address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(connection, address))
    client_thread.start()

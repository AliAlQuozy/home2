import socket
import threading

# Predefined bank data (account number :(PIN, balance))
data = {
    '2993': ('1111', 1000),
    '2693': ('2222', 2000),
}

def handle_client(client_socket,addr):
    try:
        AUTH = False

        while True:
            request = client_socket.recv(1024).decode('utf-8').strip()
            if not request:
                break

            if not AUTH:
                account_number, pin = request.split(',')
                if account_number in data and data[account_number][0] == pin:
                    AUTH = True
                    client_socket.send(b'TRUE\n')
                else:
                    client_socket.send(b'False\n')
                    break
            if request:
                command, *args = request.split(',')
                print(command)

            if command == 'BALANCE':
                balance = data[account_number][1]
                client_socket.send(f'Balance: {balance}\n'.encode('utf-8'))

            elif command == 'DEPOSIT':
                amount = float(args[0])
                data[account_number] = (data[account_number][0], data[account_number][1] + amount)
                client_socket.send(b'Deposit Successful\n')

            elif command == 'WITHDRAW':
                amount = float(args[0])
                if data[account_number][1] >= amount:
                    data[account_number] = (
                        data[account_number][0], data[account_number][1] - amount)
                    client_socket.send(b'Withdrawal Successful\n')
                else:
                    client_socket.send(b'Insufficient Funds\n')

            elif command == 'LOGOUT':
                balance = data[account_number][1]
                client_socket.send(f'Final Balance: {balance}\n'.encode('utf-8'))
                break
    finally:
        client_socket.close()
        print(f' {addr} Closed!')



ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ssock.bind(('0.0.0.0', 1234))
ssock.listen(5)
print('Server listening on port : 1234')

while True:
    csock, addr = ssock.accept()
    print(f'New Client connection At {addr}')
    client_handler = threading.Thread(target=handle_client, args=(csock,addr))
    client_handler.start()


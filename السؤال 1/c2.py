import socket

csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
csock.connect(('127.0.0.1', 1234))

account_number = input('Enter Your account number: ')
pin = input('Enter Your PIN: ')
csock.send(f'{account_number},{pin}\n'.encode('utf-8'))

msg = csock.recv(1024).decode('utf-8').strip()
if msg == 'TRUE':
    print('Login successful!')
else:
    print('Authentication failed!')
    csock.close()


while True:
    print("\nOptions:\n1. Check\n2. Deposit\n3. Withdraw \n4. Logout")
    choice = input("Enter operation: ")

    if choice == '1':
        csock.send(b'BALANCE\n')
        msg = csock.recv(1024).decode('utf-8').strip()
        print(msg)

    elif choice == '2':
        amount = input('Enter amount to deposit: ')
        csock.send(f'DEPOSIT,{amount}\n'.encode('utf-8'))
        msg = csock.recv(1024).decode('utf-8').strip()
        print(msg)

    elif choice == '3':
        amount = input('Enter amount to withdraw: ')
        csock.send(f'WITHDRAW,{amount}\n'.encode('utf-8'))
        msg = csock.recv(1024).decode('utf-8').strip()
        print(msg)

    elif choice == '4':
        csock.send(b'LOGOUT\n')
        msg = csock.recv(1024).decode('utf-8').strip()
        print(msg)
        break

    else:
        print('Invalid choice, please try again.')

csock.close()


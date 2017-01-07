import boto3
import time
from cryptography.fernet import Fernet

# setup encryption
pin = input('enter 4 digit pin for encryption key: ')
key = pin + "Hvc6L5DAqES1234DvoM8bMiIduMF93TBcpYf-vc="
print("key is", key)
f = Fernet(key)

# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue. This returns an SQS.Queue instance
txqueue = sqs.get_queue_by_name(QueueName='fromjerry')
rxqueue = sqs.get_queue_by_name(QueueName='tojerry')

# You can now access identifiers and attributes
def print_rxtx():
    print("using " + txqueue.url + " for transmit")
    print("using " + rxqueue.url + " for receive")

print_rxtx()

# Enter main loop
while True:
    chatmsg = input('ready to xmit>')
    if chatmsg:
        if chatmsg == '/check':
            for message in rxqueue.receive_messages(WaitTimeSeconds=5):
                print('rx: ' + message.body)

                token = message.body
                token = token.encode('utf-8')
                plaintext = f.decrypt(token)
                print('decrypted > ', plaintext)
                message.delete()
        elif chatmsg == '/exit' or chatmsg == '/quit':
            exit()
        elif chatmsg == '/swap':
            print("swaping tx/rx")
            currenttx = txqueue
            currentrx = rxqueue
            txqueue = currentrx
            rxqueue = currenttx
            print_rxtx()
        else:
            print("tx>", chatmsg)
            token = chatmsg.encode('utf-8')
            cipherText = f.encrypt(token)
            cipherText = cipherText.decode('utf-8')
            # cipherText = str(cipherText)
            print("tx encrypted>", cipherText)
            response = txqueue.send_message(MessageBody=cipherText)


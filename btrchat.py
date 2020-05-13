#!/usr/bin/env python3
import boto3
import time
import threading
from cryptography.fernet import Fernet
import sys

try:
    import config as cfg
except:
    print("could not find config file.")
    print("copy config_sample.py to config.py and adjust")
    sys.exit(1)

# setup encryption
pin = "invalid"
while len(pin) != 4:
    pin = input('enter 4 digit pin for encryption key: ')
    if len(pin) < 4:
        print("too short, retry")
    elif len(pin) > 4:
        print("too long, 4 chars please or digits")
    else:
        print("pin good, proceeding")

# note: you should change this as the encryption
# relies on this secret and adding a 4 digits to the end, which we'll 
# call the pin
key = pin + "Hvc6L5DAqES1234DvoM8bMiIduMF93TBcpYf-vc="
print("key is", key)
f = Fernet(key)

# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue. This returns an SQS.Queue instance
# note change this to whatever queue you provisioned for this job.
# make sure it's a fifo queue and the AWS access key you and your friend use
# have access to it
#txqueue = sqs.get_queue_by_name(QueueName='jerrytoadam.fifo')
txqueue = sqs.get_queue_by_name(QueueName=cfg.txqueue)
#rxqueue = sqs.get_queue_by_name(QueueName='adamtojerry.fifo')
rxqueue = sqs.get_queue_by_name(QueueName=cfg.rxqueue)

# You can now access identifiers and attributes
def print_rxtx():
    print("using " + txqueue.url + " for transmit")
    print("using " + rxqueue.url + " for receive")

stop_threads = False
def check_messages():
    while True:
        if stop_threads:
            print("killing check thread")
            break
        if cfg.debug > 0:
            print("Checking for messages")
        for message in rxqueue.receive_messages(WaitTimeSeconds=20):
            if cfg.debug > 0:
                print('rx: ' + message.body)
            token = message.body
            token = token.encode('utf-8')
            plaintext = f.decrypt(token)
            print('\ndecrypted > ', plaintext)
            message.delete()
        if cfg.debug > 0:
            print("check loop complete")

print_rxtx()
print("Starting thread to check messages")
t = threading.Thread(target=check_messages)
t.start()


# Enter main loop
while True:
    chatmsg = input('ready to xmit>')
    if chatmsg:
        if chatmsg == '/check':
            for message in rxqueue.receive_messages(WaitTimeSeconds=5):
                if cfg.debug > 0:
                    print('rx: ' + message.body)

                token = message.body
                token = token.encode('utf-8')
                plaintext = f.decrypt(token)
                print('\decrypted > ', plaintext)
                message.delete()
        elif chatmsg == '/exit' or chatmsg == '/quit':
            print("waiting for thread shutdown")
            stop_threads = True
            t.join()
            exit()
        elif chatmsg == '/swap':
            print("swaping tx/rx")
            currenttx = txqueue
            currentrx = rxqueue
            txqueue = currentrx
            rxqueue = currenttx
            print_rxtx()
        elif chatmsg == '/debug':
            print("enabling debug, use /nodebug to disable")
            cfg.debug = 1
        elif chatmsg == '/nodebug':
            print("disabling debug")
            cfg.debug = 0
        else:
            print("tx>", chatmsg)
            token = chatmsg.encode('utf-8')
            cipherText = f.encrypt(token)
            cipherText = cipherText.decode('utf-8')
            # cipherText = str(cipherText)
            if cfg.debug > 0:
                print("tx encrypted>", cipherText)
            response = txqueue.send_message(MessageBody=cipherText,MessageGroupId="btrchat")



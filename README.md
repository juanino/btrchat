# btrchat
Below the Radar (btr) is meant to provide a secure transport for simple messages.
It currently requires a FIFO queue in AWS and Amazon creds to do this.
FIFO queues are not available in all regions.  You can still use whatever queue type you want
but the code doesn't check the order (you'll get the messages backwards or in random order).

This really isn't usable by more than 2 people who know each other and have some other means of
sharing the secret pin.  It's meant to show:
* how SQS queues work
* one way to encrypt some data in python with a shared secret basically and symmetric encryption

# why
in cases where you can't trust SSL communication or you have a known MITM in progress
this will provide secure transport outside of SSL by using python's cryptography library and the 
the fernet high level access.

I also needed a project to experiment with the amazon SQS service and learn some more python.

# install
* git clone this code
* install python 3 from https://www.continuum.io/downloads
* conda or pip install cryptography, boto3, awscli (or aws windows aws cli install)
* setup iam policy and keys for sqs permission
* configure aws with 'aws configure' and use keys with SQS permission
* setup an aws queue for tx and rx (transmit and receive)
* get your buddy to setup a copy of the code and python3
* modify the txqueue and rxqueue variables. 
* flip them around for your buddy or use /swap after statup
* pick a 4 digit pin on startup shared via another secure means
* optionally change the key variable to some other key or use key = Fernet.generate_key() 

# run
* run the code
* enter your 4 digit pin, share with buddy who does the same
* type a message
* you buddy will run /check
* /quit or /exit will leave the program
* for testing purposes you can use /swap to act like the other side

# references
* https://cryptography.io/en/latest/fernet/
* http://boto3.readthedocs.io/en/latest/guide/sqs.html

# bugs
* /check only pulls one message off the queue, you need to run it multiple times to get more messages (feel free to fix it)
* all kinds of bad coding practices, failure to check the pin is the right length
* control-d causes it to crash
* doesn't work with python2

# aws permissions
You will need the following access:
    "sqs:DeleteMessage",
    "sqs:GetQueueUrl",
    "sqs:ReceiveMessage",
    "sqs:SendMessage"


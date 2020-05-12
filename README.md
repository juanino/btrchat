# btrchat
Below the Radar (btr) chat is meant to provide a secure transport for simple messages.
It currently requires a FIFO queue in AWS and Amazon creds to do this.
FIFO queues are not available in all regions (see: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues.html).  You can still use whatever queue type you want
but the code doesn't check the order (you'll get the messages backwards or in random order).

This really isn't usable by more than 2 people who know each other and have some other means of
sharing the secret pin.  It's meant to show:
* How SQS queues work
* One way to encrypt some data in python with a shared secret and symmetric encryption

# Why
In cases where you can't trust SSL communication or you have a known MITM in progress
this will provide secure transport outside of SSL by using python's cryptography library and the 
the fernet high level access (AES encryption).

I also needed a project to experiment with the amazon SQS service and learn some more python.

# Install
* git clone this code
* copy config_sample.py to config.py and adjust queue names
* install python 3 from https://www.continuum.io/downloads (windows) or brew install python3 (mac)
* pip3 install -r requirements.txt
* setup IAM policy and keys for sqs permission (see sample_iam.json)
* assign the policy to your IAM user and create one for your friend
* configure aws with 'aws configure' and use keys with SQS permission
* setup an aws queue for tx and rx (transmit and receive, you must check "Content-Based Deduplication")
* get your buddy to setup a copy of the code and python3
* modify the txqueue and rxqueue variables to match your queue names
* flip them around for your buddy or use /swap after startup
* pick a 4 digit pin on startup shared via another secure means
* optionally change the key variable to some other key or use key = Fernet.generate_key() 

# Run
* run the code
* enter your 4 digit pin, share with buddy who does the same
* type a message
* /quit will leave the program
* for testing purposes you can use /swap to act like the other side and run in two terminals

# References
* https://cryptography.io/en/latest/fernet/
* http://boto3.readthedocs.io/en/latest/guide/sqs.html

# Bugs
* control-d causes it to crash
* doesn't work with python2

# AWS permissions
You will need the following access:
    "sqs:DeleteMessage",
    "sqs:GetQueueUrl",
    "sqs:ReceiveMessage",
    "sqs:SendMessage"

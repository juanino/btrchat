# btrchat
Below the Radar (btr) is meant to provide a secure transport for simple messages.
It currently requires a FIFO queue in AWS and Amazon creds to do this.
FIFO queues are not available in all regions.  You can still use whatever queue type you want
but the code doesn't check the order (you'll get the messages backwards or in random order).

# why
in cases where you can't trust SSL communication or you have a known MITM in progress
this will provide secure transport outside of SSL by using python's cryptography library and the 
the fernet high level access.

I also needed a project to experiment with the amazon SQS service and learn some more python.

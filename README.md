# pysocket
This is a simple socker server for python mostly for testing purposes. 
It can connect only to a single client, and delivers a simple message back.

Start the server with either:

    $ python pysocket.py

or 

    $ ./pysocket.py

And connect to it with, for example, netcat.

    $ nc localhost 8000

Then you can send messages from the client, and receive it back exactly. To close the connection, send `close`. To shut down the server from the client, send `quit`.

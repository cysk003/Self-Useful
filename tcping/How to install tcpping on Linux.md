To install tcptraceroute on Debian/Ubuntu:

```sh
$ sudo apt-get install tcptraceroute
```

To install tcptraceroute on CentOS/REHL, first set up RepoForge on your system, and then:

```sh
$ sudo yum install tcptraceroute
```

Finally, download tcpping from the web.

```sh
$ cd /usr/bin
$ sudo wget http://www.vdberg.org/~richard/tcpping
$ sudo chmod 755 tcpping
```

To measure network latency by using tcpping, simply run it as follows.

```sh
$ tcpping www.cnn.com
seq 0: tcp response from 157.166.240.13 [open] 82.544 ms
seq 1: tcp response from 157.166.241.10 [open] 80.771 ms
seq 2: tcp response from 157.166.241.11 [open] 80.838 ms
seq 3: tcp response from 157.166.241.10 [open] 80.145 ms
seq 4: tcp response from 157.166.240.11 [open] 86.253 ms 
```
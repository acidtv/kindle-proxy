# kindle-proxy

## Installing

```shell
$ apt-get install libxml2 libxml2-dev libxslt1-dev python-dev virtualenv pip
$ git clone https://github.com/acidtv/kindle-proxy
$ cd kindle-proxy
$ virtualenv --system-site-packages ./env
$ source env/bin/activate
$ pip install -r requirements.txt
```

If problems with lxml:

* Check this page https://stackoverflow.com/questions/18334366/out-of-memory-issue-in-installing-packages-on-ubuntu-server
* Install this package: lib32z1-dev

## Running

```shell
$ cd kindle-proxy/
$ source env/bin/activate
$ env/bin/python kindle-proxy.py -p 8080
```


## How to run

- copy app/config/config.sample.py to app/config/config.py
- change user/pass/host in app/config/config.py
- for gmail smtp you will need to change your account settings to allow less secure apps (see https://myaccount.google.com/lesssecureapps)
```
$ docker-compose up
```
or

```
$ python run.py
```

## Update docs

```
$ make clean && make text
```

## Run test

```
$ nosetests
```

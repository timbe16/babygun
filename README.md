# How to run

- copy app/config/config.sample.py to app/config/config.py
- change user/pass/host in app/config/config.py
- if you using gmail smtp you will need to change your account settings to allow to connect less secure apps (see https://myaccount.google.com/lesssecureapps)
```
$ docker-compose up
```
or

```
$ python run.py
```
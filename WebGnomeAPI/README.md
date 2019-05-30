# WebGnomeAPI

## Introduction

WebGnomeAPI is a web service that interfaces between 'PyGnome' and 'WebGnomeClient'. The GitHub page is [WebGnomeApi](https://srccontrol.orr.noaa.gov/gnome/webgnomeapi.git)



## Install

First be sure you have already installed 'PyGnome'. Then clone and checkout proper branch.
```
git clone https://srccontrol.orr.noaa.gov/gnome/webgnomeapi.git
cd webgnomeapi
git checkout develop
```

Install requirements
```
pip install -r pip_requirements.txt
pip install jsmin htmlmin pyramid_redis_sessions ujson gitpython webtest
```

### Build WebGnomeApi
Build WebGnomeApi (any of these whould work)

```
pip install ./
pip setup.py develop
pip setup.py compilejson
```

### Test the server 
Install a `redis-server` (if not installed):
```
sudo apt install redis-server
```

Run a redis-server:
```
redis-server
```

Run the WebGnome tests:
```
py.test webgnome_api/tests
```

## Errors

### If redis can't start

Check which processes are listening in each port:
```
sudo lsof -i -P -n | grep LISTEN
```

Stop the srver:
```
sudo service redis-server stop
```

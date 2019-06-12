# WebGnomeClient

## Introduction

WebGnomeClient is a Javascript client that uses WebGnomeAPI to run `py_gnome`.
Git is [WebGnomeClient](https://github.com/NOAA-ORR-ERD/WebGnomeClient)

## Install

First be sure you have already installed 'PyGnome'. Then clone and checkout proper branch.
```
git clone git@github.com:NOAA-ORR-ERD/WebGnomeClient.git
cd WebGnomeClient
```

Install requirements
```
sudo apt install nodejs npm node-grunt-cli node-less
```

Install WebGnomeClient and dependencies using npm
```
npm install
```

Setting up, compile and documentation. It compiles a single index.html file.
```
grunt develop
grunt build
grunt docs
```

Start the http server:
```
grunt serve
```

Testing using selenium:
```
grunt test
```



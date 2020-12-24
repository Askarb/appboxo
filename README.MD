# Appboxo sample application: CRUD user

## setup

```sh
$ git clone https://github.com/Askarb/appboxo.git
$ cd appboxo
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv -p python3 venv
$ source venv/bin/activate
```

Then install the dependencies:

```sh
(venv)$ pip install -r requirements.txt
```

Then copy `.env.sample` file and set `DATABASE_URL`:

```sh
(venv)$ cp project/main/.env.sample project/main/.env
```

Move to project folder and run test:
```sh
(venv)$ cp project/
(venv)$ pytest
```

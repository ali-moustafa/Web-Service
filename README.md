# Web-Service

## About

Made using **Python 3.11** + **Flask**. 

Testing is done using **untitest** module.

## Important Instructions

Using Postman (recommended) for example:
- Use: `http://localhost:5000/`

## How to run

## Prerequisites

\[Optional\] Install virtual environment:

```bash
$ python -m virtualenv env
```

\[Optional\] Activate virtual environment:

On macOS and Linux:
```bash
$ source env/bin/activate
```

On Windows:
```bash
$ .\env\Scripts\activate
```

Install dependencies:
```bash
$ pip install -r requirements.txt
```

run app from cli:
```bash
$ cd <path_to_root_directory>
$ python web_app/app.py
```

### Docker

It is also possible to run the app using docker:

Build the Docker image:
```bash
$ docker build -t web-app -f Dockerfile .
```

Run the Docker container:
```bash
$ docker run --rm -i -p 5000:5000 web-app
```
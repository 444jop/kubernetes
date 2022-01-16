FROM python:3.6

run pip install flask

copy . /opt/

expose 8080

workdir /opt

entrypoint ["python", "app.py"]
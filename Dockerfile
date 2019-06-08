FROM python:3.7-alpine
MAINTAINER Oliver Wehrens <oliver@wehrens.de>
COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY . /app
WORKDIR /app
ENTRYPOINT ["python3"]
CMD ["App.py"]


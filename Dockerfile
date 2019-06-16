FROM python:3.7-alpine
MAINTAINER Oliver Wehrens <oliver@wehrens.de>
COPY requirements.txt /
RUN pip install -r /requirements.txt
RUN mkdir /app
COPY conf/users.txt /app
COPY conf/openhab-config.txt /app
COPY *.py /app/
WORKDIR /app
ENTRYPOINT ["gunicorn"]
CMD ["wsgi:app", "--bind", "0.0.0.0:5000"]


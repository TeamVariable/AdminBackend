FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /admindata/

RUN apt-get update && apt-get -y install libpq-dev
RUN apt-get install -y netcat

COPY requirements.txt /admindata/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /admindata/

# static file 
RUN python manage.py collectstatic --no-input

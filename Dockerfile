FROM python:3.13

RUN mkdir /app
RUN useradd app
WORKDIR /app
RUN pip install -U pip

COPY requirements.txt /app/
RUN pip install -r requirements.txt

USER app:app

COPY main /app/main
COPY boycott_ietf_127 /app/boycott_ietf_127
COPY manage.py /app/manage.py
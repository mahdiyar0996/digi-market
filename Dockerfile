FROM python:3.11
RUN groupadd mahdiyar && useradd mahdiyar -g mahdiyar -s /usr/bin/sh
USER mahdiyar
WORKDIR /app
USER root
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
USER mahdiyar
EXPOSE 8000
CMD python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000
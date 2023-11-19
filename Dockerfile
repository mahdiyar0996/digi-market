FROM python:3.11
RUN groupadd mahdiyar && useradd mahdiyar -g mahdiyar -s /usr/bin/sh
USER mahdiyar
WORKDIR /app
USER root
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY ../requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY .. .
USER mahdiyar
LABEL framework="django"
LABEL database="mysql"
LABEL cache="redis"
EXPOSE 8000
RUN echo yes | python3 manage.py collectstatic
CMD python3 manage.py migrate && gunicorn --bind 0.0.0.0:8000 main.wsgi:application
#CMD python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000

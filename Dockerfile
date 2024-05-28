FROM python:3.9
LABEL maintainer="oleg_filipenkov"

ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN #adduser --disabled-password --no-create-home django-user

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
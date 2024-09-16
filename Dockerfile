FROM python:3.10-slim-buster AS build

WORKDIR /app

COPY . /app

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

CMD ["python3", "manage.py", "runserver", "--port", "8000"]
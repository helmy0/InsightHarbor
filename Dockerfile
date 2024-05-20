FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

RUN python3 manage.py collectstatic --no-input

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000", "--noreload", "--insecure"]

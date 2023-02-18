FROM python:3.9

WORKDIR /usr/app
COPY ./requirements.txt /usr/app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /usr/app/requirements.txt
COPY ./webapp /usr/app
CMD ["uvicorn", "webapp.main.application:app", "--host", "0.0.0.0", "--port", "80"]
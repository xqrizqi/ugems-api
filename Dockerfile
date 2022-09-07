FROM python:3.10.6-alpine3.16

COPY * /app/

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]


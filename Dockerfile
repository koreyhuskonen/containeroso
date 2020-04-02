FROM python:3.7-slim-stretch

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY /source .

EXPOSE 5000

CMD [ "python", "./index.py" ]

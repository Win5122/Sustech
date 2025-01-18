FROM python:3-slim

WORKDIR /app

COPY requirements.txt app.py ./

RUN pip3 install --no-cache-dir -r requirements.txt

CMD [ "python", "app.py" ]

FROM python:3.12-slim

WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/** .

CMD [ "python", "torrent-manager.py"]

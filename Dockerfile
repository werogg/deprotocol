FROM python:3.10-slim-buster

ENV LD_LIBRARY_PATH=/app/libs

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN rm -rf /app/bin
RUN find . -type f -name '*.tar.gz' -delete

CMD [ "python", "main.py" ]

FROM python:3.8
WORKDIR /app
COPY requirements.txt requirements.txt
EXPOSE 5052
RUN pip3 install -r requirements.txt

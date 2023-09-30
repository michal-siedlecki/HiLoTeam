FROM python:3
WORKDIR /core
ENV PYTHONUNBUFFERED=1
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . /core

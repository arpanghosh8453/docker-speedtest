FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN python -m pip install -r requirements.txt
RUN apt-get update && apt-get install gnupg1 apt-transport-https dirmngr lsb-release curl -y
RUN curl -s https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | bash
RUN apt-get install speedtest



WORKDIR /app
COPY . /app

CMD ["python", "speedmeter.py"]
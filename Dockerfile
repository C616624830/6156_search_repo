# syntax=docker/dockerfile:1
FROM python:3.7-slim
WORKDIR /6156_search_repo
ENV FLASK_DEBUG=1
COPY . .
RUN pip3 install -r requirements.txt
CMD ["python3", "app.py"]

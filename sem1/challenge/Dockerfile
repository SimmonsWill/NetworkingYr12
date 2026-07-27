FROM python:3.12-alpine
WORKDIR /app
COPY app/requirements.txt .
RUN pip install -r requirements.txt
COPY app/ .
EXPOSE 8090
CMD ["python", "app.py"]

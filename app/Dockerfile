FROM python:3.8
COPY . .
WORKDIR .
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONUNBUFFERED=TRUE
ENTRYPOINT ["python", "main.py"]
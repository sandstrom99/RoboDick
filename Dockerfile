FROM python:3.10

COPY . .

ADD main.py .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["python", "./main.py"]
FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt

COPY tests/ ./tests/

EXPOSE 8000

CMD ["uvicorn", "tests.test_api:app", "--host", "0.0.0.0", "--port", "8000"]

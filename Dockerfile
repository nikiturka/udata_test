FROM python:3.12

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Download Playwright browser
RUN playwright install --with-deps chromium

COPY . .
FROM python:3.7.2-alpine3.8

WORKDIR /user/src/app

RUN apk update
RUN apk add tar wget openjdk8 chromium chromium-chromedriver

# download and install redpen
RUN wget https://github.com/redpen-cc/redpen/releases/download/redpen-1.10.1/redpen-1.10.1.tar.gz
RUN tar xvf redpen-1.10.1.tar.gz
RUN mkdir -p /user/local/redpen
RUN mv redpen-distribution-1.10.1 /usr/local/redpen
ENV PATH="/usr/local/redpen/bin:${PATH}"

# install python package
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "./auto_submit_daily_report.py"]

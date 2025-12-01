FROM python:3.11-slim

# Install dependencies needed for Chrome + Selenium
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    libnss3 \
    libxss1 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgbm1 \
    libasound2 \
    libu2f-udev \
    fonts-liberation \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Add Google Chrome signing key (modern method)
RUN mkdir -p /etc/apt/keyrings && \
    wget -qO- https://dl.google.com/linux/linux_signing_key.pub \
        | gpg --dearmor -o /etc/apt/keyrings/google-linux-signing-keyring.gpg

# Add Chrome repository
RUN echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-linux-signing-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
        > /etc/apt/sources.list.d/google-chrome.list

# Install Google Chrome
RUN apt-get update && apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Install matching ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') && \
    wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/$CHROME_VERSION/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver.zip -d /tmp/ && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver

# Install Selenium, pytest, requests
RUN pip install selenium pytest requests

# Add tests
WORKDIR /tests
COPY tests /tests
COPY selenium-docker/run_tests.sh /tests
RUN chmod +x /tests/run_tests.sh

CMD ["./run_tests.sh"]

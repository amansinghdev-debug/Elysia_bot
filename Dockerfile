FROM python
WORKDIR /app
COPY requirements.txt
RUN pip install -r requirements.txt

# ✅ This line downloads the browser!
RUN playwright install chromium
COPY . .
CMD ["python", "main.py"]

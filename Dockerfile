FROM python:3.8
LABEL author 'Grant Meng <grantmeng@hotmail.com>'
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD python3 app.py

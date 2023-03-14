FROM python:3.9.2

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5530

#CMD python3 collector.py

CMD [ "python3", "collector.py" ]
FROM python
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y ffmpeg
CMD python -u ./server.py

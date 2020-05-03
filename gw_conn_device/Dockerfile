FROM python:3.7-slim
WORKDIR /app
COPY . /app
RUN python3 -m pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 80
ENV NAME World
CMD ["python3", "__main__.py"]
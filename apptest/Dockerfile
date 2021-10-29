From python:3.7.5-slim
RUN pip install pytest==5.2.0 requests==2.22.0
WORKDIR /src
COPY ./src/test_app.py /src/test_app.py
ENV APP_HOST 127.0.0.1
ENV APP_PORT 80
CMD ["tail", "-f", "/dev/null"]
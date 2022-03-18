# start by pulling the python image
FROM python:3.8

# define working directory for container
WORKDIR /app

# install dependencies
RUN pip install cython
RUN pip install numpy
RUN pip install pandas
RUN pip install flask

# copy files from local folder to container
COPY . /app

# code to run webapplication
ENTRYPOINT [ "python" ]
CMD ["app.py" ]


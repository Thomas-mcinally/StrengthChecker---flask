# start by pulling the python image
FROM python:3.8

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install cython
RUN pip install numpy
RUN pip install pandas
RUN pip install flask

# copy every content from the local folder to the image
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]
CMD ["app.py" ]


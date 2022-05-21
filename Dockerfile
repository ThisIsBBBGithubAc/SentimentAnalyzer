# start by pulling the python image
FROM python:3.8

# copy the requirements file into the image
COPY ./requirements.txt /bbb_app/requirements.txt

# switch working directory
WORKDIR /bbb_app

# install the dependencies and packages in the requirements file
RUN pip install --no-cache-dir --upgrade -r /bbb_app/requirements.txt


# copy every content from the local file to the image
COPY . /bbb_app

# configure the container to run in an executed manner
ENTRYPOINT [ "python3" ]

CMD ["uvicorn", "run:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]

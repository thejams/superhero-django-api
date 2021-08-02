FROM python:3.8-slim

# Set the current working directory inside the container 
ENV PROJECT_ROOT /app
WORKDIR $PROJECT_ROOT

# set environment variables  
ENV PYTHONUNBUFFERED 1 

# install dependencies  
RUN pip install --upgrade pip

# Copy the source from the current directory to the working Directory inside the container 
COPY . .

# install project dependencies
RUN pip install pyyaml uritemplate &&\ 
    pip install coreapi &&\ 
    pip install -r requirements.txt  

# port where the Django app runs  
EXPOSE 8000  

# make migrations and start server
CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000

FROM python:3.11.4

# Set PYTHONPATH to include the directory containing the data_scrape module
ENV PYTHONPATH="${PYTHONPATH}:/usr/src/app/V1/scrape"

# Copy Files
WORKDIR /usr/src/app
COPY V1/app.py V1/app.py
COPY V1/web V1/web
COPY V1/scrape/data_scrape.py /usr/src/app/V1/scrape/data_scrape.py
COPY V1/scrape/custom_functions.py /usr/src/app/V1/scrape/custom_functions.py

# Install
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Docker Run Command
EXPOSE 80
ENV FLASK_APP=/usr/src/app/V1/app.py
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0", "--port=80"]

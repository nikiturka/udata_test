# Tesk Task - Junior Full Python Developer

### Installation
clone:
```shell
git clone https://github.com/nikiturka/udata_test
```
switch to the project folder:
```shell
cd udata_test
```
Building the docker image:
```
docker-compose build
```

Raising docker-compose:
```
docker-compose up
```

### *[The API Documentation](127.0.0.1:8000/docs)*

### Description
This project uses <kbd>FastAPI</kbd> for the API and <kbd>BeautifulSoup4</kbd> + <kbd>Playwright</kbd> for web scraping. The main file of the project
is src/main.py. Upon startup, it creates the necessary database tables if they don't already exist, and begins the 
scraping process in the background while the API remains available.

The <kbd>.env</kbd> file is included in <kbd>.gitignore</kbd>, but for demonstration purposes, I've provided an 
<kbd>.env.example</kbd> file to ensure everything works correctly.
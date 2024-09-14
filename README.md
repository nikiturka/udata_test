# INSTRUCTION
1) Open the folder where you want to download the project in your IDE.
2) In the terminal, execute the following commands:
    - <kbd> git clone https://github.com/nikiturka/udata_test </kbd>
    - <kbd>cd udata_test</kbd>
    - <kbd>docker-compose up --build</kbd>
3) Docker will build the image, create the database tables at FastAPI app startup, and run the project. You can now 
access the API at [127.0.0.1:8000/docs](127.0.0.1:8000/docs)

# DESCRIPTION
This project uses <kbd>FastAPI</kbd> for the API and <kbd>BeautifulSoup4</kbd> + <kbd>Playwright</kbd> for web scraping. The main file of the project
is src/main.py. Upon startup, it creates the necessary database tables if they don't already exist, and begins the 
scraping process in the background while the API remains available.

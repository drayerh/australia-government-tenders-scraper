# Australian Government Tenders Scraper

## Overview
This project scrapes tender information from Australian government websites and stores the data in MongoDB and DigitalOcean Spaces.

## Prerequisites
- Python 3.8+
- MongoDB
- DigitalOcean Spaces
- Scrapy
- Docker (for production)

## Installation

### Development
1. Clone the repository:
    ```sh
    git clone https://github.com/drayerh/australia-government-tenders-scraper.git
    cd australian-government-tenders-scraper
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    ```sh
    cp .env.example .env
    # Edit .env to include your MongoDB and DigitalOcean credentials
    ```

5. Run the scraper:
    ```sh
    scrapy crawl base_tender
    ```

### Production
1. Build the Docker image:
    ```sh
    docker build -t tenders-scraper .
    ```

2. Run the Docker container:
    ```sh
    docker run --env-file .env -d tenders-scraper
    ```

## Configuration
- MongoDB URI and Database: Set in `.env` file
- DigitalOcean Spaces credentials: Set in `.env` file

## Environment Variables
- `MONGO_URI`: MongoDB connection string
- `MONGO_DATABASE`: MongoDB database name
- `DO_KEY`: DigitalOcean Spaces access key
- `DO_SECRET`: DigitalOcean Spaces secret key
- `DO_BUCKET`: DigitalOcean Spaces bucket name

## License
This project is licensed under the MIT License.
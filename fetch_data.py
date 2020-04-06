import requests
import json
import logging


url = "https://api.covid19india.org/data.json"


if __name__ == "__main__":
    logging.basicConfig(filename='fetch.log', filemode='a+', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    try:
        data = requests.get(url)
        if data.status_code == 200:
            try:
                s = json.dumps(data.json())
                open("data.json", "w").write(s)
            except Exception as e:
                logging.error("Exception occured", exc_info=True)
        else:
            logging.info("API response status was " +  str(data.status_code))
        print("Ran")
    except Exception as e:
        logging.error("Exception occured", exc_info=True)

import logging
from .config import LOGS_SOURCE_FILE_NAME,LOGS_SOURCE_FILE_PATH,DESTINATION_FILE_NAME,DESTINATION_FILE_PATH
logging.basicConfig(format='Date-Time : %(asctime)s : Line No. : %(lineno)d - %(message)s', level=logging.DEBUG)

LOGS_SOURCE_FILE_PATH = f"/Users/Nitya/airflow/logs/dag_processor_manager/"
LOGS_SOURCE_FILE_NAME = "dag_processor_manager.log"
DESTINATION_FILE_PATH = r"/Users/Nitya/Desktop/Koushik/"
DESTINATION_FILE_NAME = r"dags_logs.log"


def main():
    try:
        with open(LOGS_SOURCE_FILE_PATH + LOGS_SOURCE_FILE_NAME, 'r') as fi:
            with open(DESTINATION_FILE_PATH + DESTINATION_FILE_NAME, 'a') as desf:
                desf.write(fi.read())
        return f"Success - {DESTINATION_FILE_PATH + DESTINATION_FILE_NAME}  is create"
    except FileNotFoundError as error:
        logging.error("%s : File not found - %s ", __name__, str(error))
    except Exception as err:
        logging.error("%s : Error at fetching logs - %s", __name__, err)


if __name__ == "__main__":
    main()

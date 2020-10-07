import logging
import re
from logsparsing.config import DESTINATION_FILE_PATH,DESTINATION_FILE_NAME,PROCESSED_ERRORS_FILE,PROCESSED_ERRORS_PATH
logging.basicConfig(format='Date-Time : %(asctime)s : Line No. : %(lineno)d - %(message)s', level=logging.DEBUG)

filter_pattern = "Fail|Error"


def main():
    try:
        with open(PROCESSED_ERRORS_PATH+PROCESSED_ERRORS_FILE, 'a') as fi:
            with open(DESTINATION_FILE_PATH+DESTINATION_FILE_NAME, "r") as logfi:
                for line in logfi.readlines():
                    if re.findall(filter_pattern, line):
                        fi.write(line)
    except FileNotFoundError as error:
        logging.error("%s : File not found - %s ", __name__, str(error))
    except Exception as err:
        logging.error("%s : Error at fetching logs - %s", __name__, err)

    return f"{PROCESSED_ERRORS_PATH+PROCESSED_ERRORS_FILE} is created..!!"


if __name__ == "__main__":
    main()
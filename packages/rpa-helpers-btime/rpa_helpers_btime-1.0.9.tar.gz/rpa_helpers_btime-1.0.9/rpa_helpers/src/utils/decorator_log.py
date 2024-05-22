from loguru import logger
from functools import wraps
import datetime
import sys
import uuid
from rpa_helpers.src.models.repository.repository_log import LogRepository
from rpa_helpers.src.models.repository.repository_rpa import RpaRepository

logger.add(sys.stdout, format="{time} | {message} | {level}", level="INFO")

log_db = LogRepository()
rpa_db = RpaRepository()
uuid_execution = uuid.uuid1()

def log(description):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            try:
                result = func(*args, **kwargs)
                end_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                logger_format_success = {
                    "message": f"Function '{func.__name__}' executed successfully.",
                    "status": "Success",
                    "start_time": start_time,
                    "end_time": end_time,
                    "description": description,
                    "rpa_id": 1, # Fazer uma constante na config do projeto
                    "execution_id": uuid_execution
                }

                log_db.insert(
                    message=logger_format_success["message"],
                    status=logger_format_success["status"],
                    description=logger_format_success["description"],
                    start_date=logger_format_success["start_time"],
                    end_date=logger_format_success["end_time"],
                    rpa_id=logger_format_success["rpa_id"],
                    execution_id=logger_format_success["execution_id"],

                )

                logger.info(logger_format_success)
                return result
            except Exception as e:
                end_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                logger_format_failure = {
                    "message": f"Function '{func.__name__}' failed with error: {str(e)}",
                    "status": "Failure",
                    "start_time": start_time,
                    "end_time": end_time,
                    "description": description,
                    "rpa_id": 1, # Fazer uma constante na config do projeto
                    "execution_id": uuid_execution
                }
                logger.error(logger_format_failure)

                log_db.insert(
                    message=logger_format_failure["message"],
                    status=logger_format_failure["status"],
                    description=logger_format_failure["description"],
                    start_date=logger_format_failure["start_time"],
                    end_date=logger_format_failure["end_time"],
                    rpa_id=logger_format_failure["rpa_id"],
                    execution_id=logger_format_failure["execution_id"],
                )                
                raise

        return wrapper

    return decorator
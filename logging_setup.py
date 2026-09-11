import logging
from datetime import datetime, timezone
from elasticsearch import Elasticsearch

es_client = Elasticsearch("http://elasticsearch:9200")

class ElasticsearchHandler(logging.Handler):
    def emit(self, record):
        try:
            log_entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "level": record.levelname,
                "message": record.getMessage(),
                "logger": record.name,
            }
            es_client.index(index="recruiter-call-platform-logs", document=log_entry)
        except Exception:
            pass  # never let logging failures crash the app

def setup_logging():
    logger = logging.getLogger("recruiter-call-platform")
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(console_handler)

    es_handler = ElasticsearchHandler()
    logger.addHandler(es_handler)

    return logger
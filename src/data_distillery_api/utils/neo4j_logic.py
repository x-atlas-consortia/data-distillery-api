import logging
import neo4j
from typing import List
import os

logging.basicConfig(format='[%(asctime)s] %(levelname)s in %(module)s:%(lineno)d: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def loadquerystring(filename: str) -> str:

    # Load a query string from a file.
    # filename: filename, without path.

    # Assumes that the file is in the cypher directory.

    fpath = os.path.dirname(os.getcwd())
    fpath = os.path.join(fpath, 'src/data_distillery_api/cypher', filename)

    f = open(fpath, "r")
    query = f.read()
    f.close()
    return query


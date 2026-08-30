# Dependencies
from utils import file_utils
import json

DATA_ROUTE = "data/transcripts"


if __name__ == "__main__":

    transcripts = file_utils.extract_transcripts(DATA_ROUTE)
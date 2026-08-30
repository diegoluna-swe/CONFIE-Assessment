# Dependencies
from pathlib import Path

class Transcript:
    def __init__(self, id: str, content: str):
        self.id = id
        self.content = content

# Route
def extract_transcripts(folder: str) -> dict[str, Transcript]:

    # Routing
    data_route = Path(__file__).resolve().parent.parent.parent / folder

     # Message
    print(f"Reading files under {data_route}...")

    data_buffer: dict[str, Transcript] = {}
    total_files: int = 0

    for file in data_route.iterdir():
        if file.is_file():
            try:
                
                id = file.stem
                content = file.read_text(encoding="utf-8")                
                data_buffer[file.stem] = content
                total_files += 1

            except Exception as e:
                print(f"There was an error while reading {file.id}, skipping to next file.")
                continue

    print(f"Read {total_files} total files.")

    return data_buffer
import sys
from pathlib import Path

import requests
import zstandard as zstd

REPLAY_DIR = Path(r"D:\SteamLibrary\steamapps\common\dota 2 beta\game\dota\replays")


def get_replay_url(match_id):
    print(f"Looking up match {match_id} on OpenDota...")

    url = f"https://api.opendota.com/api/matches/{match_id}"
    data = requests.get(url, timeout=30).json()

    cluster = data["cluster"]
    replay_salt = data["replay_salt"]

    if not replay_salt:
        raise RuntimeError("No replay is available for this match. Try parsing.")

    replay_url = (
        f"http://replay{cluster}.valve.net/570/{match_id}_{replay_salt}.dem.bz2"
    )

    print(f"Replay found: {replay_url}")
    return replay_url


def download_replay(url, path):

    if path.exists():
        print(f"Replay already downloaded: {path}")
        return

    print(f"Downloading replay:\n{url}")

    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        stream=True,
        timeout=(10, 120),
    )
    response.raise_for_status()

    total = int(response.headers.get("Content-Length", 0))
    downloaded = 0

    with path.open("wb") as file:
        for chunk in response.iter_content(1024 * 1024):
            file.write(chunk)
            downloaded += len(chunk)

            if total:
                print(
                    f"\r{downloaded / total:.0%}",
                    end="",
                    flush=True,
                )

    print("\nDownload complete.")


def extract_replay(source, destination):
    print(f"Extracting replay to: {destination}")

    with open(source, "rb") as compressed, open(destination, "wb") as replay:
        zstd.ZstdDecompressor().copy_stream(compressed, replay)

    print("Extraction complete.")


def main():
    if len(sys.argv) != 2:
        print("Usage: python dota_replay_importer.py <match_id>")
        sys.exit(1)

    match_id = int(sys.argv[1])
    compressed = REPLAY_DIR / f"{match_id}.dem.bz2"
    replay = REPLAY_DIR / f"{match_id}.dem"

    replay_url = get_replay_url(match_id)
    download_replay(replay_url, compressed)
    extract_replay(compressed, replay)

    print("Cleaning up compressed replay...")
    compressed.unlink()

    print(f"\nDone! Replay ready at:\n{replay}")


if __name__ == "__main__":
    main()

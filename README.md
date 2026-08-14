# Dota 2 Replay Importer

A small Python script that downloads Dota 2 replays by Match ID and places them directly into the game's `replays` folder.

## Requirements

* Python 3.10+
* [`requests`](https://pypi.org/project/requests/)
* [`zstandard`](https://pypi.org/project/zstandard/)

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python dota_replay_importer.py <match_id>
```


## Configuration

**IMPORTANT:** Set your Dota 2 replay directory at the top of `dota_replay_importer.py`:

```python
REPLAY_DIR = Path(r"D:\SteamLibrary\steamapps\common\dota 2 beta\game\dota\replays")
```

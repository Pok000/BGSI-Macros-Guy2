import base64
import os
import re
import time
import urllib.request
import urllib.parse
from typing import List, Dict, Tuple


def run_decryption(encrypted_text_b64: str, out_path: str = "decrypted_output.py"):
    """
    Decode Base64, XOR-decrypt with the app key, write raw bytes to out_path (wb).
    """
    # normalize and fix padding
    s = "".join(encrypted_text_b64.split())
    s += "=" * ((4 - len(s) % 4) % 4)

    try:
        decoded_bytes = base64.b64decode(s)
    except Exception as e:
        print(f"Base64 decode error: {e}")
        return False

    def xor_decrypt(data: bytes, key: bytes) -> bytes:
        return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

    key = b"aK3pQv9XmRzT1bHnW6LuF2YgDeCsJ4"
    decrypted_bytes = xor_decrypt(decoded_bytes, key)

    try:
        with open(out_path, "wb") as wf:
            wf.write(decrypted_bytes)
    except Exception as e:
        print(f"Failed to write {out_path}: {e}")
        return False

    # try to show a small utf-8 preview (best-effort)
    try:
        preview = decrypted_bytes[:1024].decode("utf-8", errors="replace")
        print(
            f"Wrote {out_path} ({len(decrypted_bytes)} bytes). Preview:\n{preview.splitlines()[:20]}"
        )
    except Exception:
        print(f"Wrote {out_path} ({len(decrypted_bytes)} bytes). (no preview)")

    return True


def parse_filename_version(filename: str) -> Tuple[str, Tuple[int, ...]]:
    """
    Extract base name and version tuple from a filename like "Auto Obby v21.1.py".
    If no version found, return version (0,).
    """
    m = re.match(r"^(?P<base>.+?)\s+v(?P<ver>\d+(?:\.\d+)*)\.py$", filename, flags=re.IGNORECASE)
    if m:
        base = m.group("base").strip()
        ver = tuple(int(x) for x in m.group("ver").split("."))
        return base, ver
    base = filename.rsplit(".py", 1)[0].strip()
    return base, (0,)


def pick_newest(filenames: List[str]) -> List[str]:
    """
    From a list of filenames (like 'Auto Obby v21.1.py|...'), extract the filename part,
    group by base, and return only the newest filename for each base.
    """
    groups: Dict[str, Tuple[Tuple[int, ...], str]] = {}
    for entry in filenames:
        name = entry.split("|", 1)[0].strip()
        base, ver = parse_filename_version(name)
        cur = groups.get(base)
        if cur is None or ver > cur[0]:
            groups[base] = (ver, name)
    return [v[1] for v in groups.values()]


def download_text(url: str, timeout: int = 15, retries: int = 2) -> str:
    last_exc = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as resp:
                data = resp.read()
                # best-effort decode as utf-8
                return data.decode("utf-8", errors="replace")
        except Exception as e:
            last_exc = e
            time.sleep(0.5)
    raise last_exc


def fetch_and_decrypt_scripts(entries: List[str], base_url: str = "https://guy2-macros.com/scripts/", out_dir: str = "downloaded_scripts"):
    os.makedirs(out_dir, exist_ok=True)
    newest = pick_newest(entries)
    print(f"Selected {len(newest)} newest scripts to fetch.")
    results = []
    for fname in newest:
        quoted = urllib.parse.quote(fname)
        url = base_url.rstrip("/") + "/" + quoted
        print(f"Fetching {fname} from {url} ...")
        try:
            payload = download_text(url)
        except Exception as e:
            print(f"  Failed to download {fname}: {e}")
            continue
        # quick sanity check for HTML 404 pages
        if "<html" in payload.lower() or "not found" in payload.lower():
            print(f"  Skipping {fname}: server returned HTML / not found.")
            continue
        out_path = os.path.join(out_dir, fname)
        ok = run_decryption(payload, out_path=out_path)
        results.append((fname, ok, out_path))
    print("Done.")
    return results


if __name__ == "__main__":
    scripts = [
      "Dart v8.3.py|Pops balloons in the Dart minigame|member|BGSI",
      "BoardGame v8.1.py|Plays the Board Game minigame and gets inf elixirs|member|BGSI",
      "FastHatch v8.1.py|Faster egg hatching and hatched eggs counter|member|BGSI",
      "Dart v10.1.py|Pops balloons in the Dart minigame|member|BGSI",
      "BoardGame v10.1.py|Plays the Board Game minigame and gets inf elixirs|member|BGSI",
      "Dart v11.1.py|Pops balloons in the Dart minigame|member|BGSI",
      "Dart v12.1.py|Pops balloons in the Dart minigame|member|BGSI",
      "BoardGame v12.1.py|Plays the Board Game minigame and gets inf elixirs|member|BGSI",
      "PetMatch v12.1.py|Plays the Pet Match minigame|member|BGSI",
      "PetMatch v12.2.py|Plays the Pet Match minigame|member|BGSI",
      "Dart v12.2.py|Pops balloons in the Dart minigame|member|BGSI",
      "TeamEnchant v12.1.py|Enchants your whole team to a specific enchant|member|BGSI",
      "TeamEnchant v13.1.py|Enchants your whole team to a specific enchant|member|BGSI",
      "FastHatch v13.1.py|Faster egg hatching and hatched eggs counter|member|BGSI",
      "BoardGame v13.1.py|Plays the Board Game minigame and gets inf elixirs|member|BGSI",
      "Dart v13.1.py|Pops balloons in the Dart minigame|member|BGSI",
      "PetMatch v13.1.py|Plays the Pet Match minigame|member|BGSI",
      "TeamEnchant v13.2.py|Enchants your whole team to a specific enchant|member|BGSI",
      "Dart v13.2.py|Pops balloons in the Dart minigame|member|BGSI",
      "BasicComp v14.1.py|Plays the competetive thing idk|member|BGSI",
      "BoardGame v14.1.py|Plays the Board Game minigame and gets inf elixirs|member|BGSI",
      "BasicComp v14.2.py|Plays the competetive thing idk|member|BGSI",
      "BasicComp v14.3.py|Plays the competetive thing idk|member|BGSI",
      "BasicComp v14.4.py|Plays the competetive thing idk|member|BGSI",
      "BasicComp v14.5.py|Plays the competetive thing idk|member|BGSI",
      "AutoFish v15.1.py|Fishes fish in fishing simulator infinity (bgsi)|member|BGSI",
      "QuestBoard v15.1.py|Automatically does the fishing board quests|member|BGSI",
      "QuestBoard v15.2.py|Automatically does the fishing board quests|member|BGSI",
      "PetMatch v15.1.py|Plays the Pet Match minigame|member|BGSI",
      "AutoFish v15.2.py|Fishes fish in fishing simulator infinity (bgsi)|member|BGSI",
      "BoardGame v15.1.py|Plays the Board Game minigame and gets inf elixirs|member|BGSI",
      "QuestBoard v15.3.py|Automatically does the fishing board quests|member|BGSI",
      "FastHatch v15.1.py|Faster egg hatching and hatched eggs counter|member|BGSI",
      "AutoFish v15.3.py|Fishes fish in fishing simulator infinity (bgsi)|member|BGSI",
      "QuestBoard v15.4.py|Automatically does the fishing board quests|member|BGSI",
      "TeamEnchant v16.1.py|Enchants your whole team to a specific enchant|member|BGSI",
      "Dart v16.1.py|NUKES all the balloons in the dart minigame|member|BGSI",
      "QuestBoard v16.1.py|Automatically does the fishing board quests|member|BGSI",
      "Dart v16.2.py|NUKES all the balloons in the dart minigame|member|BGSI",
      "QuestBoard v17.1.py|Automatically does the fishing board quests|member|BGSI",
      "AutoFish v17.1.py|Fishes fish in fishing simulator infinity (bgsi)|member|BGSI",
      "FastBox v17.1.py|Opens mystery boxes 12.5% faster than auto open|member|BGSI",
      "FastBox v17.2.py|Opens mystery boxes 25% faster than auto open|member|BGSI",
      "Dart v17.1.py|NUKES all the balloons in the dart minigame|member|BGSI",
      "Auto Obby v21.1.py|Auto completes easy, medium and hard obbies|donator|BGSI",
      "BoardGame v22.1.py|Plays the Board Game minigame and gets inf elixirs|member|BGSI",
      "Dart v22.1.py|NUKES all the balloons in the dart minigame|member|BGSI",
      "BoardGame v22.2.py|Plays the Board Game minigame and gets inf elixirs|member|BGSI",
      "AutoMaze v23.1.py|Completes the Maze Minigame|giveaway_sponsor|BGSI",
      "AutoMaze v23.2.py|Completes the Maze Minigame|giveaway_sponsor|BGSI",
      "AutoMaze v23.3.py|Completes the Maze Minigame|member|BGSI",
      "FastComp v24.1.py|Fast competetive macro (130 or less ping required)|donator|BGSI",
      "FastComp v24.2.py|Fast competetive macro (130 or less ping required)|donator|BGSI",
      "FastComp v24.3.py|Fast competetive macro (130 or less ping required)|donator|BGSI",
      "TeamEnchant v24.1.py|Enchants your whole team to a specific enchant|member|BGSI",
      "Trick Or Treat v25.1.py|Automatic trick-or-treating during halloween event|member|BGSI",
      "FastBox v27.1.py|Opens mystery boxes faster than auto open|member|BGSI",
      "BoardGame v27.1.py|Plays the Board Game minigame and gets inf elixirs|member|BGSI",
      "Trick Or Treat v27.1.py|Automatic trick-or-treating during halloween event|member|BGSI",
      "Auto Obby v27.1.py|Auto completes easy, medium and hard obbies|donator|BGSI",
      "TeamEnchant v28.1.py|Enchants your whole team to a specific enchant|member|BGSI",
      "WinRes v1.1.py|QoL window alignment and resizing|member|BGSI",
      "FastHatch v28.1.py|Faster egg hatching and egg counter with secret detection|member|BGSI",
      "FastHatch v28.2.py|Faster egg hatching and egg counter with secret detection|member|BGSI",
      "FastHatch v29.1.py|Faster egg hatching and egg counter with secret detection|member|BGSI"
    ]

    # fetch newest only and decrypt into ./downloaded_scripts/
    fetch_and_decrypt_scripts(scripts, base_url="https://guy2-macros.com/scripts/", out_dir="downloaded_scripts")

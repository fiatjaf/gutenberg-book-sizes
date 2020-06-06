import os.path
import zipfile
import glob
import json
import re
from itertools import combinations

spaces = re.compile(b"\s")
multispaces = re.compile(b"\s+")
words = re.compile(b"\w+")


def main():
    with open("data", "w") as results:
        for zf in glob.glob("*.zip"):
            print(zf)
            with zipfile.ZipFile(zf) as z:
                txts = [
                    f.filename
                    for f in z.infolist()
                    if f.filename.lower().endswith(".txt")
                ]
                if len(txts) > 1:
                    all_the_same = all(
                        map(
                            lambda x: x[0] == x[1],
                            combinations(map(os.path.basename, txts), 2),
                        )
                    )
                    if not all_the_same:
                        raise Exception("more than one txt")

                txt = txts[0]
                book = z.read(txt).replace(b"\r", b"")
                start = book.find(b"START")
                start = start + book[start:].find(b"\n\n")
                start = start if start >= 0 else 0
                end = book.find(b"End of Project Gutenberg")
                bookcontent = book[start:end]

                try:
                    data = {
                        "title": get_tag(b"Title: ", book),
                        "author": get_tag(b"Author: ", book),
                        "id": zf.replace(".zip", ""),
                        "characters": len(bookcontent),
                        "letters": len(spaces.sub(b"", bookcontent)),
                        "words": len(words.findall(bookcontent)),
                    }
                except UnicodeDecodeError:
                    continue

                if data["words"] == 0 or data["letters"] == 0:
                    raise Exception("zero?")

                jdata = json.dumps(data)
                results.write(jdata + "\n")
                print("  " + jdata)


def get_tag(tag, text):
    s = text.find(tag) + len(tag)
    e = s + text[s:].find(b"\n\n")
    value = multispaces.sub(b" ", text[s:e]).strip()
    return value.decode("utf-8")


main()

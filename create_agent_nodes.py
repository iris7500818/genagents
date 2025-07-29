import json, datetime, argparse, pathlib


def ts(s):                        # "YYYY-MM-DD HH:MM:SS" → epoch
    return int(datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S").timestamp())


def convert(inputfile, outputfile):
    src = json.load(open(inputfile, encoding="utf-8"))

    # dict と list の両方に対応
    iter_rows = src.values() if isinstance(src, dict) else src

    records = []

    for row in iter_rows:                  # AGA が list で入っている前提
        node_id = row.get("node_count") or int(row.get("node_id", 0))
        dt = datetime.datetime.strptime(row["created"], "%Y-%m-%d %H:%M:%S")
        records.append({
            "node_id":  node_id,
            "node_type":    row["type"],
            "content":  row["description"],
            "importance":   row["poignancy"] * 10,
            "created":  ts(row["created"]),
            "created_time":  dt.isoformat(),
            "last_retrieved":   0,
            "pointer_id":   None,
        })

    with open(outputfile, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    convert(pathlib.Path(args.input), pathlib.Path(args.output))
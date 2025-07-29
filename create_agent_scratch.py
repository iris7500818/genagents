import json, argparse, pathlib


def convert(input, output, agent_occ):
    src = json.load(input.open(encoding="UTF-8"))

    scratch = {
        "first_name":  src["first_name"],
        "last_name":   src["last_name"],
        "age":         src["age"],
        "occupation":  agent_occ,          # 例 "Cafe owner"
        "personality": src["innate"],
        "lifestyle":   src["lifestyle"],
        "biography":   src["learned"],
        "currently":   src["currently"],
        "living_area": src["living_area"],
    }

    json.dump(scratch, output.open("w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"✅ scratch.json 生成: {output}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--occ", default="")
    args = ap.parse_args()

    convert(
        pathlib.Path(args.input),
        pathlib.Path(args.output),
        args.occ
    )
# rebuild_embeddings.py
import json, time, pathlib, openai
from tqdm import tqdm

import argparse, os


MODEL = "text-embedding-ada-002"   # or "text-embedding-3-large"


def embed_texts(texts, model=MODEL, batch=100):
    encodings = []
    for i in range(0, len(texts), batch):
        chunk = texts[i:i+batch]
        retry = 0
        while True:
            try:
                resp = openai.Embedding.create(model=model, input=chunk)
                encodings.extend([d["embedding"] for d in resp["data"]])
                break
            except openai.error.RateLimitError:
                retry += 1
                time.sleep(1.5 * retry)
    return encodings


def main(folder: pathlib.Path):
    node_path = folder/"memory_stream/nodes.json"
    emb_path  = folder/"memory_stream/embeddings.json"

    nodes  = json.load(node_path.open(encoding="utf-8"))
    texts  = [n["content"] for n in nodes]

    print(f"⏳ {len(texts)} 本の文を {MODEL} でエンコードします…")
    embeddings = embed_texts(texts)

    new_dict = {txt: vec for txt, vec in zip(texts, embeddings)}
    json.dump(new_dict, emb_path.open("w", encoding="utf-8"))
    print(f"✅ embeddings.json 更新完了 → {emb_path}")


if __name__ == "__main__":
    if "OPENAI_API_KEY" not in os.environ:
        raise RuntimeError("環境変数 OPENAI_API_KEY を設定してください")
    ap = argparse.ArgumentParser(description="nodes.json 全文を再エンコードして embeddings.json を再構築")
    ap.add_argument("agent_folder", help="<agent_folder> パス")
    args = ap.parse_args()
    main(pathlib.Path(args.agent_folder))

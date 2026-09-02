"""
双载体一致性校验器 v0.1
思路来自施工图场景的 SVG(骨)+MD(魂) 双载体法：
  - 骨(bone)   = 几何事实，坐标/图形元素
  - 魂(soul)   = 语义注解，数值/标签/说明
  - crosswalk  = 两边用同一套 ID 互联

用法:
    python validator.py                       # 内置示例
    python validator.py bone.json soul.json crosswalk.json
"""
import json
import sys
from pathlib import Path


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def validate(bone, soul, crosswalk, verbose=False):
    """返回 (matched, unclear, missing) 三张清单"""
    bone_ids = {b["id"] for b in bone["elements"]}
    matched, unclear, missing = [], [], []

    for note in soul["annotations"]:
        nid = note["bone_id"]
        if nid not in bone_ids:
            missing.append({"soul_id": note["id"], "bone_id": nid,
                            "reason": "ID 在骨中不存在（断链）"})
            continue

        b = next(x for x in bone["elements"] if x["id"] == nid)

        # 冲突裁决：几何以骨为准，值以魂为准；但数值要有独立读源背靠背核对
        if "value" in note and "value_alt" in note:
            if note["value"] != note["value_alt"]:
                unclear.append({"soul_id": note["id"], "bone_id": nid,
                                "reason": f"两源不一致: {note['value']} vs {note['value_alt']}"})
                continue

        if b.get("layer") != note.get("layer"):
            unclear.append({"soul_id": note["id"], "bone_id": nid,
                            "reason": f"图层归属冲突: 骨={b.get('layer')} 魂={note.get('layer')}"})
            continue

        matched.append({"soul_id": note["id"], "bone_id": nid})
    return matched, unclear, missing


def report(name, lst):
    print(f"\n[{name}] {len(lst)} 条")
    for x in lst:
        print("  -", json.dumps(x, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) == 4:
        bone, soul, cw = (load(p) for p in sys.argv[1:4])
    else:
        here = Path(__file__).parent
        bone = load(here / "sample_bone.json")
        soul = load(here / "sample_soul.json")
        cw = load(here / "crosswalk.json")

    m, u, ms = validate(bone, soul, cw)
    total = len(soul["annotations"])
    print(f"对账完成: total={total} matched={len(m)} unclear={len(u)} missing={len(ms)}")
    report("UNCLEAR(读不清不丢人，编数才丢人)", u)
    report("MISSING(断链)", ms)

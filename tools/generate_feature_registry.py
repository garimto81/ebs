"""Feature Checklist -> JSON Registry 변환 스크립트.

PokerGFX-Feature-Checklist.md를 파싱하여 feature-registry.json을 생성합니다.
"""

import json
import re
import sys
from pathlib import Path

CHECKLIST_PATH = Path(r"C:\claude\ebs\docs\01_PokerGFX_Analysis\PokerGFX-Feature-Checklist.md")
OUTPUT_PATH = Path(r"C:\claude\ebs\docs\01_PokerGFX_Analysis\06_Cross_Reference\feature-registry.json")


def parse_checklist(text: str) -> list[dict]:
    features = []
    current_category = ""

    # Category mapping
    category_map = {
        "1. Action Tracker": "Action Tracker",
        "2. Pre-Start Setup": "Pre-Start Setup",
        "3. Viewer Overlay": "Viewer Overlay",
        "4. GFX Console": "GFX Console",
        "5. Security": "Security",
        "6. Equity & Stats": "Equity & Stats",
        "7. Hand History": "Hand History",
        "8. Server 관리": "Server 관리",
    }

    for line in text.splitlines():
        # Detect category headers
        for key, val in category_map.items():
            if line.startswith(f"## {key}"):
                current_category = val
                break

        # Parse table rows with feature IDs
        match = re.match(
            r"\|\s*(AT|PS|VO|GC|SEC|EQ|ST|HH|SV)-(\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(P[012])\s*\|",
            line,
        )
        if match:
            prefix = match.group(1)
            num = match.group(2)
            feature_id = f"{prefix}-{num}"
            name = match.group(3).strip()
            description = match.group(4).strip()
            priority = match.group(5)

            features.append({
                "id": feature_id,
                "name": name,
                "description": description,
                "category": current_category,
                "priority": priority,
            })

    return features


def build_registry(features: list[dict]) -> dict:
    registry = {
        "$schema": "feature-registry-v1",
        "version": "1.0.0",
        "generated_from": "PokerGFX-Feature-Checklist.md v4.0.0",
        "total_features": len(features),
        "confidence_levels": {
            "V": "Verified - 코드에서 직접 확인 (파일:라인)",
            "O": "Observed - 스크린샷/매뉴얼 육안 확인",
            "I": "Inferred - 추론 (근거 명시 필수)",
        },
        "features": {},
    }

    for f in features:
        registry["features"][f["id"]] = {
            "name": f["name"],
            "category": f["category"],
            "priority": f["priority"],
            "description": f["description"],
            "sources": {
                "screenshot": None,
                "manual": None,
                "binary": None,
                "live_app": None,
                "inference": None,
            },
            "ebs_mapping": {
                "widget": None,
                "protocol_message": None,
                "db_table": None,
            },
        }

    return registry


def main():
    text = CHECKLIST_PATH.read_text(encoding="utf-8")
    features = parse_checklist(text)

    if not features:
        print("ERROR: No features parsed from checklist")
        sys.exit(1)

    registry = build_registry(features)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Summary
    categories = {}
    for f in features:
        cat = f["category"]
        categories[cat] = categories.get(cat, 0) + 1

    print(f"Total features: {len(features)}")
    for cat, count in categories.items():
        print(f"  {cat}: {count}")
    print(f"Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

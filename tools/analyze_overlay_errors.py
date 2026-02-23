"""
analyze_overlay_errors.py
OCR JSON 파일들을 파싱하여 오버레이 오차율 통계를 계산하고 출력한다.

사용법:
    python C:/claude/ebs/tools/analyze_overlay_errors.py
    python C:/claude/ebs/tools/analyze_overlay_errors.py --json
"""

import json
import sys
import glob
import os
from datetime import datetime

# ────────────────────────────────────────────────
# 상수
# ────────────────────────────────────────────────

OCR_JSON_GLOB = (
    "C:/claude/ebs/docs/01_PokerGFX_Analysis/02_Annotated_ngd/*-ocr.json"
)
OUTPUT_JSON_PATH = (
    "C:/claude/ebs/docs/01_PokerGFX_Analysis/overlay-error-analysis.json"
)

DELTA_GUARD = {"dx_max": 20, "dy_max": 12, "dw_max": 25, "dh_max": 20}

SCREEN_NAMES = {
    "01": "메인 윈도우",
    "02": "Sources 탭",
    "03": "Outputs 탭",
    "04": "GFX 1 탭",
    "05": "GFX 2 탭",
    "06": "GFX3 탭",
    "07": "Commentary 탭",
    "08": "System 탭",
    "09": "Skin Editor",
    "10": "Graphic Editor Board",
    "11": "Graphic Editor Player",
}


# ────────────────────────────────────────────────
# 헬퍼
# ────────────────────────────────────────────────


def confidence_grade(delta):
    """신뢰도 등급 반환."""
    if delta is None:
        return "N/A"
    max_d = max(abs(d) for d in delta)
    if max_d <= 3:
        return "HIGH"
    if max_d <= 8:
        return "MEDIUM"
    if max_d <= 15:
        return "LOW"
    return "CRITICAL"


def guard_violations(delta):
    """DELTA_GUARD 위반 성분 목록 반환."""
    if delta is None:
        return []
    violations = []
    if abs(delta[0]) > DELTA_GUARD["dx_max"]:
        violations.append("dx")
    if abs(delta[1]) > DELTA_GUARD["dy_max"]:
        violations.append("dy")
    if abs(delta[2]) > DELTA_GUARD["dw_max"]:
        violations.append("dw")
    if abs(delta[3]) > DELTA_GUARD["dh_max"]:
        violations.append("dh")
    return violations


def screen_id_from_path(path):
    """파일 경로에서 2자리 화면 ID 추출."""
    basename = os.path.basename(path)           # "01-main-window-ocr.json"
    return basename.split("-")[0]               # "01"


# ────────────────────────────────────────────────
# 분석 코어
# ────────────────────────────────────────────────


def analyze_files(json_paths):
    """모든 OCR JSON 파일을 파싱하여 분석 결과를 반환한다."""
    screens = []          # 화면별 결과 목록
    all_violations = []   # Guard 위반 전체 목록
    grade_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0, "CRITICAL": 0, "N/A": 0}

    total_boxes = 0
    total_delta_applied = 0
    total_ocr_recognized = 0
    total_guard_violations = 0

    for path in sorted(json_paths):
        sid = screen_id_from_path(path)
        screen_name = SCREEN_NAMES.get(sid, sid)

        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        boxes = data.get("boxes", [])
        n_boxes = len(boxes)
        n_delta = 0
        n_ocr = 0
        n_guard = 0
        delta_sums = []   # 각 박스의 max_delta
        max_delta_screen = 0

        for box in boxes:
            delta = box.get("delta")
            ocr_text = box.get("ocr_text")

            if delta is not None:
                n_delta += 1
                max_d = max(abs(d) for d in delta)
                delta_sums.append(max_d)
                if max_d > max_delta_screen:
                    max_delta_screen = max_d

                viols = guard_violations(delta)
                if viols:
                    n_guard += 1
                    all_violations.append({
                        "screen": screen_name,
                        "sid": sid,
                        "label": box.get("label", "?"),
                        "dx": delta[0],
                        "dy": delta[1],
                        "dw": delta[2],
                        "dh": delta[3],
                        "violations": viols,
                    })

            if ocr_text:
                n_ocr += 1

            grade = confidence_grade(delta)
            grade_counts[grade] += 1

        avg_delta = (sum(delta_sums) / len(delta_sums)) if delta_sums else 0.0

        screens.append({
            "sid": sid,
            "name": screen_name,
            "n_boxes": n_boxes,
            "n_delta": n_delta,
            "n_ocr": n_ocr,
            "n_guard": n_guard,
            "avg_delta": avg_delta,
            "max_delta": max_delta_screen,
        })

        total_boxes += n_boxes
        total_delta_applied += n_delta
        total_ocr_recognized += n_ocr
        total_guard_violations += n_guard

    return {
        "screens": screens,
        "all_violations": all_violations,
        "grade_counts": grade_counts,
        "total_boxes": total_boxes,
        "total_delta_applied": total_delta_applied,
        "total_ocr_recognized": total_ocr_recognized,
        "total_guard_violations": total_guard_violations,
    }


# ────────────────────────────────────────────────
# 출력 포맷터
# ────────────────────────────────────────────────


def print_report(result):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    screens = result["screens"]
    violations = result["all_violations"]
    grades = result["grade_counts"]
    total_boxes = result["total_boxes"]
    total_delta = result["total_delta_applied"]
    total_ocr = result["total_ocr_recognized"]
    total_guard = result["total_guard_violations"]

    # 헤더
    print("## 오버레이 오차율 분석")
    print(f"분석 일시: {now}")
    print("원본 파일: docs/01_PokerGFX_Analysis/02_Annotated_ngd/*-ocr.json")
    print()

    # 화면별 요약
    print("### 화면별 요약")
    header = (
        "| 화면 | 박스수 | Delta 적용 | OCR 인식 | Guard 위반 | 평균 δ | 최대 δ |"
    )
    sep = (
        "|------|--------|------------|----------|------------|--------|--------|"
    )
    print(header)
    print(sep)

    for s in screens:
        delta_pct = (s["n_delta"] / s["n_boxes"] * 100) if s["n_boxes"] else 0
        ocr_pct = (s["n_ocr"] / s["n_boxes"] * 100) if s["n_boxes"] else 0
        print(
            f"| {s['name']} | {s['n_boxes']} "
            f"| {s['n_delta']} ({delta_pct:.0f}%) "
            f"| {s['n_ocr']} ({ocr_pct:.0f}%) "
            f"| {s['n_guard']} "
            f"| {s['avg_delta']:.1f}px "
            f"| {s['max_delta']}px |"
        )

    all_delta_pct = (total_delta / total_boxes * 100) if total_boxes else 0
    all_ocr_pct = (total_ocr / total_boxes * 100) if total_boxes else 0
    print(
        f"| **전체** | **{total_boxes}** "
        f"| **{total_delta} ({all_delta_pct:.0f}%)** "
        f"| **{total_ocr} ({all_ocr_pct:.0f}%)** "
        f"| **{total_guard}** "
        f"| - | - |"
    )
    print()

    # 전체 통계
    print("### 전체 통계")
    print("| 항목 | 수치 |")
    print("|------|------|")
    print(f"| 전체 박스 | {total_boxes} |")
    print(f"| Delta 적용 박스 | {total_delta} ({all_delta_pct:.1f}%) |")
    print(f"| OCR 인식 박스 | {total_ocr} ({all_ocr_pct:.1f}%) |")
    print(f"| Guard 위반 박스 | {total_guard} |")
    print(f"| 분석 화면 수 | {len(screens)} |")
    print()

    # Guard 위반 상세
    print(f"### Guard 위반 상세 ({len(violations)}건)")
    if violations:
        print("| 화면 | 박스# | dx | dy | dw | dh | 위반 성분 |")
        print("|------|-------|----|----|----|----|-----------|")
        for v in violations:
            print(
                f"| {v['screen']} | {v['label']} "
                f"| {v['dx']} | {v['dy']} | {v['dw']} | {v['dh']} "
                f"| {', '.join(v['violations'])} |"
            )
    else:
        print("Guard 위반 없음.")
    print()

    # 신뢰도 분포
    grade_criteria = {
        "HIGH": "<=3px",
        "MEDIUM": "<=8px",
        "LOW": "<=15px",
        "CRITICAL": ">15px",
        "N/A": "delta 없음",
    }
    print("### 신뢰도 분포 (전체)")
    print("| 신뢰도 | 기준 | 박스 수 | 비율 |")
    print("|--------|------|---------|------|")
    for grade in ["HIGH", "MEDIUM", "LOW", "CRITICAL", "N/A"]:
        cnt = grades[grade]
        pct = (cnt / total_boxes * 100) if total_boxes else 0
        print(
            f"| {grade} | {grade_criteria[grade]} "
            f"| {cnt} | {pct:.1f}% |"
        )


# ────────────────────────────────────────────────
# JSON 저장
# ────────────────────────────────────────────────


def save_json(result, path):
    now = datetime.now().isoformat()
    output = {
        "generated_at": now,
        "summary": {
            "total_boxes": result["total_boxes"],
            "total_delta_applied": result["total_delta_applied"],
            "total_ocr_recognized": result["total_ocr_recognized"],
            "total_guard_violations": result["total_guard_violations"],
            "screens_count": len(result["screens"]),
        },
        "screens": result["screens"],
        "guard_violations": result["all_violations"],
        "confidence_distribution": result["grade_counts"],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\n[JSON 저장] {path}")


# ────────────────────────────────────────────────
# 진입점
# ────────────────────────────────────────────────


def main():
    save_json_flag = "--json" in sys.argv

    json_paths = sorted(glob.glob(OCR_JSON_GLOB))
    if not json_paths:
        print(
            f"오류: JSON 파일을 찾을 수 없습니다.\n경로: {OCR_JSON_GLOB}",
            file=sys.stderr,
        )
        sys.exit(1)

    result = analyze_files(json_paths)
    print_report(result)

    if save_json_flag:
        save_json(result, OUTPUT_JSON_PATH)


if __name__ == "__main__":
    main()

"""
PRD-0004-EBS-Server-UI-Design.md 구조 재편 스크립트

목표:
- ### 1.1 네비게이션 맵의 각 #### Step X 뒤에
  해당 ## Step 섹션 내용을 인터리브 삽입 (헤딩 레벨 2단계 내림)
- ## Step 1 ~ ## Step 8 h2 섹션 전체 삭제
- 나머지 섹션 (1.2 이후, 변경 이력 등) 보존
"""

import re

INPUT = r"C:\claude\ebs\docs\01_PokerGFX_Analysis\PRD-0004-EBS-Server-UI-Design.md"
OUTPUT = r"C:\claude\ebs\docs\01_PokerGFX_Analysis\PRD-0004-EBS-Server-UI-Design.md.tmp"

with open(INPUT, "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split("\n")

# -----------------------------------------------------------------------
# Step 1: ## Step X 섹션들을 추출하여 딕셔너리에 저장
# 키: Step 번호 문자열 (예: "1", "2", ..., "8")
# 값: 헤딩 조정된 내용 라인 리스트
# -----------------------------------------------------------------------

def adjust_headings(section_lines):
    """
    ## Step X: 화면명 헤딩 자체와 그 바로 아래 blockquote(> 설명)는 제거.
    나머지 헤딩을 2단계 내림:
      ### -> #####
      #### -> ######
      ##### -> #######
    """
    result = []
    skip_blockquote_after_header = True  # 첫 줄(헤딩 자체)은 이미 제거됨

    for line in section_lines:
        # 헤딩 자체(## Step X ...) 는 section_lines에 포함되지 않음 (caller가 제외)
        # 첫 번째 blockquote 라인들 제거
        if skip_blockquote_after_header:
            if line.startswith("> "):
                continue
            elif line.strip() == "":
                # 빈 줄도 스킵 (blockquote 뒤 공백)
                if len(result) == 0:
                    continue
                else:
                    skip_blockquote_after_header = False
                    result.append(line)
            else:
                skip_blockquote_after_header = False
                # 헤딩 조정
                line = _shift_heading(line)
                result.append(line)
        else:
            line = _shift_heading(line)
            result.append(line)

    return result

def _shift_heading(line):
    """헤딩을 2단계 내림 (### -> #####, #### -> ######, ##### -> #######)"""
    # 정확히 #으로 시작하는 헤딩 라인만 처리
    m = re.match(r'^(#{1,6})( .+)$', line)
    if m:
        hashes = m.group(1)
        rest = m.group(2)
        new_hashes = hashes + "##"
        # 최대 7단계
        if len(new_hashes) > 7:
            new_hashes = "#" * 7
        return new_hashes + rest
    return line

# ## Step X 섹션 찾기
# 섹션은 ## Step N: ... 으로 시작하고, 다음 ## Step 또는 ## 로 시작하는 라인까지

step_sections = {}  # step_num -> list of lines (헤딩 제외)

i = 0
section_pattern = re.compile(r'^## Step (\d+):')

# 모든 ## Step X 섹션의 시작 위치 찾기
step_starts = []  # (line_index, step_num)
for idx, line in enumerate(lines):
    m = section_pattern.match(line)
    if m:
        step_starts.append((idx, m.group(1)))

# 각 섹션의 범위 추출
# 끝은 다음 ## Step X 또는 ## (h2 레벨) 또는 파일 끝
# 단, ## Commentary와 ## 10장 등도 h2 섹션이므로 그것도 끝으로 처리

def is_h2_start(line):
    """h2 헤딩 라인 (## 로 시작하지만 ### 가 아닌 것)"""
    return re.match(r'^## [^#]', line) is not None

# 모든 h2 섹션 시작점 (## Step X 포함)
h2_starts = []
for idx, line in enumerate(lines):
    if is_h2_start(line):
        h2_starts.append(idx)

for si, (start_idx, step_num) in enumerate(step_starts):
    # 이 섹션의 끝: 다음 h2 섹션의 시작 - 1
    # 다음 h2 시작점 찾기
    end_idx = len(lines)
    for h2_idx in h2_starts:
        if h2_idx > start_idx:
            end_idx = h2_idx
            break

    # start_idx+1 부터 end_idx-1 까지가 섹션 내용 (헤딩 라인 제외)
    section_body = lines[start_idx + 1: end_idx]
    # 마지막 --- 구분선 제거 (섹션 끝에 있는 ---)
    while section_body and section_body[-1].strip() in ("---", ""):
        section_body.pop()

    adjusted = adjust_headings(section_body)
    step_sections[step_num] = adjusted

print(f"추출된 ## Step 섹션: {list(step_sections.keys())}")

# -----------------------------------------------------------------------
# Step 2: 1.1 섹션 내 각 #### Step X 블록 뒤에 해당 내용 삽입
# -----------------------------------------------------------------------

# 1.1 섹션의 Step 번호 -> ## Step 번호 매핑
# (1.1 순서 기준 → 기존 ## Step)
step_mapping = {
    "1": "1",   # Step 1 (Main Window) -> ## Step 1
    "2": "5",   # Step 2 (Rules) -> ## Step 5
    "3": "6",   # Step 3 (System) -> ## Step 6
    "4": None,  # Step 4 (Action Tracker) -> 별도 섹션 없음
    "5": "4",   # Step 5 (GFX) -> ## Step 4
    "6": "3",   # Step 6 (Outputs) -> ## Step 3
    "7": "2",   # Step 7 (Sources) -> ## Step 2
    "8": "7+8", # Step 8 (Skin Editor + Graphic Editor) -> ## Step 7 + ## Step 8
}

# -----------------------------------------------------------------------
# Step 3: 전체 파일을 재구성
# -----------------------------------------------------------------------

# 전략:
# 1. 1.1 섹션 안에서 #### Step X 블록을 찾아 내용 삽입
# 2. ## Step 1~8 섹션은 완전히 제거
# 3. 나머지는 그대로 유지

# ## Step X 섹션들이 있는 줄 범위를 기록 (제거 대상)
step_section_ranges = set()  # 제거할 줄 인덱스들
for si, (start_idx, step_num) in enumerate(step_starts):
    # 끝은 다음 h2 섹션 바로 전
    end_idx = len(lines)
    for h2_idx in h2_starts:
        if h2_idx > start_idx:
            end_idx = h2_idx
            break
    for idx in range(start_idx, end_idx):
        step_section_ranges.add(idx)

# 1.1 내 #### Step X 패턴
step4_pattern = re.compile(r'^#### Step (\d+):')

# 1.2 섹션이 시작되는 줄 찾기 (1.1 섹션의 끝)
nav_section_end = None
for idx, line in enumerate(lines):
    if re.match(r'^### 1\.2 ', line):
        nav_section_end = idx
        break

print(f"1.2 섹션 시작: 줄 {nav_section_end}")

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]

    # ## Step X 섹션에 속하는 줄 → 스킵
    if i in step_section_ranges:
        i += 1
        continue

    # 1.1 섹션 안에서 #### Step X 블록 처리
    if nav_section_end is not None and i < nav_section_end:
        m = step4_pattern.match(line)
        if m:
            step_num = m.group(1)  # "1" ~ "8"
            # #### Step X 헤딩 라인 그대로 출력
            new_lines.append(line)
            i += 1

            # #### Step X 아래의 기존 내용 (flowchart mermaid 등) 수집 + 출력
            # 다음 #### Step, ### 1.x, ## 가 나올 때까지
            while i < len(lines):
                next_line = lines[i]
                # 1.2 이후면 중단
                if nav_section_end is not None and i >= nav_section_end:
                    break
                # 다음 #### Step X면 중단
                if step4_pattern.match(next_line):
                    break
                # ### 1.x 섹션이면 중단
                if re.match(r'^### 1\.\d', next_line):
                    break
                new_lines.append(next_line)
                i += 1

            # 해당 ## Step 섹션 내용 삽입
            mapped = step_mapping.get(step_num)
            if mapped is None:
                # Action Tracker - 섹션 없음
                pass
            elif mapped == "7+8":
                # Step 7 + Step 8 결합
                content7 = step_sections.get("7", [])
                content8 = step_sections.get("8", [])
                if content7:
                    new_lines.append("")
                    new_lines.extend(content7)
                if content8:
                    new_lines.append("")
                    new_lines.extend(content8)
                if content7 or content8:
                    new_lines.append("")
            else:
                content_to_insert = step_sections.get(mapped, [])
                if content_to_insert:
                    new_lines.append("")
                    new_lines.extend(content_to_insert)
                    new_lines.append("")
            continue
        else:
            new_lines.append(line)
            i += 1
    else:
        new_lines.append(line)
        i += 1

# 연속된 빈 줄 3개 이상을 2개로 압축
final_lines = []
blank_count = 0
for line in new_lines:
    if line.strip() == "":
        blank_count += 1
        if blank_count <= 2:
            final_lines.append(line)
    else:
        blank_count = 0
        final_lines.append(line)

result_content = "\n".join(final_lines)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(result_content)

print(f"\n원본 줄 수: {len(lines)}")
print(f"결과 줄 수: {len(final_lines)}")
print(f"임시 파일: {OUTPUT}")

# 검증
h2_step_count = sum(1 for l in final_lines if re.match(r'^## Step \d+', l))
print(f"\n검증: '## Step N' 패턴 개수 = {h2_step_count} (0이어야 함)")

step4_count = sum(1 for l in final_lines if re.match(r'^#### Step \d+', l))
print(f"검증: '#### Step N' 패턴 개수 = {step4_count} (8이어야 함)")

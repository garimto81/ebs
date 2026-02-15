#!/usr/bin/env python3
"""Detect UI elements from PokerGFX screenshots using Tesseract + OpenCV.

Strategy: Extract precise text positions via Tesseract, detect separator
lines via OpenCV, and combine into UI regions. This replaces Claude Vision's
imprecise coordinate estimation with actual pixel-level data.

Usage:
    python detect_ui_elements.py --target 02           # Text + separator detection
    python detect_ui_elements.py --target 02 --debug   # + debug overlay images
    python detect_ui_elements.py --target 02 --raw     # Raw text positions only
"""
import argparse
import io
import json
import os
import sys
from pathlib import Path

import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageDraw, ImageFont
from pytesseract import Output

# Force UTF-8 output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

INPUT_DIR = "C:/claude/ebs/images/pokerGFX"
OUTPUT_DIR = "C:/claude/ebs/docs/01_PokerGFX_Analysis/02_Annotated_ngd"
DEBUG_DIR = "C:/claude/ebs/tools/debug_output"

IMAGE_MAP = {
    '01': '\uc2a4\ud06c\ub9b0\uc0f7 2026-02-05 180624.png',
    '02': '\uc2a4\ud06c\ub9b0\uc0f7 2026-02-05 180637.png',
    '03': '\uc2a4\ud06c\ub9b0\uc0f7 2026-02-05 180645.png',
    '04': '\uc2a4\ud06c\ub9b0\uc0f7 2026-02-05 180649.png',
    '05': '\uc2a4\ud06c\ub9b0\uc0f7 2026-02-05 180652.png',
    '06': '\uc2a4\ud06c\ub9b0\uc0f7 2026-02-05 180655.png',
    '07': '\uc2a4\ud06c\ub9b0\uc0f7 2026-02-05 180659.png',
    '08': '\uc2a4\ud06c\ub9b0\uc0f7 2026-02-05 180702.png',
    '09': '\uc2a4\ud06c\ub9b0\uc0f7 2026-02-05 180715.png',
    '10': '\uc2a4\ud06c\ub9b0\uc0f7 2026-02-05 180720.png',
    '11': '\uc2a4\ud06c\ub9b0\uc0f7 2026-02-05 180728.png',
}


def load_image(path):
    """Load image with Unicode path support. Returns (PIL Image, OpenCV BGR)."""
    pil_img = Image.open(path).convert('RGB')
    cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    return pil_img, cv_img


def save_image_cv2(cv_img, path):
    """Save OpenCV image with Unicode path support."""
    rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    Image.fromarray(rgb).save(path)


# ============================================================
# STEP 1: Tesseract OCR - extract precise text positions
# ============================================================

def detect_text(cv_img):
    """Extract all text bounding boxes using Tesseract OCR.

    Returns list of dicts: {text, x, y, w, h, conf, level, block_num}
    """
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    data = pytesseract.image_to_data(gray, output_type=Output.DICT)

    results = []
    for i in range(len(data['text'])):
        conf = int(data['conf'][i])
        text = data['text'][i].strip()
        if conf > 30 and text:
            results.append({
                'text': text,
                'x': data['left'][i],
                'y': data['top'][i],
                'w': data['width'][i],
                'h': data['height'][i],
                'conf': conf,
                'level': data['level'][i],
                'block_num': data['block_num'][i],
                'line_num': data['line_num'][i],
            })
    return results


# ============================================================
# STEP 2: OpenCV - detect separator lines
# ============================================================

def detect_h_separators(cv_img, min_length=100):
    """Detect horizontal separator lines using Canny + HoughLinesP.

    Returns sorted list of unique y-coordinates where separators exist.
    """
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=80,
                            minLineLength=min_length, maxLineGap=10)
    if lines is None:
        return []

    h_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if abs(y2 - y1) < 3:  # nearly horizontal
            h_lines.append((y1 + y2) // 2)

    # Deduplicate: merge lines within 3px
    h_lines.sort()
    unique = []
    for y in h_lines:
        if not unique or y - unique[-1] > 3:
            unique.append(y)
    return unique


def detect_v_separators(cv_img, min_length=50):
    """Detect vertical separator lines."""
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=60,
                            minLineLength=min_length, maxLineGap=10)
    if lines is None:
        return []

    v_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if abs(x2 - x1) < 3:  # nearly vertical
            v_lines.append((x1 + x2) // 2)

    v_lines.sort()
    unique = []
    for x in v_lines:
        if not unique or x - unique[-1] > 3:
            unique.append(x)
    return unique


# ============================================================
# STEP 3: OpenCV contours - detect rectangular UI panels
# ============================================================

def detect_contour_rects(cv_img, min_area=2000, min_side=30):
    """Detect rectangular contours (UI panels, buttons).

    Returns list of (x, y, w, h) sorted by area descending.
    """
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 30, 100)

    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=2)

    contours, _ = cv2.findContours(dilated, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    rects = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w * h >= min_area and w >= min_side and h >= min_side:
            rects.append((x, y, w, h))

    # Deduplicate overlapping rects (keep larger)
    rects.sort(key=lambda r: r[2] * r[3], reverse=True)
    unique = []
    for rect in rects:
        rx, ry, rw, rh = rect
        is_dup = False
        for ux, uy, uw, uh in unique:
            # Check significant overlap
            ox = max(0, min(rx + rw, ux + uw) - max(rx, ux))
            oy = max(0, min(ry + rh, uy + uh) - max(ry, uy))
            overlap = ox * oy
            if overlap > 0.7 * min(rw * rh, uw * uh):
                is_dup = True
                break
        if not is_dup:
            unique.append(rect)

    return unique


# ============================================================
# VISUALIZATION & OUTPUT
# ============================================================

def draw_debug_overlay(pil_img, texts, h_seps, v_seps, contours):
    """Draw comprehensive debug overlay on PIL image."""
    draw = ImageDraw.Draw(pil_img, 'RGBA')

    try:
        font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 10)
    except Exception:
        font = ImageFont.load_default()

    # Draw horizontal separators (cyan)
    for y in h_seps:
        draw.line([(0, y), (pil_img.width, y)], fill=(0, 255, 255, 120), width=1)

    # Draw vertical separators (yellow)
    for x in v_seps:
        draw.line([(x, 0), (x, pil_img.height)], fill=(255, 255, 0, 80), width=1)

    # Draw contour rects (blue, semi-transparent)
    for x, y, w, h in contours:
        draw.rectangle([x, y, x + w, y + h], outline=(0, 100, 255, 200), width=2)

    # Draw text boxes (green)
    for t in texts:
        x, y, w, h = t['x'], t['y'], t['w'], t['h']
        conf = t['conf']
        color = (0, 200, 0, 180) if conf > 60 else (200, 200, 0, 150)
        draw.rectangle([x, y, x + w, y + h], outline=color, width=1)
        draw.text((x, y - 10), f"{t['text']} ({conf}%)", fill=color, font=font)

    return pil_img


def print_text_report(texts, h_seps, v_seps, img_shape):
    """Print structured text detection report."""
    h, w = img_shape[:2]
    print(f"\n{'='*70}")
    print(f"  TEXT DETECTION REPORT  ({w}x{h})")
    print(f"{'='*70}")

    # Sort by y then x
    sorted_texts = sorted(texts, key=lambda t: (t['y'], t['x']))

    print(f"\n  Detected {len(sorted_texts)} text elements:")
    print(f"  {'Text':<35} {'Position':<25} {'Conf':>5}")
    print(f"  {'-'*35} {'-'*25} {'-'*5}")

    for t in sorted_texts:
        pos = f"({t['x']:>3},{t['y']:>3}) {t['w']:>3}x{t['h']:<3}"
        text = t['text'][:35]
        print(f"  {text:<35} {pos:<25} {t['conf']:>3}%")

    print(f"\n  Horizontal separators ({len(h_seps)}):")
    for y in h_seps:
        print(f"    y={y}")

    print(f"\n  Vertical separators ({len(v_seps)}):")
    for x in v_seps:
        print(f"    x={x}")


def print_anchor_map(texts, target_key):
    """Print text positions as anchor points for generate_annotations.py.

    Groups known PokerGFX UI labels to their detected positions.
    """
    print(f"\n{'='*70}")
    print(f"  ANCHOR MAP for {target_key}")
    print(f"{'='*70}")

    # Known UI labels per image target
    # Keywords are used to match Tesseract-detected text to UI regions
    known_labels = {
        '01': {
            '1: Title Bar': ['PokerGFX', 'Server', 'Table'],
            '2: Preview': ['Preview'],
            '3: CPU/GPU': ['CPU', 'GPU'],
            '4: Record/Error': ['Record', 'Error', 'Lock'],
            '5: Secure Delay': ['Secure', 'Delay'],
            '6: Reset Hand': ['Reset', 'Hand', 'Settings'],
            '7: Register Deck': ['Register', 'Deck'],
            '8: Action Tracker': ['Launch', 'Action', 'Tracker'],
            '9: Studio': ['Studio'],
            '10: Split Recording': ['Split', 'Recording'],
            '11: Tag Player': ['Tag', 'Player'],
        },
        '02': {
            '1: Tab Bar': ['Sources', 'Outputs', 'GFX'],
            '2: Device Table': ['Device', 'Format', 'Action', 'Cycle', 'Status'],
            '3: Board Cam': ['Board', 'Cam', 'Hide', 'GFX', 'Auto', 'Camera'],
            '4: Mode': ['Mode', 'Static'],
            '5: Split/Follow': ['Heads', 'Split', 'Screen', 'Follow', 'Players', 'Board'],
            '6: Linger/Post': ['Linger', 'Post', 'Bet', 'Hand'],
            '7: Chroma Key': ['Background', 'key', 'colour', 'Chroma', 'Key'],
            '8: Network Cam': ['Add', 'Network', 'Camera'],
            '9: Audio': ['Audio', 'Sync', 'Level', 'Input'],
            '10: Switcher': ['External', 'Switcher', 'Source', 'ATEM', 'Control'],
            '11: Board Sync': ['Crossfade'],
            '12: Player View': ['Player', 'View'],
        },
        '03': {
            '1: Video Size': ['Video', 'Size', 'Resolution'],
            '2: Vertical': ['Vertical', '9x16', '16:9'],
            '3: Frame Rate': ['Frame', 'Rate', 'fps'],
            '4: Live Output': ['Live', 'NDI', 'Output'],
            '5: Delay Output': ['Delay', 'Output'],
            '6: Virtual Camera': ['Virtual', 'Camera'],
            '7: Recording Mode': ['Recording', 'Mode', 'Record'],
            '8: Secure Delay': ['Secure', 'Delay'],
            '9: Dynamic Delay': ['Dynamic'],
            '10: Auto Stream': ['Auto', 'Stream'],
            '11: Countdown': ['Countdown', 'Show'],
            '12: Countdown Video': ['Browse', 'Video'],
            '13: Twitch/ChatBot': ['Twitch', 'Chat', 'Bot'],
        },
        '04': {
            '1: Board Position': ['Board', 'Position', 'Layout'],
            '2: Reveal/Fold': ['Reveal', 'Fold', 'Cards', 'Card'],
            '3: Leaderboard Pos': ['Leaderboard', 'Position'],
            '4: Transition': ['Transition', 'In', 'Out'],
            '5: Heads Up': ['Heads', 'Up', 'Camera'],
            '6: Skin Name': ['Skin', 'Name', 'Editor'],
            '7: Sponsor Logo': ['Sponsor', 'Logo'],
            '8: Vanity': ['Vanity'],
            '9: Margins': ['Margin', 'Top', 'Bottom'],
            '10: Indent/Bounce': ['Indent', 'Bounce', 'Action'],
            '11: Show Hand': ['Show', 'Hand', 'Each'],
            '12: Action Clock': ['Action', 'Clock'],
        },
        '05': {
            '1: Leaderboard': ['Leaderboard', 'Show', 'Name', 'Stack'],
            '2: Game Rules': ['Bomb', 'Pot', 'Straddle', 'Ante'],
            '3: Seat/Eliminated': ['Seat', 'Eliminated', 'Open'],
            '4: Rabbit Hunting': ['Rabbit', 'Hunting', 'Blink'],
            '5: Hilite Nit': ['Hilite', 'Nit', 'Clear'],
            '6: Order/Equities': ['Order', 'Equities', 'Equity'],
            '7: Equity Outs': ['Outs', 'Split', 'Pot'],
        },
        '06': {
            '1: Outs': ['Outs', 'Out'],
            '2: Score Strip': ['Score', 'Strip'],
            '3: Blinds': ['Blinds', 'Blind', 'Level'],
            '4: Currency': ['Currency', 'Symbol', 'Dollar'],
            '5: Chipcount': ['Chipcount', 'Precision', 'Round'],
            '6: Display': ['Display', 'Amounts', 'Mode'],
        },
        '07': {
            '1: Commentary': ['Commentary', 'Mode', 'Password'],
            '2: Statistics': ['Statistics', 'Only'],
            '3: Leaderboard': ['Control', 'Leaderboard'],
            '4: Camera PIP': ['Camera', 'PIP'],
            '5: Full Screen': ['Full', 'Screen'],
            '6: Reserved': [],
        },
        '08': {
            '1: Table Name': ['Table', 'Name', 'Password'],
            '2: Reset/Calibrate': ['Reset', 'Calibrate'],
            '3: License/Serial': ['License', 'Serial', 'Key'],
            '4: Updates/PRO': ['Update', 'PRO', 'Version'],
            '5: MultiGFX': ['MultiGFX', 'Sync', 'Multi'],
            '6: GPU Encode': ['GPU', 'Encode', 'Tags'],
            '7: RFID Antenna': ['RFID', 'Antenna', 'Reader'],
            '8: Action Tracker': ['Action', 'Tracker'],
            '9: System Info': ['System', 'Info', 'Memory'],
            '10: Diagnostics': ['Diagnostic', 'Log'],
            '11: Delay/Export': ['Export', 'Folder'],
            '12: Stream Deck': ['Stream', 'Deck'],
        },
        '09': {
            '1: Name/Details': ['Name', 'Details', 'Skin'],
            '2: 4K/Transparency': ['4K', 'Transparency', 'UHD'],
            '3: Adjustments': ['Adjust', 'Size', 'Offset', 'Scale'],
            '4: Elements': ['Element', 'Board', 'Player', 'Photo'],
            '5: Text/Font': ['Text', 'Font', 'Caps', 'Speed'],
            '6: Cards': ['Card', 'Cards', 'Deck'],
            '7: Flags': ['Flag', 'Flags', 'Country'],
            '8: Player Variant': ['Player', 'Variant', 'Set'],
            '9: Bottom Buttons': ['OK', 'Cancel', 'Save', 'Apply'],
        },
        '10': {
            '1: Layout Size': ['Layout', 'Size', '296'],
            '2: Import Image': ['Import', 'Image', 'Mode'],
            '3: Animation': ['Animation', 'Speed'],
            '4: Transition': ['Transition', 'In', 'Out'],
            '5: Element/Position': ['Element', 'Position', 'Anchor'],
            '6: Text/Font': ['Text', 'Font', 'Alignment', 'Shadow'],
            '7: Colour/Hilite': ['Colour', 'Color', 'Hilite'],
            '8: Background': ['Background', 'Image'],
            '9: Adjust/OK': ['Adjust', 'Colours', 'OK', 'Cancel'],
            '10: Live Preview': ['Preview', 'Live'],
        },
        '11': {
            '1: Title Bar': ['Graphic', 'Editor', 'Player'],
            '2: Element/Import': ['Element', 'Import', 'Mode'],
            '3: Settings': ['Animation', 'Text', 'Font', 'Position'],
            'A: Photo': ['Photo'],
            'B: Hole Cards': ['Card', 'Hole'],
            'C: Name': ['Name'],
            'D: Flag': ['Flag', 'Country'],
            'E: Equity': ['Equity'],
            'F: Action': ['Action'],
            'G: Stack': ['Stack', 'Chip'],
            'H: Position': ['POS', 'Dealer'],
        },
    }

    labels = known_labels.get(target_key, {})
    if not labels:
        print("  No known labels for this target.")
        return

    for box_name, keywords in labels.items():
        matches = []
        for t in texts:
            if any(kw.lower() in t['text'].lower() for kw in keywords):
                matches.append(t)

        if matches:
            min_x = min(m['x'] for m in matches)
            min_y = min(m['y'] for m in matches)
            max_x = max(m['x'] + m['w'] for m in matches)
            max_y = max(m['y'] + m['h'] for m in matches)

            print(f"\n  {box_name}:")
            print(f"    Bounding: ({min_x}, {min_y}) to ({max_x}, {max_y})")
            print(f"    Rect: ({min_x}, {min_y}, {max_x - min_x}, {max_y - min_y})")
            for m in sorted(matches, key=lambda t: (t['y'], t['x'])):
                print(f"      '{m['text']}' at ({m['x']},{m['y']}) {m['w']}x{m['h']} [{m['conf']}%]")
        else:
            print(f"\n  {box_name}:")
            print(f"    ** NO MATCHES ** (keywords: {keywords})")

    print(f"\n{'='*70}")


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='Detect UI elements via Tesseract + OpenCV')
    parser.add_argument('--input', default=None, help='Input image path')
    parser.add_argument('--target', default='02', help='Target image (01-11)')
    parser.add_argument('--debug', action='store_true', help='Save debug overlay images')
    parser.add_argument('--raw', action='store_true', help='Raw text positions only')
    args = parser.parse_args()

    # Resolve path
    if args.input:
        img_path = args.input
    else:
        if args.target not in IMAGE_MAP:
            print(f"Error: target '{args.target}' not in {list(IMAGE_MAP.keys())}")
            return 1
        img_path = f"{INPUT_DIR}/{IMAGE_MAP[args.target]}"

    if not os.path.exists(img_path):
        print(f"Error: not found: {img_path}")
        return 1

    # Load
    print(f"Loading: {os.path.basename(img_path)}")
    pil_img, cv_img = load_image(img_path)
    h, w = cv_img.shape[:2]
    print(f"Size: {w}x{h}")

    # Step 1: Tesseract text detection
    print("\nStep 1: Tesseract OCR...")
    texts = detect_text(cv_img)
    print(f"  {len(texts)} text elements detected")

    if args.raw:
        print_text_report(texts, [], [], cv_img.shape)
        return 0

    # Step 2: Separator lines
    print("Step 2: Separator lines...")
    h_seps = detect_h_separators(cv_img)
    v_seps = detect_v_separators(cv_img)
    print(f"  {len(h_seps)} horizontal, {len(v_seps)} vertical")

    # Step 3: Contour rects
    print("Step 3: Contour rectangles...")
    contours = detect_contour_rects(cv_img)
    print(f"  {len(contours)} rectangles")

    # Output
    print_text_report(texts, h_seps, v_seps, cv_img.shape)
    print_anchor_map(texts, args.target)

    # Debug overlay
    if args.debug:
        os.makedirs(DEBUG_DIR, exist_ok=True)

        # Full debug overlay
        debug_img = pil_img.copy()
        debug_img = draw_debug_overlay(debug_img, texts, h_seps, v_seps, contours)
        debug_path = f"{DEBUG_DIR}/debug-{args.target}.png"
        debug_img.save(debug_path)
        print(f"\nDebug overlay: {debug_path}")

        # Text-only overlay
        text_img = pil_img.copy()
        text_draw = ImageDraw.Draw(text_img)
        for t in texts:
            x, y, tw, th = t['x'], t['y'], t['w'], t['h']
            text_draw.rectangle([x, y, x + tw, y + th], outline='lime', width=1)
        text_path = f"{DEBUG_DIR}/text-only-{args.target}.png"
        text_img.save(text_path)
        print(f"Text overlay:  {text_path}")

    # JSON export
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    json_path = f"{OUTPUT_DIR}/{args.target}-detected.json"
    data = {
        'image': os.path.basename(img_path),
        'size': [int(w), int(h)],
        'texts': [{'text': t['text'], 'x': int(t['x']), 'y': int(t['y']),
                    'w': int(t['w']), 'h': int(t['h']), 'conf': int(t['conf'])}
                   for t in texts],
        'h_separators': [int(s) for s in h_seps],
        'v_separators': [int(s) for s in v_seps],
        'contour_rects': [{'x': int(r[0]), 'y': int(r[1]), 'w': int(r[2]), 'h': int(r[3])}
                          for r in contours],
    }
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\nJSON: {json_path}")

    print("\nDone.")
    return 0


if __name__ == '__main__':
    exit(main())

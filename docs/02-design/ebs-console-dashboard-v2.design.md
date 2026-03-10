---
doc_type: "design"
doc_id: "EBS-Console-Dashboard-v2"
version: "2.0.0"
status: "draft"
last_updated: "2026-03-04"
parent_doc: "ebs-console.prd.md"
related_docs:
  - "EBS-UI-Design-v3.prd.md"
  - "ebs-console-ui.design.md"
  - "ebs-console-feature-triage.md"
---

# EBS Console Dashboard v2.0 — Flutter + Rive 설계서

> **패러다임 전환**: React/Electron(v1.0) → Flutter Desktop + Rive(v2.0)

## 1장. Design Philosophy

### "Linear-meets-broadcast" 5대 원칙

EBS Console은 방송 프로덕션 환경에서 운영자가 **최소 인터랙션으로 최대 정보를 소비**하는 도구다. 아래 5가지 원칙이 모든 설계 결정의 기준이 된다.

| # | 원칙 | 설명 | 구현 |
|---|------|------|------|
| 1 | **Keyboard First** | 마우스 의존 최소화, 키보드로 전체 워크플로우 완결 | Ctrl+1~5 탭 전환, Tab 포커스 순회 |
| 2 | **Monochrome + Status Color** | Zinc 그레이스케일 베이스, 상태 변화만 컬러로 표현 | 7색 RFID 체계, CPU/GPU 3단계 인디케이터 |
| 3 | **8px Grid** | 모든 간격과 크기는 8의 배수 | `EdgeInsets.all(8)`, `SizedBox(height: 16)`, 4px는 인라인 전용 |
| 4 | **Information Density > Decoration** | 방송 제어는 정보 밀도가 핵심, 장식 요소 최소화 | elevation: 0, 투명 보더, 컴팩트 라벨 |
| 5 | **GPU-Accelerated Native** | 60fps 보장, 네이티브 성능 우선 | Flutter Impeller 렌더러, Rive C++ 런타임 |

### v1.0 → v2.0 패러다임 전환 근거

v1.0(React/Electron)에서 v2.0(Flutter Desktop)으로 전환한 핵심 이유는 **Rive 네이티브 통합**이다. 웹 기반 아키텍처에서는 NodeCG iframe 임베드가 필수였으나, Flutter Desktop은 Rive C++ 런타임을 위젯으로 직접 임베드한다.

| 항목 | v1.0 (React 기반) | v2.0 (Flutter + Rive) |
|------|-------------------|----------------------|
| 프레임워크 | Electron + React 19 | Flutter Desktop |
| UI 라이브러리 | shadcn/ui (React) | shadcn_flutter (84 컴포넌트) |
| 컬러 | Slate (#0F172A) | Zinc (#09090b) via `ColorScheme.dark()` 수동 오버라이드 |
| 타이포그래피 | CSS 시스템 폰트 | Geist Sans/Mono via `google_fonts` |
| 레이아웃 | 고정 2컬럼 | `panes` 패키지 IDE 스타일 리사이즈 |
| 내비게이션 | 수평 탭 바 | `NavigationRail` 수직 사이드바 (48px↔200px) |
| 상태관리 | Zustand + persist | Riverpod 3.0 (auto-retry, offline persist) |
| 상태 표시 | 프로그레스 바 | 컬러 도트 `Container(decoration: BoxDecoration)` |
| 오버레이 프리뷰 | NodeCG iframe | `RiveAnimation` widget 직접 임베드 |
| 보더 | 솔리드 그레이 | 투명 보더 `Colors.white.withOpacity(0.10)` |
| 검증 | Zod 스키마 | Dart 타입 시스템 + 폼 유효성 검사 |

전환의 핵심 성능 이점:
- Rive 네이티브 C++ 통합 (웹 WASM 대비 2~3x 성능)
- 단일 코드베이스로 Windows/macOS/Linux 지원
- Impeller 렌더러로 GPU 가속 UI 렌더링
- NodeCG iframe 임베드 불필요 → Rive 위젯 직접 임베드

> **PRD 충돌 고지**: `EBS-UI-Design-v3.prd.md`(v1.0.0)는 Electron + React를 "채택"으로 결정하고
> Flutter Desktop을 "탈락"으로 명시했다. 그러나 프로젝트 아키텍처(`CLAUDE.md`)에서 Frontend는
> Flutter + Rive로 확정되었으며, 본 설계서는 이 아키텍처 결정을 따른다.
> PRD v2.0의 기술 스택 섹션은 향후 v2.0.0으로 업데이트가 필요하다.

## 2장. Technology Stack

### 핵심 패키지

| Layer | Package | Version | 역할 |
|-------|---------|---------|------|
| UI 프레임워크 | `shadcn_flutter` | 0.0.52 | 84개 컴포넌트, 다크 테마, Material 독립 |
| 레이아웃 | `panes` | 1.1.1 | IDE 스타일 리사이즈 패널, 비율 상태 유지 |
| 내비게이션 | `NavigationRail` | Flutter SDK | 사이드바 확장/축소 (48px↔200px) |
| 애니메이션 | `rive` | 0.14.4 | 네이티브 C++ 런타임, 오버레이 + UI 위젯 |
| 상태관리 | `flutter_riverpod` | 3.x | Mutations, auto-retry, pause/resume |
| WebSocket | `web_socket_channel` | ^2.3.0 | 실시간 게임 상태 스트림 |
| 차트 | `fl_chart` | latest | 모니터링 대시보드 |
| 타이포그래피 | `google_fonts` | ^6.2.1 | Geist Sans/Mono |
| 데이터 테이블 | `DataTable` | Flutter SDK | 소스 관리 테이블 |

### Riverpod 3.0 WebSocket 패턴

```dart
@riverpod
Stream<GameState> gameStateStream(Ref ref) async* {
  final channel = WebSocketChannel.connect(
    Uri.parse('ws://localhost:8080/ws'),
  );
  await for (final message in channel.stream) {
    yield GameState.fromJson(jsonDecode(message as String));
  }
}
```

auto-retry 지수 백오프: `1s → 2s → 4s → 8s → 16s max`

### UI 프레임워크 선택 근거

| 후보 | 평가 | 결과 |
|------|------|------|
| **shadcn_flutter** | 84개 컴포넌트, 다크 테마 네이티브, Material 독립 | **채택** |
| fluent_ui | Windows 전용 미학, macOS에서 이질감 | 탈락 |
| Material 3 | 모바일 중심 디자인 언어, 데스크톱 밀도 부족 | 탈락 |

shadcn_flutter는 shadcn/ui(React)의 Flutter 포트로, v1.0에서 사용하던 컴포넌트 체계를 그대로 계승하면서 네이티브 성능을 확보한다.

## 3장. Design System

### 3.1 Color

Zinc 팔레트 기반 `ColorScheme.dark()` 수동 오버라이드. Material 3 기본 블루 틴트를 완전히 제거한다.

```dart
final ebsColorScheme = ColorScheme.dark(
  surface: const Color(0xFF09090B),                    // zinc-950: 앱 배경
  surfaceContainerLowest: const Color(0xFF18181B),     // zinc-900: Surface-1 (패널)
  surfaceContainer: const Color(0xFF27272A),           // zinc-800: Surface-2 (카드)
  surfaceContainerHighest: const Color(0xFF3F3F46),    // zinc-700: Surface-3 (호버)
  primary: const Color(0xFFFAFAFA),                    // zinc-50: 프라이머리 텍스트
  onSurface: const Color(0xFFA1A1AA),                  // zinc-400: 세컨더리 텍스트
  outline: Colors.white.withOpacity(0.10),             // 투명 보더
  surfaceTint: Colors.transparent,                     // Material 3 블루 틴트 제거
);
```

**상태 컬러** (상수 정의):

```dart
class EbsColors {
  static const red500    = Color(0xFFEF4444);  // 에러, RFID 미연결
  static const green500  = Color(0xFF22C55E);  // 정상, 연결됨
  static const blue500   = Color(0xFF3B82F6);  // 정보, 미등록 카드
  static const amber500  = Color(0xFFF59E0B);  // 경고, CPU/GPU 중간
  static const orange500 = Color(0xFFF97316);  // RFID 응답 없음
  static const zinc500   = Color(0xFF71717A);  // 비활성, 중립
  static const magenta   = Color(0xFFD946EF);  // RFID 중복 카드
}
```

**RFID 7색 체계** (v1.0 계승):

| 색상 | Hex | 의미 |
|------|-----|------|
| Green | `#22C55E` | 정상 운용 |
| Grey | `#71717A` | 보안 링크 수립 중 |
| Blue | `#3B82F6` | 미등록 카드 감지 |
| Black | `#18181B` | 동일 카드 중복 |
| Magenta | `#D946EF` | 중복 카드 |
| Orange | `#F97316` | 응답 없음 |
| Red | `#EF4444` | 미연결 |

> **v1.0 대비 hex 변경**: Grey `#94A3B8`(Slate) → `#71717A`(Zinc), Black `#1E293B`(Slate) → `#18181B`(Zinc).
> Zinc 팔레트 통일을 위한 변경이며, 색상의 의미와 시각적 구분은 동일하게 유지된다.

**CPU/GPU 인디케이터** (v1.0 계승):

| 색상 | 조건 |
|------|------|
| Green `#22C55E` | <60% |
| Amber `#F59E0B` | <85% |
| Red `#EF4444` | ≥85% |

### 3.2 Typography

Geist Sans(UI) + Geist Mono(데이터) 이중 서체 체계:

```dart
final ebsTextTheme = TextTheme(
  labelSmall:  GoogleFonts.geistSans(fontSize: 11),  // 보조 라벨
  bodySmall:   GoogleFonts.geistSans(fontSize: 12),  // Status Bar
  bodyMedium:  GoogleFonts.geistSans(fontSize: 13),  // 기본 본문
  bodyLarge:   GoogleFonts.geistSans(fontSize: 14),  // 폼 필드
  titleSmall:  GoogleFonts.geistSans(fontSize: 16),  // 섹션 제목
  titleMedium: GoogleFonts.geistSans(fontSize: 18),  // 탭 제목
  titleLarge:  GoogleFonts.geistSans(fontSize: 24),  // 페이지 제목
);
```

- 데이터 표시 (수치, 코드, 타이머): `GoogleFonts.geistMono()`
- textScaler 고정: `MediaQuery(data: MediaQueryData(textScaler: TextScaler.linear(1.0)), child: app)` — 데스크톱 환경에서 OS 스케일링 무시

### 3.3 Spacing

8px 기본 단위. 4px는 인라인 간격 전용 예외:

```dart
class EbsSpacing {
  static const xs  = 4.0;   // 인라인 간격 (아이콘-텍스트)
  static const sm  = 8.0;   // 기본 간격
  static const md  = 16.0;  // 섹션 간격
  static const lg  = 24.0;  // 영역 간격
  static const xl  = 32.0;  // 페이지 여백
}
```

### 3.4 Icons

Flutter Material Icons 기본 사용. 부족한 아이콘은 `lucide_icons` 패키지로 보충.

| 사용처 | 크기 |
|--------|------|
| Status Bar | 16px |
| NavigationRail | 20px |
| 액션 버튼 | 24px |

### 3.5 Elevation

`elevation: 0` 원칙. Surface 구분은 배경색 + 투명 보더로 처리:

```dart
Container(
  decoration: BoxDecoration(
    color: ebsColorScheme.surfaceContainerLowest,
    border: Border.all(color: Colors.white.withOpacity(0.10)),
    borderRadius: BorderRadius.circular(8),
  ),
)
```

그림자 대신 `surfaceContainerLowest → surfaceContainer → surfaceContainerHighest` 계층으로 깊이를 표현한다.

## 4장. Layout Architecture

### 4.1 Main Window

`panes` 패키지 기반 3영역 구조:

```
  +------------------------------------------------------+
  | [EBS] v1.0    DELAYED 00:28    CPU GPU RFID  [- X]  |
  +----+------------------------------+------------------+
  | N  |                              |                  |
  | A  |    Preview Panel             | Property Panel   |
  | V  |    (Rive overlay preview)    | (context-        |
  |    |    16:9 chroma key blue      |  sensitive)      |
  | R  |                              |                  |
  | A  +------------------------------+------------------+
  | I  |                                                 |
  | L  |  Tab Content Area                               |
  |    |  (scrollable SingleChildScrollView)              |
  |    |                                                 |
  +----+-------------------------------------------------+
  | Status: Connected | Hold'em | 50K/100K | Hand #47    |
  +------------------------------------------------------+
```

Scaffold 구조:

```dart
Scaffold(
  appBar: PreferredSize(
    preferredSize: Size.fromHeight(36),
    child: EbsTitleBar(),
  ),
  body: Row(
    children: [
      EbsNavigationRail(),         // 48px or 200px
      Expanded(
        child: Panes(
          children: [
            PaneChild(child: Column(
              children: [
                Expanded(child: Row(
                  children: [
                    Expanded(flex: 6, child: EbsPreviewPanel()),
                    Expanded(flex: 4, child: EbsPropertyPanel()),
                  ],
                )),
                Expanded(child: EbsTabContent()),
              ],
            )),
          ],
        ),
      ),
    ],
  ),
  bottomNavigationBar: EbsStatusBar(),
)
```

**앱 윈도우 크기 정책**:
- 최소: 1280x720
- Preview(좌):Control(우) 기본 비율 = 6:4
- `panes` 패키지로 사용자 리사이즈 가능, 비율 `SharedPreferences` 저장

### 4.2 NavigationRail Sidebar

```dart
NavigationRail(
  extended: isExpanded,  // 48px ↔ 200px 토글
  destinations: [
    NavigationRailDestination(
      icon: Icon(Icons.input), label: Text('I/O'),
    ),
    NavigationRailDestination(
      icon: Icon(Icons.brush), label: Text('GFX'),
    ),
    NavigationRailDestination(
      icon: Icon(Icons.gavel), label: Text('Rules'),
    ),
    NavigationRailDestination(
      icon: Icon(Icons.tv), label: Text('Display'),
    ),
    NavigationRailDestination(
      icon: Icon(Icons.settings), label: Text('System'),
    ),
  ],
  selectedIndex: currentTab,
  onDestinationSelected: (index) =>
    ref.read(currentTabProvider.notifier).state = index,
)
```

**단축키**: Ctrl+1(I/O), Ctrl+2(GFX), Ctrl+3(Rules), Ctrl+4(Display), Ctrl+5(System)

구현: `Shortcuts` + `Actions` 위젯으로 글로벌 키바인딩 등록.

### 4.3 Resizable Panes

`panes` 패키지로 Preview/Controls 영역 리사이즈:

| 속성 | 값 |
|------|-----|
| 드래그 핸들 | 4px 투명 영역, 호버 시 zinc-500 하이라이트 |
| 비율 persist | `SharedPreferences`에 `double` 저장 |
| Preview 최소 너비 | 320px |
| Controls 최소 너비 | 280px |

## 5장. Title Bar & Status Bar

### 5.1 Custom Title Bar

36px 높이의 커스텀 AppBar. 로고, 버전, Delayed 인디케이터, 시스템 상태 도트, 윈도우 컨트롤을 배치한다.

```dart
AppBar(
  toolbarHeight: 36,
  leading: Row(children: [
    const SizedBox(width: 12),
    Text('EBS', style: GoogleFonts.geistSans(
      fontSize: 14, fontWeight: FontWeight.w700,
    )),
    const SizedBox(width: 8),
    Text('v1.0', style: TextStyle(
      fontSize: 11, color: EbsColors.zinc500,
    )),
  ]),
  title: _buildDelayIndicator(),  // Delayed 모드 시 표시
  actions: [
    _StatusDot(color: cpuColor, tooltip: 'CPU 42%'),   // M-03
    _StatusDot(color: gpuColor, tooltip: 'GPU 28%'),   // M-04
    _StatusDot(color: rfidColor, tooltip: 'RFID 정상'), // M-05
    const SizedBox(width: 8),
    IconButton(icon: Icon(Icons.minimize), onPressed: minimize),
    IconButton(icon: Icon(Icons.close), onPressed: close),
  ],
)
```

**\_StatusDot 위젯**: 8x8 원형 컨테이너로 시스템 상태를 표현한다.

```dart
Container(
  width: 8, height: 8,
  decoration: BoxDecoration(
    shape: BoxShape.circle,
    color: statusColor,
  ),
)
```

**Delayed 모드 표시**: Amber 컬러 텍스트 `DELAYED MM:SS` 형식. `StreamBuilder`로 매초 갱신한다. 정상 모드에서는 비표시.

**v1.0 요소 매핑**:

| 요소 ID | 위젯 | 설명 |
|---------|------|------|
| M-01 | `Text('EBS')` | 앱 타이틀 |
| M-03 | `_StatusDot` | CPU 사용률 |
| M-04 | `_StatusDot` | GPU 사용률 |
| M-05 | `_StatusDot` | RFID 상태 |
| M-06 | `Icon` | 연결 상태 아이콘 |

### 5.2 Status Bar

28px 높이의 BottomAppBar. 연결 상태, 게임 정보, 키보드 힌트를 표시한다.

```dart
BottomAppBar(
  height: 28,
  child: Row(children: [
    _ConnectionDot(status: engineStatus),    // Engine
    _ConnectionDot(status: nodecgStatus),    // NodeCG
    _ConnectionDot(status: casparcgStatus),  // CasparCG
    _ConnectionDot(status: atStatus),        // AT
    const VerticalDivider(),
    Text('Hold\'em', style: bodySmall),
    Text('50K/100K', style: geistMono),
    Text('Hand #47', style: geistMono),
    const Spacer(),
    Text('Ctrl+K: Command', style: labelSmall.copyWith(
      color: EbsColors.zinc500,
    )),
  ]),
)
```

**\_ConnectionDot**: `_StatusDot`와 동일한 8px 원형 도트. 각 서비스 연결 상태를 Green(연결)/Red(미연결)로 표시한다. 마우스 호버 시 `Tooltip`으로 서비스명과 URL을 표시.

**v1.0 요소 매핑**:

| 요소 ID | 위젯 | 설명 |
|---------|------|------|
| M-09 | `BottomAppBar` | Status Bar 전체 |
| M-10 | `_ConnectionDot` x4 | 4개 서비스 연결 상태 |

## 6장. 5-Tab Dashboard Design

> **요소 ID 재설계 고지**: v2.0은 v1.0의 접두사 체계(M/S/O/G/Y)는 계승하되,
> **기능 번호를 전면 재할당**했다. v1.0의 G-10(Sponsor Logo 1)과 v2.0의 G-10(Stack Display)은
> 동일 ID이지만 다른 기능이다. v1.0→v2.0 매핑은 아래 원칙을 따른다:
> - 접두사 의미 유지: M=Main Window, S=Sources, O=Outputs, G=GFX/Rules/Display, Y=System
> - 번호는 v2.0 탭 내 논리적 순서로 재할당 (v1.0 번호와 1:1 대응하지 않음)
> - v1.0과의 정확한 대응이 필요하면 `ebs-console-ui.design.md`의 원본 ID를 참조

5개 탭은 `NavigationRail`의 `selectedIndex`에 따라 Tab Content Area에 렌더링된다. 각 탭은 `SingleChildScrollView`로 감싸 오버플로우를 방지한다.

### 6.1 I/O (Sources + Outputs)

20개 요소. Sources(S-01~S-12)와 Outputs(O-01~O-08)를 상하 분할 배치한다.

**Sources (S-01~S-12)**: `DataTable` 기반 30행 테이블. 각 행은 inline 편집을 지원한다.

| 컬럼 | 위젯 | 설명 |
|------|------|------|
| # | `Text` | 소스 번호 (읽기 전용) |
| Name | `TextFormField` | 소스 이름 (inline edit) |
| Type | `DropdownButton` | NDI / Capture / File |
| Status | `_StatusDot` | 연결 상태 (읽기 전용) |
| Actions | `Switch` | 활성/비활성 토글 |

**Outputs (O-01~O-08)**: 출력 설정 폼 영역.

| 요소 ID | 위젯 | 설명 |
|---------|------|------|
| O-01 | `DropdownButton` | Video Size (720p / 1080p / 4K) |
| O-02 | `DropdownButton` | Frame Rate (30 / 60 fps) |
| O-03 | `Switch` | Chroma Key Enable |
| O-04 | `ColorPicker` | Chroma Key Color (`#0000FF` 기본) |
| O-05 | `Switch` | Fill & Key NDI Output |
| O-06 | `Switch` | 9x16 Vertical Mode |
| O-07 | `DropdownButton` | Output Format (NDI / SDI) |
| O-08 | `Switch` | Recording |

### 6.2 GFX

19개 요소. `ExpansionTile` 4그룹으로 구성한다.

**Layout (G-01~G-06)**:

| 요소 ID | 위젯 | 설명 |
|---------|------|------|
| G-01 | `SegmentedButton` | Board Position (Top / Center / Bottom) |
| G-02 | `DropdownButton` | Player Count (2 / 6 / 8 / 9 / 10) |
| G-03 | `Slider` | Board Margin Top % (0~100) |
| G-04 | `Slider` | Board Margin Left % (0~100) |
| G-05 | `Slider` | Board Margin Right % (0~100) |
| G-06 | `DropdownButton` | Graphics Size (S / M / L / XL) |

**Card & Player (G-07~G-10)**:

| 요소 ID | 위젯 | 설명 |
|---------|------|------|
| G-07 | `SegmentedButton` | Card Reveal (Instant / Flip / Slide) |
| G-08 | `Switch` + `FilePickerButton` | Player Photo 활성화 + 파일 선택 |
| G-09 | `Switch` | National Flag 표시 |
| G-10 | `SegmentedButton` | Stack Display (Chips / BB / Both) |

**Animation (G-11~G-14)**:

| 요소 ID | 위젯 | 설명 |
|---------|------|------|
| G-11 | `Slider` | Animation Speed (0.5x ~ 2.0x) |
| G-12 | `DropdownButton` | Transition Type (Fade / Slide / Scale) |
| G-13 | `DropdownButton` | Entrance (FadeIn / SlideUp / ScaleIn) |
| G-14 | `DropdownButton` | Exit (FadeOut / SlideDown / ScaleOut) |

**Branding (G-15~G-19)**:

| 요소 ID | 위젯 | 설명 |
|---------|------|------|
| G-15 | `FilePickerButton` + thumbnail | Event Logo |
| G-16 | `FilePickerButton` + position `DropdownButton` | Sponsor Logo 1 |
| G-17 | `FilePickerButton` + position `DropdownButton` | Sponsor Logo 2 |
| G-18 | `FilePickerButton` + position `DropdownButton` | Sponsor Logo 3 |
| G-19 | `Switch` + opacity `Slider` | Watermark |

### 6.3 Rules

9개 요소. 컴팩트 폼 레이아웃.

**Game Rules (G-20~G-23)**:

| 요소 ID | 위젯 | 설명 |
|---------|------|------|
| G-20 | `DropdownButtonFormField` | Game Type (22종: Hold'em, Omaha, Short Deck 등) |
| G-21 | `CheckboxListTile` | Straddle 허용 |
| G-22 | `DropdownButton` | Card Reveal Order (Left→Right / Simultaneous) |
| G-23 | `Switch` + `TextFormField` | Ante 활성화 + 금액 입력 |

**Player Display (G-24~G-28)**:

| 요소 ID | 위젯 | 설명 |
|---------|------|------|
| G-24 | `CheckboxListTile` | Position Display (D / SB / BB / UTG 등) |
| G-25 | `SegmentedButton` | Stack Direction (Above / Below) |
| G-26 | `DropdownButton` | Name Format (Full / First+Last Initial / Nickname) |
| G-27 | `Switch` | Country Display |
| G-28 | `Switch` | Photo Display |

### 6.4 Display

13개 요소. `GridView` 2컬럼 레이아웃.

**Blinds (G-29~G-33)**:

| 요소 ID | 위젯 | 설명 |
|---------|------|------|
| G-29 | `SegmentedButton` | Blind Format (100/200 vs 1/2 vs 0.1K/0.2K) |
| G-30 | `TextFormField` | Currency Symbol ($ / ₩ / €) |
| G-31 | `Switch` | Ante Display |
| G-32 | `Switch` | Level Display |
| G-33 | `Switch` | Break Timer |

**Precision (G-34~G-38)**:

| 요소 ID | 위젯 | 설명 |
|---------|------|------|
| G-34 | `DropdownButton` | Stack Precision (Exact / K / M) |
| G-35 | `DropdownButton` | Pot Precision (Exact / K / M) |
| G-36 | `DropdownButton` | Bet Precision (Exact / K / M) |
| G-37 | `DropdownButton` | Decimal Places (0 / 1 / 2) |
| G-38 | `SegmentedButton` | Separator (, vs .) |

**Mode (G-39~G-41)**:

| 요소 ID | 위젯 | 설명 |
|---------|------|------|
| G-39 | `SegmentedButton` | Display Mode (Tournament / Cash) |
| G-40 | `Switch` | BB Display (Show stack in BB) |
| G-41 | `SegmentedButton` | Chipcount Type (Exact / Estimated) |

### 6.5 System

13개 요소. 그룹별 `Container` (3.5 Elevation 스타일) 위젯으로 구분한다.

**Table (Y-01~Y-02)**:

| 요소 ID | 위젯 | 설명 |
|---------|------|------|
| Y-01 | `TextFormField` | Table Name |
| Y-02 | `TextFormField` | Table Number |

**RFID (Y-03~Y-07)**:

| 요소 ID | 위젯 | 설명 |
|---------|------|------|
| Y-03 | `_StatusDot` + `Text` | RFID Status (7색 도트, 읽기 전용) |
| Y-04 | `Text` | Antenna Count (읽기 전용) |
| Y-05 | `Text` | Reader Status (읽기 전용) |
| Y-06 | `ElevatedButton` | Register Deck (M-13 매핑) |
| Y-07 | `SegmentedButton` | RFID Mode (Auto / Manual / Off) |

**AT (Y-08~Y-09)**:

| 요소 ID | 위젯 | 설명 |
|---------|------|------|
| Y-08 | `_StatusDot` + `Text` | AT Connection (도트 + URL, 읽기 전용) |
| Y-09 | `Text` | AT Latency (ms 단위, 읽기 전용) |

**Diagnostics (Y-10~Y-12)**:

| 요소 ID | 위젯 | 설명 |
|---------|------|------|
| Y-10 | `LinearProgressIndicator` + `Text` | CPU Usage (%) |
| Y-11 | `LinearProgressIndicator` + `Text` | GPU Usage (%) |
| Y-12 | `LinearProgressIndicator` + `Text` | Memory Usage (%) |

CPU/GPU 인디케이터 색상은 3.1 Color의 3단계 체계(Green/Amber/Red)를 따른다.

**Startup (Y-13)**:

| 요소 ID | 위젯 | 설명 |
|---------|------|------|
| Y-13 | `Switch` | Auto-connect (앱 시작 시 자동 연결) |

## 7장. Preview Panel

Rive 오버레이를 Flutter 위젯으로 직접 임베드한다. NodeCG iframe 없이 네이티브 C++ 런타임으로 렌더링.

### 7.1 Rive 오버레이 임베드

```dart
AspectRatio(
  aspectRatio: 16 / 9,
  child: Container(
    color: const Color(0xFF0000FF),  // Chroma Key Blue
    child: FittedBox(
      child: Stack(children: [
        RiveAnimation.asset('assets/rive/board.riv',
          stateMachines: ['BoardState']),
        RiveAnimation.asset('assets/rive/player.riv',
          stateMachines: ['PlayerState']),
        RiveAnimation.asset('assets/rive/blinds.riv',
          stateMachines: ['BlindsState']),
        RiveAnimation.asset('assets/rive/field.riv',
          stateMachines: ['FieldState']),
        RiveAnimation.asset('assets/rive/divider.riv',
          stateMachines: ['DividerState']),
        RiveAnimation.asset('assets/rive/cards.riv',
          stateMachines: ['CardsState']),
      ]),
    ),
  ),
)
```

### 7.2 오버레이 레이어 구성

6개 Rive 파일이 `Stack`으로 겹쳐 하나의 방송 오버레이를 구성한다:

| 레이어 | .riv 파일 | StateMachine | 역할 |
|--------|----------|-------------|------|
| Board | `board.riv` | `BoardState` | 커뮤니티 카드, POT, 사이드팟 |
| Player | `player.riv` | `PlayerState` | 이름, 스택, 홀카드, 액션, 사진 |
| Blinds | `blinds.riv` | `BlindsState` | SB/BB, Ante, 핸드 번호, 이벤트 로고 |
| Field | `field.riv` | `FieldState` | 잔여 플레이어 수 |
| Divider | `divider.riv` | `DividerState` | 분할선 |
| Cards | `cards.riv` | `CardsState` | 52장 카드 에셋 |

### 7.3 스케일링

`FittedBox`로 `panes` 리사이즈 시 Preview Panel 크기에 맞춰 자동 스케일링된다. `AspectRatio(16/9)`가 비율을 고정하므로 오버레이 왜곡이 발생하지 않는다.

**v1.0 요소 매핑**: M-02 (Preview Panel)

## 8장. Rive Integration

### 9.1 초기화

Rive 런타임은 앱 시작 시 Flutter 엔진 초기화 이후 즉시 로드한다:

```dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await RiveFile.initialize();  // Rive 런타임 초기화
  runApp(const ProviderScope(child: EbsConsoleApp()));
}
```

### 9.2 오버레이 .riv 파일

6개 Rive 파일이 방송 오버레이를 구성한다:

| 파일 | StateMachine | 입력 | 역할 |
|------|-------------|------|------|
| player.riv | PlayerState | isActive(bool), chipCount(number), action(trigger), fold(trigger), showdown(trigger) | 플레이어 그래픽 |
| board.riv | BoardState | street(number: 0~4), potSize(number), showCards(trigger) | 보드 그래픽 |
| blinds.riv | BlindsState | sb(number), bb(number), ante(number), handNumber(number) | 블라인드 표시 |
| field.riv | FieldState | remaining(number), total(number) | 잔여 플레이어 |
| divider.riv | DividerState | isVisible(bool) | 분할선 |
| cards.riv | CardsState | cardIndex(number), isRevealed(bool), flipCard(trigger) | 카드 에셋 |

### 9.3 StateMachine API

Rive 0.14.4 기준 StateMachine 입력 제어 패턴:

```dart
late RiveAnimationController _controller;

void _onRiveInit(Artboard artboard) {
  final controller = StateMachineController.fromArtboard(artboard, 'PlayerState');
  if (controller != null) {
    artboard.addController(controller);
    // Boolean 입력
    controller.findInput<bool>('isActive')?.value = true;
    // Number 입력
    controller.findInput<double>('chipCount')?.value = 50000;
    // Trigger 입력
    (controller.findInput<bool>('showdown') as SMITrigger?)?.fire();
  }
}

RiveAnimation.asset(
  'assets/rive/player.riv',
  stateMachines: const ['PlayerState'],
  onInit: _onRiveInit,
)
```

입력 타입 3종:
- **Boolean** (`SMIBool`): `.value = true/false`로 상태 전환
- **Number** (`SMINumber`): `.value = double`로 수치 입력
- **Trigger** (`SMITrigger`): `.fire()`로 1회성 이벤트 발화

> **API 버전 주의**: Rive Flutter 0.14.x에서 StateMachine 관련 클래스명이 변경될 수 있다.
> `StateMachineController`, `SMIBool`, `SMINumber`, `SMITrigger` 등은 0.13.x 기준 API이며,
> 0.14.4 정식 릴리스 시점의 마이그레이션 가이드를 반드시 확인해야 한다.
> 대안: `controller.findInput<bool>('name')` 대신 `controller.getBoolInput('name')` 등
> getter 메서드가 도입될 수 있으므로, 구현 시 pub.dev 최신 문서를 참조한다.

### 9.4 UI 마이크로 애니메이션

| 대상 | 방식 | 설정 |
|------|------|------|
| 탭 전환 | `AnimatedSwitcher` | 200ms 페이드 |
| 버튼 호버 | Rive 마이크로 애니메이션 (선택 사항, CSS transition 대체 가능) | — |
| 로딩 인디케이터 | Rive 스피너 | `assets/rive/loading.riv` |
| 연결 상태 도트 | 펄스 애니메이션 | 연결 시도 중일 때만 활성화 |

로딩 스피너와 연결 도트 펄스는 별도 `.riv` 파일로 분리하여 메인 오버레이 로드와 독립적으로 동작한다.

## 9장. State Management

Riverpod 3.0 기반 4계층 Provider 구조.

### 10.1 Provider 구조

```dart
// 1. Console 설정 — 5탭 86개 설정 (JSON persist)
@riverpod
class ConsoleSettings extends _$ConsoleSettings {
  @override
  ConsoleSettingsState build() => ConsoleSettingsState.fromJson(
    _loadFromDisk(),  // SharedPreferences or local JSON
  );

  void updateSetting(String key, dynamic value) {
    state = state.copyWith(key: value);
    _saveToDisk(state.toJson());
  }
}

// 2. 게임 상태 스트림 — WebSocket (auto-retry)
@riverpod
Stream<GameState> gameState(Ref ref) {
  final ws = ref.watch(webSocketProvider);
  return ws.stream.map((msg) => GameState.fromJson(jsonDecode(msg)));
}

// 3. 연결 상태 — 4개 서비스
@riverpod
class ConnectionStatus extends _$ConnectionStatus {
  @override
  Map<String, ConnectionState> build() => {
    'engine': ConnectionState.disconnected,
    'nodecg': ConnectionState.disconnected,
    'casparcg': ConnectionState.disconnected,
    'at': ConnectionState.disconnected,
  };
}

// 4. Rive 컨트롤러 캐시
@riverpod
StateMachineController? riveController(Ref ref, String artboardName) => null;
```

### 10.2 Mutations API

액션 실행의 라이프사이클을 `AsyncValue`로 관리한다:

```dart
// Reset Hand 액션 라이프사이클
@riverpod
class ResetHand extends _$ResetHand {
  @override
  AsyncValue<void> build() => const AsyncData(null);

  Future<void> execute() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      await ref.read(webSocketProvider).send(jsonEncode({'type': 'reset_hand'}));
    });
  }
}
```

> **주의**: Mutations API는 Riverpod 3.0에서 experimental로 제공된다.
> 향후 breaking change 가능성이 있으므로, 프로덕션 배포 전 안정화 상태를 확인한다.
> 대안: Mutations 대신 `AsyncNotifier` + `AsyncValue.guard()` 패턴으로 동일 기능 구현 가능.

### 10.3 Auto-Retry 지수 백오프

WebSocket 연결 끊김 시 자동 재연결: `1s → 2s → 4s → 8s → 16s max` 간격. 최대 재시도 횟수 제한 없음 (방송 환경에서는 끊김 시 무한 재시도가 올바른 동작).

### 10.4 Offline Persist

`ConsoleSettings`는 앱 종료 시 JSON 파일로 저장하고, 재시작 시 복원한다. WebSocket 미연결 상태에서도 설정 변경이 가능하며, 연결 복구 시 서버에 일괄 전송한다.

## 10장. Interaction Patterns

6가지 핵심 인터랙션 패턴.

### 11.1 Hover

`MouseRegion` + `AnimatedContainer` 150ms. 배경 zinc-800 → zinc-700 전환:

```dart
MouseRegion(
  onEnter: (_) => setState(() => isHovered = true),
  onExit: (_) => setState(() => isHovered = false),
  child: AnimatedContainer(
    duration: const Duration(milliseconds: 150),
    color: isHovered ? const Color(0xFF3F3F46) : const Color(0xFF27272A),
    child: child,
  ),
)
```

### 11.2 Focus

`FocusTraversalGroup`으로 탭 키 순서를 관리한다. 탭 전환 시 첫 번째 입력 필드에 자동 포커스를 부여한다.

### 11.3 탭 전환

`IndexedStack`으로 5탭 상태를 유지한다. 탭 이동 시 스크롤 위치와 입력값이 보존된다:

```dart
IndexedStack(
  index: currentTab,
  children: const [IoTab(), GfxTab(), RulesTab(), DisplayTab(), SystemTab()],
)
```

### 11.4 폼 커밋

`onFieldSubmitted` → Provider 업데이트 → WebSocket 전송. 변경 즉시 반영하며 별도 Save 버튼은 없다. 유효성 검증 실패 시 필드 테두리를 Red로 표시하고 이전 값을 유지한다.

### 11.5 Undo

Ctrl+Z로 이전 상태를 복원한다. Provider 기반 스냅샷 히스토리를 유지하며, 최대 10단계까지 되돌릴 수 있다.

### 11.6 드래그

`panes` 패키지 리사이즈 핸들로 영역 크기를 조정한다. 드래그 중 `SystemMouseCursors.resizeColumn` 커서로 변경하여 리사이즈 가능 영역임을 시각적으로 표시한다.

## 11장. Changelog

| 날짜 | 버전 | 변경 내용 | 결정 근거 |
|------|------|-----------|----------|
| 2026-03-04 | v2.0.0 | 최초 작성 — React/Electron(v1.0) → Flutter Desktop + Rive(v2.0) 전면 재설계. RFID Grey/Black hex Zinc 팔레트로 변경, CPU/GPU 인디케이터 Yellow→Amber 변경, 요소 ID 번호 재할당 | CLAUDE.md 아키텍처(Flutter + Rive) 준수, Zinc 팔레트 통일 |

### v1.0 → v2.0 계승 사항

- v1.0 86개 요소 ID 체계 (M/S/O/G/Y 접두사) 유지
- RFID 7색 상태 체계 계승 (Grey/Black hex를 Zinc 팔레트로 조정)
- 5탭 구조 (I/O, GFX, Rules, Display, System) 유지
- Preview Panel 16:9 비율 + Chroma Key 배경 유지

배제 사항:
- M-07 Lock Toggle: v2.0에서 배제. 방송 중 설정 잠금은 Riverpod Provider의 읽기 전용 모드로 대체.

---

**Version**: 2.0.0 | **Updated**: 2026-03-04

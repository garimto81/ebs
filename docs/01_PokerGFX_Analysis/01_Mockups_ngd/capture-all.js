const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

// PokerGFX Server UI mockups (numbered series)
const serverMockups = [
  { html: '01-main-window.html', png: '01-main-window.png', width: 830, height: 420 },
  { html: '02-sources-tab.html', png: '02-sources-tab.png', width: 785, height: 720 },
  { html: '03-outputs-tab.html', png: '03-outputs-tab.png', width: 785, height: 720 },
  { html: '04-gfx1-tab.html', png: '04-gfx1-tab.png', width: 785, height: 745 },
  { html: '05-gfx2-tab.html', png: '05-gfx2-tab.png', width: 785, height: 680 },
  { html: '06-gfx3-tab.html', png: '06-gfx3-tab.png', width: 785, height: 710 },
  { html: '07-commentary-tab.html', png: '07-commentary-tab.png', width: 785, height: 620 },
  { html: '08-system-tab.html', png: '08-system-tab.png', width: 785, height: 690 },
  { html: '09-skin-editor.html', png: '09-skin-editor.png', width: 950, height: 520 },
  { html: '10-graphic-editor-board.html', png: '10-graphic-editor-board.png', width: 710, height: 640 },
  { html: '11-graphic-editor-player.html', png: '11-graphic-editor-player.png', width: 710, height: 560 },
  { html: '13-action-tracker-wireframe.html', png: '13-action-tracker-wireframe.png', width: 1000, height: 800 },
  { html: '14-viewer-overlay-wireframe.html', png: '14-viewer-overlay-wireframe.png', width: 1000, height: 800 },
];

// PokerGFX analysis diagrams (PRD-referenced)
const analysisDiagrams = [
  { html: 'pokergfx-sports-vs-poker.html', png: 'pokergfx-sports-vs-poker.png', width: 1000, height: 800 },
  { html: 'pokergfx-module-overview.html', png: 'pokergfx-module-overview.png', width: 720, height: 720 },
  { html: 'pokergfx-hand-lifecycle.html', png: 'pokergfx-hand-lifecycle.png', width: 1000, height: 800 },
  { html: 'pokergfx-system-architecture.html', png: 'pokergfx-system-architecture.png', width: 1000, height: 800 },
  { html: 'pokergfx-rfid-subsystem.html', png: 'pokergfx-rfid-subsystem.png', width: 1000, height: 800 },
  { html: 'pokergfx-service-pipeline.html', png: 'pokergfx-service-pipeline.png', width: 1000, height: 800 },
  { html: 'pokergfx-graphics-hierarchy.html', png: 'pokergfx-graphics-hierarchy.png', width: 1000, height: 800 },
  { html: 'pokergfx-network-protocol.html', png: 'pokergfx-network-protocol.png', width: 1000, height: 800 },
  { html: 'pokergfx-security-modes.html', png: 'pokergfx-security-modes.png', width: 1000, height: 800 },
  { html: 'pokergfx-drm-licensing.html', png: 'pokergfx-drm-licensing.png', width: 1000, height: 800 },
  { html: 'pokergfx-broadcast-overlay.html', png: 'pokergfx-broadcast-overlay.png', width: 1000, height: 800 },
  { html: 'pokergfx-data-flow.html', png: 'pokergfx-data-flow.png', width: 1000, height: 800 },
];

const files = [...serverMockups, ...analysisDiagrams];

(async () => {
  const browser = await chromium.launch();
  const outputDir = __dirname;

  let ok = 0, skip = 0;
  for (const f of files) {
    const htmlPath = path.join(__dirname, f.html);
    if (!fs.existsSync(htmlPath)) {
      console.log(`SKIP: ${f.html} not found`);
      skip++;
      continue;
    }
    const page = await browser.newPage({ viewport: { width: f.width, height: f.height } });
    await page.goto(`file:///${htmlPath.replace(/\\/g, '/')}`);
    await page.waitForTimeout(500);

    // Hide annotation overlays for clean mockup captures
    await page.evaluate(() => {
      document.querySelectorAll('.box, .label, .annotation, .callout').forEach(el => {
        el.style.display = 'none';
      });
    });
    await page.waitForTimeout(100);

    const container = await page.$('.container');
    if (container) {
      await container.screenshot({ path: path.join(outputDir, f.png) });
      console.log(`OK: ${f.png}`);
    } else {
      await page.screenshot({ path: path.join(outputDir, f.png), fullPage: true });
      console.log(`OK (full): ${f.png}`);
    }
    ok++;
    await page.close();
  }

  await browser.close();
  console.log(`\nDone! ${ok} captured, ${skip} skipped.`);
})();

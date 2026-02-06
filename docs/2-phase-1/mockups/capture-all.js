const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const files = [
  { html: '01-main-window.html', png: '01-main-window.png', width: 785, height: 385 },
  { html: '02-sources-tab.html', png: '02-sources-tab.png', width: 785, height: 720 },
  { html: '03-outputs-tab.html', png: '03-outputs-tab.png', width: 785, height: 720 },
  { html: '04-gfx1-tab.html', png: '04-gfx1-tab.png', width: 785, height: 745 },
  { html: '05-gfx2-tab.html', png: '05-gfx2-tab.png', width: 785, height: 680 },
  { html: '06-gfx3-tab.html', png: '06-gfx3-tab.png', width: 785, height: 710 },
  { html: '07-commentary-tab.html', png: '07-commentary-tab.png', width: 785, height: 620 },
  { html: '08-system-tab.html', png: '08-system-tab.png', width: 785, height: 690 },
  { html: '09-skin-editor.html', png: '09-skin-editor.png', width: 903, height: 481 },
  { html: '10-graphic-editor-board.html', png: '10-graphic-editor-board.png', width: 664, height: 600 },
  { html: '11-graphic-editor-player.html', png: '11-graphic-editor-player.png', width: 664, height: 520 },
];

(async () => {
  const browser = await chromium.launch();
  const outputDir = path.join(__dirname, '..', 'annotated');
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

  for (const f of files) {
    const htmlPath = path.join(__dirname, f.html);
    if (!fs.existsSync(htmlPath)) {
      console.log(`SKIP: ${f.html} not found`);
      continue;
    }
    const page = await browser.newPage({ viewport: { width: f.width, height: f.height } });
    await page.goto(`file:///${htmlPath.replace(/\\/g, '/')}`);
    await page.waitForTimeout(500);

    // Screenshot just the container element for tight crop
    const container = await page.$('.container');
    if (container) {
      await container.screenshot({ path: path.join(outputDir, f.png) });
      console.log(`OK: ${f.png}`);
    } else {
      await page.screenshot({ path: path.join(outputDir, f.png), fullPage: true });
      console.log(`OK (full): ${f.png}`);
    }
    await page.close();
  }

  await browser.close();
  console.log('All done!');
})();

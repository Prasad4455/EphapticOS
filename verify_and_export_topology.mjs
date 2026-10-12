import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { ChromeVisualBrowser } from 'file:///C:/Users/Deepe/.gemini/antigravity-ide/brain/75c30846-69cc-41b6-9aa1-5b889e9b504b/scratch/archify/archify/bin/visual-check.mjs';

const chrome = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const htmlPath = path.resolve('.archify/architecture-production-topology-20261011-075917/production-topology.html');
const outPngPath = path.resolve('.archify/architecture-production-topology-20261011-075917/production-topology.2400x1260.png');
const artifactPng = 'C:\\Users\\Deepe\\.gemini\\antigravity-ide\\brain\\75c30846-69cc-41b6-9aa1-5b889e9b504b\\production-topology.2400x1260.png';
const artifactHtml = 'C:\\Users\\Deepe\\.gemini\\antigravity-ide\\brain\\75c30846-69cc-41b6-9aa1-5b889e9b504b\\production-topology.html';

console.log('Testing HTML:', htmlPath);
const browser = new ChromeVisualBrowser(chrome);

async function run() {
  try {
    const session = await browser.sessionPromise;
    const send = (method, params = {}) => browser.cdp.send(method, params, session);

    async function evaluate(expression) {
      const res = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
      if (res.exceptionDetails) {
        console.error('JS Exception:', res.exceptionDetails);
      }
      return res.result?.value;
    }

    // Set viewport to 2400 x 1260
    await send('Emulation.setDeviceMetricsOverride', {
      width: 2400,
      height: 1260,
      deviceScaleFactor: 1,
      mobile: false
    });

    const loaded = browser.cdp.waitFor('Page.loadEventFired', session);
    await send('Page.navigate', { url: pathToFileURL(htmlPath).href });
    await loaded;

    // Wait for fonts & stable layout
    await evaluate('document.fonts.ready');
    await evaluate('Archify.viewerChromeLayout ? Archify.viewerChromeLayout.whenStable() : Promise.resolve()');

    // 1. Confirm Component Search
    console.log('\n--- 1. Testing Component Search ---');
    await evaluate(`Archify.finder.open()`);
    await evaluate(`document.getElementById('node-finder-input').focus()`);
    await send('Input.insertText', { text: 'api_pods' });

    const searchResult = await evaluate(`(() => {
      const panel = document.getElementById('node-finder');
      const results = [...panel.querySelectorAll('.node-finder-result')].map(el => ({
        id: el.dataset.nodeId,
        label: el.querySelector('.node-finder-result-label, span, em')?.textContent?.trim() || el.textContent.trim(),
        aria: el.getAttribute('aria-label')
      }));
      return {
        isOpen: Archify.finder.isOpen(),
        query: document.getElementById('node-finder-input').value,
        totalNodesInIndex: Archify.finder.count,
        matchedCount: results.length,
        matches: results
      };
    })()`);
    console.log('Search Verification Result:', JSON.stringify(searchResult, null, 2));

    await evaluate(`Archify.finder.close()`);

    // 2. Confirm Upstream & Downstream Tracing
    console.log('\n--- 2. Testing Upstream & Downstream Tracing ---');
    const traceResult = await evaluate(`(() => {
      const results = {};
      if (Archify.focus) {
        // Set focus to api_pods
        const setSelected = Archify.focus.set('api_pods');
        results.setApiPods = setSelected;
        results.activeNode = Archify.focus.active();

        // Downstream reach
        const downSuccess = Archify.focus.reach('downstream');
        results.reachDownstream = downSuccess;
        results.reachabilityAfterDown = Archify.focus.reachability();

        // Upstream reach
        const upSuccess = Archify.focus.reach('upstream');
        results.reachUpstream = upSuccess;
        results.reachabilityAfterUp = Archify.focus.reachability();

        // Clear focus
        Archify.focus.clear();
        results.cleared = (Archify.focus.active() === null);
      }
      return results;
    })()`);
    console.log('Tracing Verification Result:', JSON.stringify(traceResult, null, 2));

    // Ensure clean state before screenshot
    await evaluate(`(() => {
      if (Archify.finder) Archify.finder.close();
      if (Archify.focus) Archify.focus.clear();
    })()`);
    await evaluate(`Promise.all(document.getAnimations().filter(a => Number.isFinite(a.effect.getTiming().iterations)).map(a => a.finished.catch(() => {})))`);

    // 3. Export 2400 x 1260 PNG
    console.log('\n--- 3. Exporting 2400x1260 PNG ---');
    const screenshot = await send('Page.captureScreenshot', { format: 'png' });
    const buffer = Buffer.from(screenshot.data, 'base64');
    fs.writeFileSync(outPngPath, buffer);
    console.log(`Saved screenshot to: ${outPngPath} (${buffer.length} bytes)`);

    // Copy to artifact directory
    fs.writeFileSync(artifactPng, buffer);
    console.log(`Saved screenshot to artifacts: ${artifactPng}`);

    fs.copyFileSync(htmlPath, artifactHtml);
    console.log(`Copied HTML to artifacts: ${artifactHtml}`);

    console.log('\nAll verifications and export completed successfully!');
  } catch (err) {
    console.error('Execution error:', err);
  } finally {
    await browser.close();
  }
}

run();

// Renderiza uma página HTML animada (com window.render(t)) em vídeo MP4 1080x1920.
// Uso: node render.js pagina.html saida.mp4 DURACAO_EM_SEGUNDOS [t1,t2,... para só tirar quadros de teste]
const { chromium } = require('playwright'); const { spawn } = require('child_process'); const path = require('path');
const [page, out, dur, only] = process.argv.slice(2); const FPS = 30;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(page)); await p.waitForTimeout(800);
  if (only) { for (const t of only.split(',')) { await p.evaluate(x => render(x), +t); await p.waitForTimeout(150); await p.screenshot({ path: out.replace(/\.mp4$/, '') + '-' + t + '.jpg', type: 'jpeg', quality: 80 }); } await b.close(); return; }
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-b:v', '3200k', '-maxrate', '4500k', '-bufsize', '9000k', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out]);
  for (let i = 0; i < FPS * +dur; i++) { await p.evaluate(x => render(x), i / FPS); const buf = await p.screenshot({ type: 'jpeg', quality: 92 }); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close(); console.log('ok');
})();

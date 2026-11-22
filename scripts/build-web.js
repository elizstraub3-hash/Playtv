// Monta o site publicado na Vercel (pasta dist/):
//   /          → página de vendas (site/index.html)
//   /app/      → versão web do aplicativo (www/)
//   demais arquivos de www/ também ficam na raiz (ícone, capa, fontes, política de privacidade)
const fs = require('fs');
const path = require('path');
const root = path.join(__dirname, '..');
const dist = path.join(root, 'dist');
fs.rmSync(dist, { recursive: true, force: true });
fs.cpSync(path.join(root, 'www'), dist, { recursive: true });
fs.cpSync(path.join(root, 'www'), path.join(dist, 'app'), { recursive: true });
fs.cpSync(path.join(root, 'site'), dist, { recursive: true });
console.log('Site montado em dist/');

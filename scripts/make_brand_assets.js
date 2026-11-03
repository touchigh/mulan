const {chromium}=require('playwright');
const R=require('path').resolve(__dirname,'..')+'/';
(async()=>{const b=await chromium.launch();const p=await b.newPage();
const fonts='<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400&display=swap">';
const hero='data:image/jpeg;base64,'+require('fs').readFileSync(''+R+'img/hero.jpg').toString('base64');
await p.setViewportSize({width:1200,height:630});
await p.setContent(`${fonts}<style>body{margin:0;width:1200px;height:630px;display:flex;font-family:Jost,'Noto Sans CJK SC',sans-serif;background:#FBFCFD;color:#12263D}
.l{width:560px;padding:64px;display:flex;flex-direction:column;justify-content:center;gap:20px}.m{font-weight:300;letter-spacing:.18em;font-size:30px}
h1{font-weight:400;font-size:52px;line-height:1.08;margin:0}em{font-style:normal;font-weight:300;color:#1F4E7A}p{font-size:22px;color:#4D6074;margin:0}
.r{flex:1;background:url(${hero}) center/cover}</style><div class="l"><div class="m">沐岚 MU LAN</div><h1>Bathrooms that let older people <em>stay independent</em></h1><p>Aging-friendly bathroom products · Foshan</p></div><div class="r"></div>`,{waitUntil:'networkidle'}).catch(()=>{});
await p.waitForTimeout(800);await p.screenshot({path:''+R+'brand/og-home.jpg',type:'jpeg',quality:80});
await p.setViewportSize({width:512,height:512});
await p.setContent(`${fonts}<style>body{margin:0;width:512px;height:512px;background:#1F4E7A;color:#fff;display:grid;place-items:center;font-family:'Noto Sans CJK SC',sans-serif;font-size:300px;font-weight:300}</style>沐`);
await p.screenshot({path:''+R+'brand/favicon.png'});
await p.setViewportSize({width:800,height:200});
await p.setContent(`${fonts}<style>body{margin:0;width:800px;height:200px;background:#fff;color:#12263D;display:grid;place-items:center;font-family:Jost,'Noto Sans CJK SC',sans-serif;font-size:72px;font-weight:300;letter-spacing:.18em}</style><div>沐岚 MU LAN</div>`,{waitUntil:'networkidle'}).catch(()=>{});
await p.waitForTimeout(500);await p.screenshot({path:''+R+'brand/logo.png'});
await b.close();})();

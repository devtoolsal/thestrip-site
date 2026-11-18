import { createRequire } from "node:module";
import { readFile, writeFile } from "node:fs/promises";
import sharp from "sharp";

const require = createRequire(import.meta.url);
const { renderReceipt } = require("../api/dist/photos/photo-render.js");

const SITE = "https://devtoolsal.github.io/thestrip-site/contact.html";
const TITLES = ["THE BIG DAY", "THE LATE NIGHT", "THE SOMETHING ELSE"];
const DATE = "18 NOV 2026";

for (let index = 1; index <= 12; index += 1) {
  const pad = String(index).padStart(2, "0");
  const source = await readFile(`assets/gallery-${pad}.jpg`);

  const rendered = await renderReceipt(source, {
    planName: TITLES[(index - 1) % TITLES.length],
    priceLabel: `${pad} / 12`,
    orderId: pad,
    dateLabel: DATE,
    downloadUrl: SITE,
    qrHeading1: "SCAN TO",
    qrHeading2: "STEP IN",
    qrFooter: "thestripphotobooth.co.za"
  });

  const printMeta = await sharp(rendered.printPng).metadata();
  const stripWidth = 720;
  const stripHeight = Math.round(stripWidth * printMeta.height / printMeta.width);
  const canvasWidth = 1200;
  const canvasHeight = stripHeight + 190;
  const stripX = Math.round((canvasWidth - stripWidth) / 2);
  const stripY = 70;
  const centerX = canvasWidth / 2;
  const centerY = stripY + stripHeight / 2;

  const poster = `<svg xmlns="http://www.w3.org/2000/svg" width="${canvasWidth}" height="${canvasHeight}">
    <defs>
      <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="18"/>
      </filter>
      <filter id="grain" x="0" y="0" width="100%" height="100%">
        <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/>
        <feColorMatrix type="saturate" values="0"/>
        <feComponentTransfer><feFuncA type="table" tableValues="0 0.035"/></feComponentTransfer>
      </filter>
    </defs>

    <rect width="${canvasWidth}" height="${canvasHeight}" fill="#F4F3EF"/>

    <g transform="rotate(-1.6 ${centerX} ${centerY})">
      <rect x="${stripX + 8}" y="${stripY + 16}" width="${stripWidth}" height="${stripHeight}" fill="#232320" opacity="0.22" filter="url(#shadow)"/>
      <image x="${stripX}" y="${stripY}" width="${stripWidth}" height="${stripHeight}"
        href="data:image/png;base64,${rendered.printPng.toString("base64")}"/>
    </g>

    <line x1="60" y1="${canvasHeight - 78}" x2="140" y2="${canvasHeight - 78}" stroke="#9E5538" stroke-width="2"/>
    <text x="60" y="${canvasHeight - 42}" font-family="Helvetica, Arial, sans-serif" font-size="14" letter-spacing="5" fill="#5E5B55">THE ART OF THE MOMENT.</text>
    <text x="${canvasWidth - 60}" y="${canvasHeight - 42}" text-anchor="end" font-family="Helvetica, Arial, sans-serif" font-size="14" letter-spacing="3" fill="#5E5B55">THE STRIP · GALLERY ${pad}</text>

    <rect width="${canvasWidth}" height="${canvasHeight}" filter="url(#grain)" opacity="0.55"/>
  </svg>`;

  const posterBuffer = await sharp(Buffer.from(poster)).jpeg({ quality: 92 }).toBuffer();

  await writeFile(
    `assets/gallery-print-${pad}.jpg`,
    await sharp(posterBuffer).resize({ width: 1000 }).jpeg({ quality: 88 }).toBuffer()
  );
  await writeFile(
    `assets/gallery-print-sm-${pad}.jpg`,
    await sharp(posterBuffer).resize({ width: 700 }).jpeg({ quality: 82 }).toBuffer()
  );
  console.log(`gallery-print-${pad}.jpg + gallery-print-sm-${pad}.jpg`);
}

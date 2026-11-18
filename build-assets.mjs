import sharp from "sharp";
import { writeFile } from "node:fs/promises";

const favicon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect width="100" height="100" rx="18" fill="#232320"/>
  <text x="50" y="74" text-anchor="middle" font-family="DM Sans, Arial, sans-serif" font-weight="700" font-size="66" fill="#F4F3EF">S</text>
</svg>`;

await writeFile("assets/favicon.svg", favicon);
await sharp(Buffer.from(favicon)).resize(180, 180).png().toFile("assets/apple-touch-icon.png");

const strips = [];
for (let index = 0; index < 3; index += 1) {
  const names = ["gallery-03.jpg", "gallery-07.jpg", "gallery-11.jpg"];
  const input = await sharp(`assets/${names[index]}`)
    .resize(140, 420, { fit: "cover" })
    .toBuffer();
  strips.push({ input, left: 728 + index * 152, top: 105 });
}

const text = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630">
  <text x="70" y="116" font-family="Helvetica, Arial, sans-serif" font-size="16" letter-spacing="5" fill="#9E5538">ENCLOSED PHOTOBOOTH</text>
  <text x="66" y="262" font-family="Helvetica, Arial, sans-serif" font-size="118" font-weight="700" letter-spacing="-6" fill="#232320">The Strip</text>
  <line x1="70" y1="300" x2="150" y2="300" stroke="#9E5538" stroke-width="3"/>
  <text x="70" y="360" font-family="Helvetica, Arial, sans-serif" font-size="34" fill="#232320">Behind the curtain.</text>
  <text x="70" y="402" font-family="Helvetica, Arial, sans-serif" font-size="34" fill="#232320">In the moment.</text>
  <text x="70" y="462" font-family="Helvetica, Arial, sans-serif" font-size="20" fill="#77756E">A little privacy. A lot of personality.</text>
</svg>`;

await sharp({
  create: { width: 1200, height: 630, channels: 3, background: "#F4F3EF" }
})
  .composite([...strips, { input: Buffer.from(text), left: 0, top: 0 }])
  .jpeg({ quality: 90 })
  .toFile("assets/og-image.jpg");

console.log("assets built");

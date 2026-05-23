import fs from "node:fs";
import path from "node:path";

const root = process.cwd();

const dataFiles = [
    "src/modules/public/data/home-page.data.ts",
    "src/modules/public/data/about-page.data.ts",
    "src/modules/public/data/contacts-page.data.ts",
    "src/modules/public/data/teachers-page.data.ts",
];

const translationsPath = "src/i18n/public-content.translations.ts";

function readFile(filePath) {
    return fs.readFileSync(path.join(root, filePath), "utf8");
}

function extractRussianStrings(content) {
    const result = new Set();
    const regex = /"((?:[^"\\]|\\.)*)"|`([^`]*)`/gs;
    let match;

    while ((match = regex.exec(content))) {
        const value = (match[1] ?? match[2] ?? "")
            .replaceAll("\\n", " ")
            .replace(/\s+/g, " ")
            .trim();

        if (/[А-Яа-яЁё]/.test(value)) {
            result.add(value);
        }
    }

    return result;
}

const translationsContent = readFile(translationsPath);
const translatedKeys = new Set();

for (const match of translationsContent.matchAll(/"((?:[^"\\]|\\.)*)"\s*:/g)) {
    translatedKeys.add(match[1]);
}

const missing = [];

for (const file of dataFiles) {
    const content = readFile(file);
    const strings = extractRussianStrings(content);

    for (const value of strings) {
        if (!translatedKeys.has(value)) {
            missing.push({
                file,
                value,
            });
        }
    }
}

if (!missing.length) {
    console.log("✅ Все публичные строки переведены.");
    process.exit(0);
}

console.log(`❌ Не переведено строк: ${missing.length}\n`);

for (const item of missing) {
    console.log(`- ${item.file}`);
    console.log(`  "${item.value}"\n`);
}

process.exit(1);

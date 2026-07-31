#!/usr/bin/env node

/**
 * MY_SKILL Installer — Copy skills to any directory you choose.
 *
 * No hardcoded paths. You decide where skills go.
 *
 * Usage:
 *   npx github:AVA-2568/MY_SKILL              # copy to current directory (./skills/)
 *   npx github:AVA-2568/MY_SKILL --target DIR # copy to custom directory
 *   npx github:AVA-2568/MY_SKILL --list       # list all available skills
 *   npx github:AVA-2568/MY_SKILL --help       # show help
 */

const fs = require("fs");
const path = require("path");

const SKILLS_DIR = path.join(__dirname, "..", "skills");
const INDEX_PATH = path.join(__dirname, "..", "INDEX.yaml");

function listSkills() {
  const items = fs.readdirSync(SKILLS_DIR, { withFileTypes: true });
  const skills = items.filter((d) => d.isDirectory()).map((d) => d.name);
  console.log(`\n  📦 MY_SKILL — ${skills.length} skills available\n`);
  skills.forEach((s, i) => {
    const skPath = path.join(SKILLS_DIR, s, "SKILL.md");
    let desc = "";
    if (fs.existsSync(skPath)) {
      const content = fs.readFileSync(skPath, "utf-8");
      const m = content.match(/^description:\s*(.+)$/m);
      if (m) desc = m[1].trim();
    }
    console.log(`  ${String(i + 1).padStart(2)}. ${s.padEnd(28)} ${desc.slice(0, 60)}`);
  });
  console.log("");
}

function installSkills(targetDir) {
  // Default: current working directory, create a skills/ subfolder
  if (!targetDir) targetDir = path.join(process.cwd(), "skills");

  if (!fs.existsSync(targetDir)) {
    fs.mkdirSync(targetDir, { recursive: true });
  }

  const items = fs.readdirSync(SKILLS_DIR, { withFileTypes: true });
  const skills = items.filter((d) => d.isDirectory()).map((d) => d.name);

  console.log(`\n  📦 Installing ${skills.length} skills to: ${targetDir}\n`);

  let copied = 0;
  skills.forEach((name) => {
    const src = path.join(SKILLS_DIR, name);
    const dst = path.join(targetDir, name);

    if (fs.existsSync(dst)) {
      fs.rmSync(dst, { recursive: true, force: true });
    }

    copyDirSync(src, dst);
    copied++;
    console.log(`  ✅ ${name}`);
  });

  // Copy INDEX.yaml alongside skills
  if (fs.existsSync(INDEX_PATH)) {
    const idxDst = path.join(targetDir, "..", "INDEX.yaml");
    fs.copyFileSync(INDEX_PATH, idxDst);
    console.log(`  ✅ INDEX.yaml`);
  }

  console.log(`\n  ✨ Done! ${copied} skills copied to: ${targetDir}\n`);
}

function copyDirSync(src, dst) {
  fs.mkdirSync(dst, { recursive: true });
  const entries = fs.readdirSync(src, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const dstPath = path.join(dst, entry.name);
    if (entry.isDirectory()) {
      copyDirSync(srcPath, dstPath);
    } else {
      fs.copyFileSync(srcPath, dstPath);
    }
  }
}

function printHelp() {
  console.log(`
  MY_SKILL — Personal Skill Library

  No hardcoded paths. You decide where skills go.

  Usage:
    npx github:AVA-2568/MY_SKILL                  Copy skills to ./skills/ (current dir)
    npx github:AVA-2568/MY_SKILL --target <DIR>   Copy to a custom directory
    npx github:AVA-2568/MY_SKILL --list            List available skills
    npx github:AVA-2568/MY_SKILL --help            Show this help

  Examples:
    npx github:AVA-2568/MY_SKILL
    npx github:AVA-2568/MY_SKILL --target ~/.trae-cn/skills
    npx github:AVA-2568/MY_SKILL --target ./my-skills
  `);
}

// ── CLI ───────────────────────────────────────────────────────────────

const args = process.argv.slice(2);

if (args.includes("--help") || args.includes("-h")) {
  printHelp();
  process.exit(0);
}

if (args.includes("--list") || args.includes("-l")) {
  listSkills();
  process.exit(0);
}

let targetDir = null;
const targetIdx = args.indexOf("--target");
if (targetIdx !== -1 && args[targetIdx + 1]) {
  targetDir = path.resolve(args[targetIdx + 1]);
}

installSkills(targetDir);
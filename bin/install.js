#!/usr/bin/env node

/**
 * MY_SKILL Installer — Install TRAE skills to your AI agent platform.
 *
 * Usage:
 *   npx github:AVA-2568/MY_SKILL            # install to default platform
 *   npx github:AVA-2568/MY_SKILL --target  ./.trae-cn/skills   # custom target
 *   npx github:AVA-2568/MY_SKILL --list     # list all available skills
 *   npx github:AVA-2568/MY_SKILL --help     # show help
 */

const fs = require("fs");
const path = require("path");

const SKILLS_DIR = path.join(__dirname, "..", "skills");
const INDEX_PATH = path.join(__dirname, "..", "INDEX.yaml");

function getTargetDir() {
  // Default: TRAE skills directory
  const home = process.env.USERPROFILE || process.env.HOME;
  return path.join(home, ".trae-cn", "skills");
}

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
  if (!targetDir) targetDir = getTargetDir();

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

    // Remove existing
    if (fs.existsSync(dst)) {
      fs.rmSync(dst, { recursive: true, force: true });
    }

    // Copy recursively
    copyDirSync(src, dst);
    copied++;
    console.log(`  ✅ ${name}`);
  });

  // Copy INDEX.yaml
  if (fs.existsSync(INDEX_PATH)) {
    const idxDst = path.join(targetDir, "..", "INDEX.yaml");
    fs.copyFileSync(INDEX_PATH, idxDst);
    console.log(`  ✅ INDEX.yaml`);
  }

  console.log(`\n  ✨ Done! ${copied} skills installed.\n`);
  console.log(`  💡 Restart your AI agent to load the new skills.\n`);
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
  MY_SKILL — Personal TRAE Skill Library

  Usage:
    npx github:AVA-2568/MY_SKILL              Install all skills to default path
    npx github:AVA-2568/MY_SKILL --list        List available skills
    npx github:AVA-2568/MY_SKILL --target DIR  Install to custom directory
    npx github:AVA-2568/MY_SKILL --help        Show this help

  Default install path:
    Windows: %USERPROFILE%\\\\.trae-cn\\\\skills
    macOS/Linux: ~/.trae-cn/skills

  After install, restart your AI agent to load the new skills.
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
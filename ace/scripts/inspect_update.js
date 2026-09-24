#!/usr/bin/env node
'use strict';

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const KIT_ROOT = path.resolve(__dirname, '..', '..');
const MANIFEST_PATH = path.join(KIT_ROOT, 'ace', 'runtime-version.json');

function slash(value) {
  return value.replace(/\\/g, '/');
}

function isUnresolvedPlaceholder(value) {
  return typeof value === 'string' && /__[A-Z0-9_]+__/.test(value);
}

function safeRelative(relative) {
  if (typeof relative !== 'string' || !relative || path.isAbsolute(relative)) {
    throw new Error(`Unsafe manifest path: ${relative}`);
  }
  const normalized = slash(path.normalize(relative));
  if (normalized === '..' || normalized.startsWith('../') || normalized.includes('/../')) {
    throw new Error(`Unsafe manifest path: ${relative}`);
  }
  return normalized.replace(/\/$/, '');
}

function safePath(root, relative) {
  const clean = safeRelative(relative);
  const absolute = path.resolve(root, ...clean.split('/'));
  const fromRoot = path.relative(root, absolute);
  if (fromRoot.startsWith('..') || path.isAbsolute(fromRoot)) {
    throw new Error(`Path escapes root: ${relative}`);
  }
  let current = root;
  for (const segment of fromRoot.split(path.sep).filter(Boolean)) {
    current = path.join(current, segment);
    let stat;
    try {
      stat = fs.lstatSync(current);
    } catch (error) {
      if (error.code === 'ENOENT') break;
      throw error;
    }
    if (stat.isSymbolicLink()) {
      throw new Error(`Symbolic links are not inspected: ${slash(path.relative(root, current))}`);
    }
  }
  return absolute;
}

function compareSemver(left, right) {
  const parse = (value) => {
    const match = typeof value === 'string' && value.match(
      /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$/,
    );
    if (!match) return null;
    return {
      core: match.slice(1, 4).map(Number),
      prerelease: match[4] ? match[4].split('.') : [],
    };
  };
  const a = parse(left);
  const b = parse(right);
  if (!a || !b) return null;
  for (let index = 0; index < 3; index += 1) {
    if (a.core[index] !== b.core[index]) return a.core[index] > b.core[index] ? 1 : -1;
  }
  if (!a.prerelease.length || !b.prerelease.length) {
    return a.prerelease.length === b.prerelease.length ? 0 : (a.prerelease.length ? -1 : 1);
  }
  const length = Math.max(a.prerelease.length, b.prerelease.length);
  for (let index = 0; index < length; index += 1) {
    if (a.prerelease[index] === undefined) return -1;
    if (b.prerelease[index] === undefined) return 1;
    if (a.prerelease[index] === b.prerelease[index]) continue;
    const aNumeric = /^\d+$/.test(a.prerelease[index]);
    const bNumeric = /^\d+$/.test(b.prerelease[index]);
    if (aNumeric && bNumeric) return Number(a.prerelease[index]) > Number(b.prerelease[index]) ? 1 : -1;
    if (aNumeric !== bNumeric) return aNumeric ? -1 : 1;
    return a.prerelease[index] > b.prerelease[index] ? 1 : -1;
  }
  return 0;
}

function hashFile(file) {
  const content = fs.readFileSync(file, 'utf8').replace(/\r\n/g, '\n');
  return crypto.createHash('sha256').update(content, 'utf8').digest('hex');
}

function readJson(root, relative) {
  try {
    const file = safePath(root, relative);
    let stat;
    try {
      stat = fs.lstatSync(file);
    } catch (error) {
      if (error.code === 'ENOENT') return { exists: false };
      throw error;
    }
    if (!stat.isFile()) throw new Error(`${relative} is not a regular file`);
    return { exists: true, value: JSON.parse(fs.readFileSync(file, 'utf8')) };
  } catch (error) {
    return { exists: true, error: error.message };
  }
}

function listFiles(root, relative) {
  const base = safePath(root, relative);
  if (!fs.existsSync(base)) return [];
  if (!fs.statSync(base).isDirectory()) return [safeRelative(relative)];
  const files = [];
  const visit = (directory) => {
    const entries = fs.readdirSync(directory, { withFileTypes: true })
      .sort((left, right) => left.name.localeCompare(right.name));
    for (const entry of entries) {
      const absolute = path.join(directory, entry.name);
      const rel = slash(path.relative(root, absolute));
      if (entry.isSymbolicLink()) {
        files.push(`${rel} [symlink]`);
      } else if (entry.isDirectory()) {
        visit(absolute);
      } else if (entry.isFile()) {
        files.push(rel);
      }
    }
  };
  visit(base);
  return files;
}

function inspectMode(configResult, conflicts, normalization) {
  if (!configResult.exists) return 'unconfigured';
  if (configResult.error || !configResult.value || Array.isArray(configResult.value)) {
    conflicts.push({
      path: 'ace/config/project.json',
      reason: configResult.error || 'Configuration must be a JSON object.',
    });
    return 'unknown';
  }
  const config = configResult.value;
  if (!Object.prototype.hasOwnProperty.call(config, 'integration_mode')) {
    normalization.push({
      path: 'ace/config/project.json',
      field: 'integration_mode',
      required_value: 'embedded',
      reason: 'Legacy embedded configuration must declare its integration mode.',
    });
    return 'legacy_embedded';
  }
  if (config.integration_mode === 'embedded') return 'current_embedded';
  if (config.integration_mode !== 'mediated') {
    normalization.push({
      path: 'ace/config/project.json',
      field: 'integration_mode',
      required_value: 'embedded or mediated',
      reason: 'Unsupported integration mode.',
    });
    return 'unknown';
  }
  const canonicalAgents = Array.isArray(config.participating_agents)
    ? config.participating_agents : [];
  for (const [platformName, platform] of Object.entries(config.platforms || {}).sort()) {
    if (!platform || !platform.enabled) continue;
    const mapping = platform.canonical_to_runtime;
    const mappingIsObject = mapping && typeof mapping === 'object' && !Array.isArray(mapping);
    const mappingKeys = mappingIsObject ? Object.keys(mapping) : [];
    const mappingValues = mappingIsObject ? mappingKeys.map((agent) => mapping[agent]) : [];
    const validMapping = mappingIsObject
      && canonicalAgents.every((agent) => mappingKeys.includes(agent))
      && mappingKeys.every((agent) => canonicalAgents.includes(agent))
      && mappingValues.every((value) => typeof value === 'string'
        && value.trim() && !isUnresolvedPlaceholder(value))
      && new Set(mappingValues).size === mappingValues.length;
    if (!validMapping) {
      normalization.push({
        path: 'ace/config/project.json',
        field: `platforms.${platformName}.canonical_to_runtime`,
        required_value: 'exact, unique canonical-to-runtime worker mappings',
        reason: 'Mediated installations must map every participating worker exactly once.',
      });
    }
    const entries = platform.orchestrator_entrypoints;
    const validEntries = entries && typeof entries === 'object' && !Array.isArray(entries)
      && typeof entries.project === 'string' && entries.project.trim()
      && typeof entries.ace === 'string' && entries.ace.trim()
      && !isUnresolvedPlaceholder(entries.project) && !isUnresolvedPlaceholder(entries.ace)
      && entries.ace === `${entries.project}-ace`;
    if (!validEntries) {
      normalization.push({
        path: 'ace/config/project.json',
        field: `platforms.${platformName}.orchestrator_entrypoints`,
        required_value: 'project entrypoint and its -ace suffixed entrypoint',
        reason: 'Mediated installations require the ACE entrypoint to equal the project entrypoint plus -ace.',
      });
    } else if (validMapping && mappingValues.some(
      (runtime) => runtime === entries.project || runtime === entries.ace,
    )) {
      normalization.push({
        path: 'ace/config/project.json',
        field: `platforms.${platformName}.canonical_to_runtime`,
        required_value: 'worker mappings distinct from orchestrator entrypoints',
        reason: 'Mediated worker runtime IDs must not collide with either orchestrator entrypoint.',
      });
    }
  }
  return 'mediated';
}

function ownedFiles(manifest, mode) {
  const files = { ...(manifest.ownership?.kit_owned || {}) };
  const modeKey = mode === 'legacy_embedded' || mode === 'current_embedded'
    ? 'embedded'
    : (mode === 'mediated' ? 'mediated' : null);
  if (modeKey) Object.assign(files, manifest.ownership?.mode_specific?.[modeKey] || {});
  return files;
}

function inspect(targetRoot) {
  const manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf8'));
  const conflicts = [];
  const normalization = [];
  const configResult = readJson(targetRoot, 'ace/config/project.json');
  const mode = inspectMode(configResult, conflicts, normalization);
  const targetManifestResult = readJson(targetRoot, 'ace/runtime-version.json');
  const targetManifest = targetManifestResult.value;
  if (targetManifestResult.error) {
    conflicts.push({ path: 'ace/runtime-version.json', reason: targetManifestResult.error });
  }
  const manifestCompatible = targetManifestResult.exists
    && !targetManifestResult.error
    && targetManifest?.manifest_version === manifest.manifest_version;
  const installedHashes = manifestCompatible
    ? ownedFiles(targetManifest, mode)
    : {};
  let manifestState = 'missing';
  let versionRelation = 'unknown';
  if (targetManifestResult.exists && !targetManifestResult.error) {
    if (targetManifest?.manifest_version !== manifest.manifest_version) {
      manifestState = 'conflict';
      conflicts.push({
        path: 'ace/runtime-version.json',
        reason: `Manifest version mismatch: installed ${String(targetManifest?.manifest_version)}, kit ${String(manifest.manifest_version)}.`,
      });
    } else {
      const versionOrder = compareSemver(targetManifest.runtime_version, manifest.runtime_version);
      if (versionOrder === null) {
        manifestState = 'conflict';
        conflicts.push({
          path: 'ace/runtime-version.json',
          reason: `Runtime versions must be valid semantic versions: installed ${String(targetManifest.runtime_version)}, kit ${String(manifest.runtime_version)}.`,
        });
      } else if (versionOrder > 0) {
        versionRelation = 'newer_installed';
        manifestState = 'downgrade_blocked';
        conflicts.push({
          path: 'ace/runtime-version.json',
          reason: `Installed runtime ${targetManifest.runtime_version} is newer than kit ${manifest.runtime_version}; downgrade is blocked.`,
        });
      } else {
        versionRelation = versionOrder === 0 ? 'current' : 'older_installed';
        manifestState = versionOrder === 0 ? 'current' : 'update_available';
      }
    }
  } else if (targetManifestResult.error) {
    manifestState = 'conflict';
  }
  const kitOwned = [{
    path: manifest.manifest_path,
    state: manifestState,
    kit_sha256: null,
    target_sha256: null,
  }];

  for (const [relative, expectedHash] of Object.entries(ownedFiles(manifest, mode))
    .sort(([left], [right]) => left.localeCompare(right))) {
    let state;
    let targetHash = null;
    try {
      const target = safePath(targetRoot, relative);
      if (!fs.existsSync(target)) {
        state = 'missing';
      } else if (!fs.statSync(target).isFile()) {
        state = 'conflict';
        conflicts.push({ path: relative, reason: 'Expected a regular file.' });
      } else {
        targetHash = hashFile(target);
        if (targetHash === expectedHash) state = 'current';
        else if (!/^[a-f0-9]{64}$/i.test(installedHashes[relative] || '')) {
          state = 'unverified';
        } else if (installedHashes[relative] === targetHash) state = 'update_available';
        else {
          state = 'conflict';
          conflicts.push({
            path: relative,
            reason: targetManifest
              ? 'Kit-owned file differs from both installed and current versions.'
              : 'Kit-owned file differs and no installed manifest proves its provenance.',
          });
        }
      }
    } catch (error) {
      state = 'conflict';
      conflicts.push({ path: relative, reason: error.message });
    }
    kitOwned.push({
      path: relative,
      state,
      kit_sha256: expectedHash,
      target_sha256: targetHash,
    });
  }

  const managedMerge = manifest.ownership.managed_merge.map((relative) => {
    try {
      const target = safePath(targetRoot, relative);
      const kit = safePath(KIT_ROOT, relative);
      if (!fs.existsSync(target)) return { path: relative, state: 'missing' };
      if (!fs.statSync(target).isFile()) {
        conflicts.push({ path: relative, reason: 'Managed-merge path is not a regular file.' });
        return { path: relative, state: 'conflict' };
      }
      return {
        path: relative,
        state: fs.existsSync(kit) && hashFile(target) === hashFile(kit)
          ? 'current' : 'merge_required',
      };
    } catch (error) {
      conflicts.push({ path: relative, reason: error.message });
      return { path: relative, state: 'conflict' };
    }
  });

  const preservedInventory = (relative) => {
    try {
      return {
        path: relative,
        files: relative.endsWith('/') ? listFiles(targetRoot, relative) : (
          fs.existsSync(safePath(targetRoot, relative)) ? [safeRelative(relative)] : []
        ),
        action: 'preserve',
      };
    } catch (error) {
      conflicts.push({ path: relative, reason: error.message });
      return { path: relative, files: [], action: 'preserve' };
    }
  };
  const projectOwned = manifest.ownership.project_owned.map(preservedInventory);
  const kitOwnedPaths = new Set(Object.keys(manifest.ownership.kit_owned));
  const protectedData = manifest.ownership.protected_runtime_data.map((relative) => {
    const inventory = preservedInventory(relative);
    inventory.files = inventory.files.filter((file) => !kitOwnedPaths.has(file));
    return inventory;
  });
  conflicts.sort((left, right) => left.path.localeCompare(right.path)
    || left.reason.localeCompare(right.reason));
  normalization.sort((left, right) => left.field.localeCompare(right.field));
  return {
    inspection_version: 1,
    kit_root: KIT_ROOT,
    target_root: targetRoot,
    kit_runtime_version: manifest.runtime_version,
    installed_runtime_version: targetManifest?.runtime_version || null,
    version_relation: versionRelation,
    update_blocked: versionRelation === 'newer_installed',
    installation_mode: mode,
    write_performed: false,
    kit_owned: kitOwned,
    managed_merge: managedMerge,
    project_owned: projectOwned,
    protected_runtime_data: protectedData,
    conflicts,
    required_config_normalization: normalization,
  };
}

function targetArgument(args) {
  const index = args.indexOf('--target');
  const value = index === -1 ? args[0] : args[index + 1];
  if (!value || value.startsWith('--')) {
    throw new Error('Usage: node ace/scripts/inspect_update.js --target <TARGET_ROOT>');
  }
  const root = path.resolve(value);
  if (!fs.existsSync(root) || !fs.statSync(root).isDirectory()) {
    throw new Error(`Target root is not a directory: ${root}`);
  }
  if (fs.lstatSync(root).isSymbolicLink()) {
    throw new Error(`Target root must not be a symbolic link: ${root}`);
  }
  return root;
}

function run(args = process.argv.slice(2)) {
  const report = inspect(targetArgument(args));
  process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  return report;
}

if (require.main === module) {
  try {
    run();
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}

module.exports = { inspect, run };

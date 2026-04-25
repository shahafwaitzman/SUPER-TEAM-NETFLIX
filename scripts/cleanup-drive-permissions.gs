/**
 * cleanup-drive-permissions.gs
 *
 * Apps Script for Super Team Academy.
 * Removes all PERSONAL (user) permissions from a Drive folder + all sub-folders + files.
 * Keeps the OWNER and "Anyone with the link" permissions intact.
 *
 * USAGE:
 *   1. Open https://script.google.com → New Project
 *   2. Paste this entire file
 *   3. Replace ROOT_FOLDER_ID below with your academy folder ID
 *      (from URL: drive.google.com/drive/folders/THIS_PART_HERE)
 *   4. Click Save
 *   5. Run auditAccess() FIRST → see who would be removed (dry-run)
 *   6. If list looks correct → run cleanAccess() to actually remove
 *   7. Authorize when prompted
 */

const ROOT_FOLDER_ID = 'PASTE_YOUR_ACADEMY_FOLDER_ID_HERE';

// ════════════════════════════════════════════
// auditAccess — DRY RUN (does NOT remove anything)
// ════════════════════════════════════════════
function auditAccess() {
  const folder = DriveApp.getFolderById(ROOT_FOLDER_ID);
  const stats = { folders: 0, files: 0, perms: 0, users: new Set() };
  Logger.log('=== AUDIT START — folder: ' + folder.getName() + ' ===');
  walkAndAudit_(folder, stats, 0);
  Logger.log('=== AUDIT COMPLETE ===');
  Logger.log('Folders scanned: ' + stats.folders);
  Logger.log('Files scanned:   ' + stats.files);
  Logger.log('Personal permissions found: ' + stats.perms);
  Logger.log('Unique users with access:   ' + stats.users.size);
  Logger.log('--- Users that WILL be removed if you run cleanAccess(): ---');
  Array.from(stats.users).sort().forEach(email => Logger.log('  · ' + email));
}

function walkAndAudit_(folder, stats, depth) {
  stats.folders++;
  countPerms_(folder, stats);
  // Files
  const files = folder.getFiles();
  while (files.hasNext()) {
    const file = files.next();
    stats.files++;
    countPerms_(file, stats);
  }
  // Subfolders
  const subs = folder.getFolders();
  while (subs.hasNext()) {
    walkAndAudit_(subs.next(), stats, depth + 1);
  }
}

function countPerms_(item, stats) {
  // Editors + Viewers (skip owner)
  const editors = item.getEditors();
  const viewers = item.getViewers();
  editors.forEach(u => { stats.perms++; stats.users.add(u.getEmail()); });
  viewers.forEach(u => { stats.perms++; stats.users.add(u.getEmail()); });
}

// ════════════════════════════════════════════
// cleanAccess — REAL run (removes personal permissions)
// ════════════════════════════════════════════
function cleanAccess() {
  const folder = DriveApp.getFolderById(ROOT_FOLDER_ID);
  const stats = { folders: 0, files: 0, removed: 0, errors: 0 };
  Logger.log('=== CLEAN START — folder: ' + folder.getName() + ' ===');
  walkAndClean_(folder, stats, 0);
  Logger.log('=== CLEAN COMPLETE ===');
  Logger.log('Folders processed: ' + stats.folders);
  Logger.log('Files processed:   ' + stats.files);
  Logger.log('Permissions removed: ' + stats.removed);
  Logger.log('Errors: ' + stats.errors);
  Logger.log('Owner + "Anyone with the link" permissions are preserved.');
}

function walkAndClean_(folder, stats, depth) {
  stats.folders++;
  removePerms_(folder, stats);
  const files = folder.getFiles();
  while (files.hasNext()) {
    const file = files.next();
    stats.files++;
    removePerms_(file, stats);
  }
  const subs = folder.getFolders();
  while (subs.hasNext()) {
    walkAndClean_(subs.next(), stats, depth + 1);
  }
}

function removePerms_(item, stats) {
  // Remove all editors
  const editors = item.getEditors();
  editors.forEach(u => {
    try {
      item.removeEditor(u.getEmail());
      stats.removed++;
    } catch (e) {
      stats.errors++;
      Logger.log('  ! Could not remove editor ' + u.getEmail() + ' from ' + item.getName() + ': ' + e.message);
    }
  });
  // Remove all viewers
  const viewers = item.getViewers();
  viewers.forEach(u => {
    try {
      item.removeViewer(u.getEmail());
      stats.removed++;
    } catch (e) {
      stats.errors++;
      Logger.log('  ! Could not remove viewer ' + u.getEmail() + ' from ' + item.getName() + ': ' + e.message);
    }
  });
}

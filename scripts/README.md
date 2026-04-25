# Drive Permissions Cleanup

Removes all personal (user-specific) permissions from the Academy Drive folder.
Keeps Owner + "Anyone with the link" intact.

## How to use

1. Open https://script.google.com → **New project**
2. Delete the default `Code.gs` content
3. Paste contents of [`cleanup-drive-permissions.gs`](./cleanup-drive-permissions.gs)
4. **IMPORTANT** — replace `PASTE_YOUR_ACADEMY_FOLDER_ID_HERE` with your real folder ID
   - Get it from the Drive URL: `drive.google.com/drive/folders/THIS_PART`
5. Click **Save** (💾) → name the project (e.g. "Drive Cleanup")

### Step 1: AUDIT (dry-run, removes nothing)
- Top toolbar → function dropdown → select **`auditAccess`**
- Click **Run** ▶
- First time only: authorize ("Allow") — needs Drive permissions
- Open **View → Logs** (or Cmd+Enter) to see results

You'll see:
```
Folders scanned: 12
Files scanned: 78
Personal permissions found: 45
Unique users with access: 18
--- Users that WILL be removed: ---
  · arikp1512@gmail.com
  · asoulininbal@gmail.com
  ...
```

### Step 2: CLEAN (real, removes!)
- Only after you verify the list above
- Function dropdown → **`cleanAccess`** → **Run** ▶
- Wait for "CLEAN COMPLETE" in logs

## What is preserved
- ✅ Owner (you) — always kept
- ✅ "Anyone with the link" — always kept
- ✅ Domain-wide permissions (if any) — kept
- ❌ Specific user invites — REMOVED

## Reverting
- Cannot undo individual user removals
- But anyone with the link still has full access (Viewer role)
- If you need to restore specific user as Editor → invite them again manually

## Limitations
- May time out if folder has 1000+ items (Apps Script has 6-min execution limit)
- For very large folders, run cleanAccess() multiple times

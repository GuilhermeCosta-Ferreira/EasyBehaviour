import Database from '@tauri-apps/plugin-sql';
import { open, save } from '@tauri-apps/plugin-dialog';
import {
  BaseDirectory,
  mkdir,
  readFile,
  writeFile,
  remove,
} from '@tauri-apps/plugin-fs';

const IMPORT_DIR = 'imported_dbs'; // folder created to where the db will live
const WORKING_DB = `${IMPORT_DIR}/working.sqlite`; // full path for the imported file

let dbInstance = null;



/**
 * Lets the user pick a SQLite file, copies it into AppData, and returns the internal path.
 * The promise is needed for an async function
 * @returns {Promise<string|null>}
 */
export async function importDbFromUserFile() {
  // 1. user selects a file
  const selected = await open({
    title: 'Select SQLite database',
    multiple: false,
    filters: [{ name: 'SQLite DB', extensions: ['db', 'sqlite', 'sqlite3'] }],
  });

  // 2. If the user gives up on importing
  if (!selected || Array.isArray(selected)) return null;

  // 3. ensure internal dir exists
  await mkdir(IMPORT_DIR, { baseDir: BaseDirectory.AppData, recursive: true });

  // 4. read chosen file (absolute path) -> write to appdata copy
  // Dialog open() adds selected paths to the fs scope, so this read is permitted.
  const bytes = await readFile(selected);
  await writeFile(WORKING_DB, bytes, { baseDir: BaseDirectory.AppData });

  // 5. reset any open connection
  dbInstance = await deselectWorkingDb();

  return WORKING_DB;
}



/**
 * Gets (and caches) the Database instance for the internal working DB.
 * @returns {Promise<Database>}
 */
export async function getWorkingDb() {
  if (dbInstance) return dbInstance;

  // This opens the DB file stored under AppData.
  // Note: plugin-sql expects a relative path (it resolves internally).
  dbInstance = await Database.load(`sqlite:${WORKING_DB}`);
  return dbInstance;
}



/**
 * Exports the internal working DB to a user-chosen destination.
 * @returns {Promise<string|null>}
 */
export async function exportWorkingDb() {
  // 1. Pick destination path
  const dest = await save({
    title: 'Export database as…',
    defaultPath: 'export.sqlite',
    filters: [{ name: 'SQLite DB', extensions: ['db', 'sqlite', 'sqlite3'] }],
  });

  // 2. Cancel if canceled
  if (!dest) return null;

  // IMPORTANT: ensure DB is not mid-write. If you’re doing lots of writes,
  // consider a "close DB" step (depending on plugin capabilities).
  const bytes = await readFile(WORKING_DB, { baseDir: BaseDirectory.AppData });
  await writeFile(dest, bytes);

  return dest;
}



/**
 * De-selects the working DB:
 * - closes the current connection (if open)
 * - clears the cached instance
 * - optionally deletes the working.sqlite file
 *
 * @param {{ deleteWorkingFile?: boolean }} opts
 * @returns {Promise<void>}
 */
export async function deselectWorkingDb(opts = {}) {
  const { deleteWorkingFile = false } = opts;

  // 1) Close active connection if it exists
  if (dbInstance) {
    try {
      // Recommended: make sure pending WAL/pages are flushed first (optional).
      // If you don't use WAL, this is harmless.
      try {
        await dbInstance.execute('PRAGMA wal_checkpoint(FULL);');
      } catch {
        // ignore (some builds/modes may not support WAL checkpointing)
      }

      await dbInstance.close(); // <- the important part
    } finally {
      dbInstance = null;
    }
  }

  // 2) Optionally remove the working DB file from AppData
  if (deleteWorkingFile) {
    try {
      await remove(WORKING_DB, { baseDir: BaseDirectory.AppData });
    } catch {
      // ignore if it doesn't exist
    }
  }
}

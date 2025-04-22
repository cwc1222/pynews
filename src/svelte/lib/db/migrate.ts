import type { D1Database } from '@cloudflare/workers-types';
import { readFileSync, readdirSync, writeFileSync } from 'fs';
import { createHash } from 'crypto';
import path from 'path';

interface Migration {
	version: number;
	description: string;
	checksum: string;
}

async function getCurrentVersion(db: D1Database): Promise<number> {
	try {
		const result = await db
			.prepare('SELECT MAX(version) as version FROM schema_versions')
			.first<{ version: number }>();
		return result?.version || 0;
	} catch {
		return 0; // Table doesn't exist yet
	}
}

function calculateChecksum(sql: string): string {
	return createHash('sha256').update(sql).digest('hex');
}

async function applyMigration(db: D1Database, version: number, sql: string, description: string) {
	const checksum = calculateChecksum(sql);

	// Start transaction
	await db.prepare('BEGIN TRANSACTION').run();

	try {
		// Apply migration
		await db.batch([
			db.prepare(sql),
			db
				.prepare('INSERT INTO schema_versions (version, description, checksum) VALUES (?, ?, ?)')
				.bind(version, description, checksum)
		]);

		await db.prepare('COMMIT').run();
		console.log(`Applied migration ${version}: ${description}`);
	} catch (error) {
		await db.prepare('ROLLBACK').run();
		throw error;
	}
}

export async function migrate(db: D1Database) {
	const currentVersion = await getCurrentVersion(db);
	const migrationsDir = path.join(__dirname, 'migrations');

	// Get all migration files
	const migrations = readdirSync(migrationsDir)
		.filter((file) => file.endsWith('.sql'))
		.map((file) => {
			const [version] = file.match(/^\d+/)!;
			return {
				version: parseInt(version),
				path: path.join(migrationsDir, file),
				description: file.replace(/^\d+_/, '').replace('.sql', '')
			};
		})
		.sort((a, b) => a.version - b.version)
		.filter((m) => m.version > currentVersion);

	// Apply pending migrations in order
	for (const migration of migrations) {
		const sql = readFileSync(migration.path, 'utf-8');
		await applyMigration(db, migration.version, sql, migration.description);
	}
}

// Example of how to add a new migration
export async function createMigration(description: string) {
	const migrationsDir = path.join(__dirname, 'migrations');
	const files = readdirSync(migrationsDir).filter((f) => f.endsWith('.sql'));
	const lastVersion = Math.max(...files.map((f) => parseInt(f.match(/^\d+/)![0])), 0);
	const newVersion = lastVersion + 1;
	const filename = `${String(newVersion).padStart(3, '0')}_${description}.sql`;

	const template = `-- Migration ${newVersion}: ${description}

-- Write your SQL here
`;

	const filePath = path.join(migrationsDir, filename);
	writeFileSync(filePath, template);
	console.log(`Created new migration file: ${filename}`);
}

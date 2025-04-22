import { migrate } from './migrate';
import type { D1Database } from '@cloudflare/workers-types';

interface Env {
	DB: D1Database;
	DEPLOY_HOOK_SECRET: string;
}

async function generateSignature(payload: string, secret: string): Promise<string> {
	const encoder = new TextEncoder();
	const key = await crypto.subtle.importKey(
		'raw',
		encoder.encode(secret),
		{ name: 'HMAC', hash: 'SHA-256' },
		false,
		['sign']
	);

	const signature = await crypto.subtle.sign('HMAC', key, encoder.encode(payload));

	return Array.from(new Uint8Array(signature))
		.map((b) => b.toString(16).padStart(2, '0'))
		.join('');
}

export default {
	async fetch(request: Request, env: Env): Promise<Response> {
		// Only allow POST requests to /__migrate
		if (request.method !== 'POST' || new URL(request.url).pathname !== '/__migrate') {
			return new Response('Not found', { status: 404 });
		}

		// Verify deployment hook signature
		const signature = request.headers.get('CF-Webhook-Signature');
		if (!signature || !env.DEPLOY_HOOK_SECRET) {
			return new Response('Unauthorized', { status: 401 });
		}

		try {
			// Verify the request is from Cloudflare deployment
			const payload = await request.text();
			const expectedSignature = await generateSignature(payload, env.DEPLOY_HOOK_SECRET);

			if (signature !== expectedSignature) {
				return new Response('Invalid signature', { status: 401 });
			}

			// Run migrations
			await migrate(env.DB);
			return new Response('Migrations completed successfully', { status: 200 });
		} catch (error: unknown) {
			console.error('Migration failed:', error);
			const errorMessage = error instanceof Error ? error.message : 'Unknown error';
			return new Response(`Migration failed: ${errorMessage}`, { status: 500 });
		}
	}
};

import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { generateToken, sendConfirmationEmail } from '$lib/email';

interface SubscribeRequest {
	email: string;
}

export const POST: RequestHandler = async ({ request, platform }) => {
	const env = platform?.env as Env;
	try {
		const data = (await request.json()) as SubscribeRequest;
		const { email } = data;

		if (!email || !email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
			return json({ error: 'Invalid email address' }, { status: 400 });
		}

		if (!env.DB) {
			throw new Error('Database not available');
		}

		// Check if email already exists
		const existing = await env.DB.prepare('SELECT email FROM subscribers WHERE email = ?')
			.bind(email)
			.first<{ email: string }>();

		if (existing) {
			return json({ error: 'Email already registered' }, { status: 400 });
		}

		const confirmationToken = generateToken();

		// Insert new subscriber
		await env.DB.prepare('INSERT INTO subscribers (email, confirmation_token) VALUES (?, ?)')
			.bind(email, confirmationToken)
			.run();

		const workerUrl = new URL(request.url);
		await sendConfirmationEmail(email, confirmationToken, workerUrl);

		return json({ success: true });
	} catch (error) {
		console.error('Subscription error:', error);
		return json({ error: 'Failed to subscribe' }, { status: 500 });
	}
};

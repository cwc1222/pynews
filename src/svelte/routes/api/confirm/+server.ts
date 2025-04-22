import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ url, platform }) => {
	try {
		const token = url.searchParams.get('token');
		const email = url.searchParams.get('email');

		if (!token || !email || !platform?.env?.DB) {
			return json({ error: 'Invalid confirmation link' }, { status: 400 });
		}

		// Update subscriber status
		const result = await platform.env.DB.prepare(
			`
                UPDATE subscribers
                SET status = 'confirmed'
                WHERE email = ?
                AND confirmation_token = ?
                AND status = 'pending'
                RETURNING *
            `
		)
			.bind(email, token)
			.first<App.SubscriberResponse>();

		if (!result) {
			return json({ error: 'Invalid or expired confirmation link' }, { status: 400 });
		}

		return json({ success: true });
	} catch (error) {
		console.error('Confirmation error:', error);
		return json({ error: 'Failed to confirm subscription' }, { status: 500 });
	}
};

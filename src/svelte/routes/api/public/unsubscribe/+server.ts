import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const DELETE: RequestHandler = async ({ url, platform }) => {
	return json({ success: true });
	/*
	try {
		const token = url.searchParams.get('token');
		const email = url.searchParams.get('email');

		if (!token || !email || !platform?.env?.DB) {
			return json({ error: 'Invalid unsubscribe link' }, { status: 400 });
		}

		const result = await platform.env.DB.prepare(
			`
                DELETE FROM subscribers
                WHERE email = ?
                AND confirmation_token = ?
                RETURNING *
            `
		)
			.bind(email, token)
			.first<App.SubscriberResponse>();

		if (!result) {
			return json({ error: 'Invalid unsubscribe link' }, { status: 400 });
		}

		return json({ success: true });
	} catch (error) {
		console.error('Unsubscribe error:', error);
		return json({ error: 'Failed to unsubscribe' }, { status: 500 });
	}
	*/
};

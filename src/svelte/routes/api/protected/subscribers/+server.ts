import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ url, platform }) => {
	/*
	try {
		const token = url.searchParams.get('token');

		if (!platform?.env?.API_TOKEN || !token || token !== platform.env.API_TOKEN) {
			return json({ error: 'Unauthorized' }, { status: 401 });
		}

		const subscribers = await platform.env.DB.prepare(
			'SELECT email FROM subscribers WHERE status = ?'
		)
			.bind('confirmed')
			.all<{ email: string }>();

		return json({ subscribers: subscribers.results });
	} catch (error) {
		console.error('Failed to fetch subscribers:', error);
		return json({ error: 'Failed to fetch subscribers' }, { status: 500 });
	}
	*/
	return json({ success: true });
};

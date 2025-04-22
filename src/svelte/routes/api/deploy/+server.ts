import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ request, platform }) => {
	try {
		const token = request.headers.get('x-deploy-hook');

		if (!platform?.env?.DEPLOY_HOOK_SECRET || !token || token !== platform.env.DEPLOY_HOOK_SECRET) {
			return json({ error: 'Unauthorized' }, { status: 401 });
		}

		const subscribers = await platform.env.DB.prepare(
			'SELECT email FROM subscribers WHERE status = ?'
		)
			.bind('confirmed')
			.all<{ email: string }>();

		return json({ message: 'Deploy hook received', subscribers: subscribers.results });
	} catch (error) {
		console.error('Failed to process deploy hook:', error);
		return json({ error: 'Failed to process deploy hook' }, { status: 500 });
	}
};

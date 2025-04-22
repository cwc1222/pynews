/// <reference types="@sveltejs/kit" />
import type { D1Database } from '@cloudflare/workers-types';

// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare global {
	namespace App {
		interface Platform {
			env: {
				DB: D1Database;
				API_TOKEN: string;
				PUBLIC_APP_URL: string;
				GMAIL_SENDER: string;
				DEPLOY_HOOK_SECRET: string;
			};
		}

		interface Locals {}
		interface PageData {}
		interface Error {}

		interface SubscriberResponse {
			email: string;
			status: 'pending' | 'confirmed';
			confirmation_token: string;
			created_at: string;
			updated_at: string;
		}

		interface ApiResponse {
			success?: boolean;
			error?: string;
		}
	}
}

export {};

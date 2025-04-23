/// <reference types="@sveltejs/kit" />

// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare global {
	namespace App {
		interface Platform {}
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

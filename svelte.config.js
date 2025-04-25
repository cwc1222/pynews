import adapter from '@sveltejs/adapter-cloudflare';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter(),
		alias: {
			$lib: 'src/svelte/lib'
		},
		files: {
			hooks: {
				server: 'src/svelte/hooks.server',
				client: 'src/svelte/hooks.client'
			},
			lib: 'src/svelte/lib',
			params: 'src/svelte/params',
			routes: 'src/svelte/routes',
			serviceWorker: 'src/svelte/service-worker',
			appTemplate: 'src/svelte/app.html'
		}
	}
};

export default config;

import adapter from '@sveltejs/adapter-cloudflare';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

const config = {
	preprocess: vitePreprocess(),
	kit: {
		adapter: adapter(),
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

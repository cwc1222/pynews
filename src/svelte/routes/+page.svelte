<script lang="ts">
	import { t, locale } from '$lib/i18n';

	let email = '';
	let subscribed = false;
	let error = '';
	let loading = false;

	interface ApiResponse {
		error?: string;
		success?: boolean;
	}

	async function handleSubmit() {
		if (!email) {
			error = t('errors.emailRequired', $locale);
			return;
		}

		if (!email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
			error = t('errors.emailInvalid', $locale);
			return;
		}

		loading = true;
		error = '';

		try {
			const response = await fetch('/api/public/subscribe', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ email })
			});

			const data = (await response.json()) as ApiResponse;

			if (!response.ok) {
				throw new Error(data.error || t('errors.generic', $locale));
			}

			subscribed = true;
		} catch (err) {
			error = err instanceof Error ? err.message : t('errors.generic', $locale);
		} finally {
			loading = false;
		}
	}
</script>

<div class="flex min-h-screen flex-col items-center justify-center bg-gray-900 p-4 text-white">
	<div class="flex flex-col items-center">
		<img
			src="/logo.webp"
			alt="Logo"
			class="mb-4 h-32 w-32 rounded-full border-4 border-gray-200 object-contain"
		/>
		<h1 class="mb-8 text-2xl font-bold text-white">{t('title', $locale)}</h1>
	</div>

	<div class="w-full max-w-md rounded-lg bg-gray-800 p-8 shadow-md">
		<h1 class="mb-6 text-center text-2xl font-bold">
			{t('subscribe.heading', $locale)}
		</h1>

		{#if subscribed}
			<div class="mb-4 text-center text-green-400">
				{t('subscribe.success', $locale)}
			</div>
		{:else}
			<form on:submit|preventDefault={handleSubmit} class="space-y-4">
				<div>
					<label for="email" class="mb-1 block text-sm font-medium text-gray-300">
						{t('subscribe.emailLabel', $locale)}
					</label>
					<input
						type="email"
						id="email"
						bind:value={email}
						placeholder={t('subscribe.emailPlaceholder', $locale)}
						class="w-full rounded-md border bg-gray-700 px-4 py-2 text-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
						disabled={loading}
					/>
				</div>

				{#if error}
					<div class="text-sm text-red-400">{error}</div>
				{/if}

				<button
					type="submit"
					class="w-full rounded-md bg-blue-600 px-4 py-2 text-white transition duration-200 hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
					disabled={loading}
				>
					{loading ? t('subscribe.buttonLoading', $locale) : t('subscribe.button', $locale)}
				</button>
			</form>
		{/if}

		<p class="mt-4 text-center text-sm text-gray-400">
			{t('subscribe.description', $locale)}
		</p>
	</div>
</div>

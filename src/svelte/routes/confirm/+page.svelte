<script lang="ts">
	import { onMount } from 'svelte';

	export let data;
	let status: 'loading' | 'success' | 'error' = 'loading';
	let message = '';

	interface ApiResponse {
		error?: string;
		success?: boolean;
	}

	onMount(async () => {
		try {
			const token = data.searchParams.get('token');
			const email = data.searchParams.get('email');

			if (!token || !email) {
				throw new Error('Invalid confirmation link');
			}

			const response = await fetch(`/api/confirm?email=${email}&token=${token}`, {
				method: 'POST'
			});

			const result = (await response.json()) as ApiResponse;

			if (!response.ok) {
				throw new Error(result.error || 'Failed to confirm subscription');
			}

			status = 'success';
			message = 'Your subscription has been confirmed! You will start receiving news updates soon.';
		} catch (err) {
			status = 'error';
			message = err instanceof Error ? err.message : 'Something went wrong. Please try again.';
		}
	});
</script>

<div class="flex min-h-screen flex-col items-center justify-center bg-gray-900 p-4 text-white">
	<img src="/logo.webp" alt="Logo" class="mb-8 h-32 w-32 object-contain" />

	<div class="w-full max-w-md rounded-lg bg-gray-800 p-8 text-center shadow-md">
		<h1 class="mb-6 text-2xl font-bold">Email Confirmation</h1>

		{#if status === 'loading'}
			<div class="text-blue-400">Confirming your subscription...</div>
		{:else if status === 'success'}
			<div class="text-green-400">
				{message}
			</div>
		{:else}
			<div class="text-red-400">
				{message}
			</div>
		{/if}

		<a href="/" class="mt-6 inline-block text-blue-400 hover:text-blue-300"> Return to Homepage </a>
	</div>
</div>

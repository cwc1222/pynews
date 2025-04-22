<script lang="ts">
	import '../app.css';
	import { waitLocale } from 'svelte-i18n';
	import { onMount } from 'svelte';
	import '../lib/i18n';

	let ready = false;

	onMount(async () => {
		await waitLocale();
		ready = true;
	});
</script>

{#if ready}
	<slot />
{/if}

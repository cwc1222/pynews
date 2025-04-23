<script lang="ts">
	import '../app.css';
	import { locale, getAvailableLocales, type Locale } from '$lib/i18n';
	// import { onMount } from 'svelte';

	const languages = getAvailableLocales();
	const LANGUAGE_KEY = 'preferred-language';
	
	// Map browser language codes to our locale codes
	const browserLangMap: Record<string, Locale> = {
		'en': 'en-US',
		'es': 'es-PY',
		'zh': 'zh-TW'
	};

	// Initialize language preference
	if (typeof window !== 'undefined') {
		const cachedLanguage = localStorage.getItem(LANGUAGE_KEY) as Locale | null;
		
		if (cachedLanguage && Object.values(browserLangMap).includes(cachedLanguage)) {
			locale.set(cachedLanguage);
		} else {
			const browserLang = navigator.language.split('-')[0].toLowerCase();
			locale.set(browserLangMap[browserLang] || 'en-US');
		}
	}

	// Subscribe to locale changes to save them to localStorage
	locale.subscribe((value) => {
		if (typeof window !== 'undefined') {
			localStorage.setItem(LANGUAGE_KEY, value);
		}
	});
</script>

<div class="relative">
	<div class="absolute top-4 right-4">
		<select
			bind:value={$locale}
			class="rounded-md border border-gray-700 bg-gray-800 px-3 py-1 text-white"
		>
			{#each languages as lang}
				<option value={lang.code}>{lang.name}</option>
			{/each}
		</select>
	</div>

	<slot />
</div>

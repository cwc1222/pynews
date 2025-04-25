import type { Writable } from 'svelte/store';
import { writable } from 'svelte/store';

// Import translations
import en from './locales/en-US.json';
import es from './locales/es-PY.json';
import zh from './locales/zh-TW.json';

export type Locale = 'en-US' | 'es-PY' | 'zh-TW';
export type Translations = typeof en;

const translations: Record<Locale, Translations> = {
	'en-US': en,
	'es-PY': es,
	'zh-TW': zh
};

export const locale: Writable<Locale> = writable('en-US');

export function t(key: string, locale: Locale = 'en-US'): string {
	const keys = key.split('.');
	let value: any = translations[locale];

	for (const k of keys) {
		if (value === undefined) {
			// Fallback to English if translation is missing
			value = translations['en-US'];
			for (const fallbackKey of keys) {
				value = value[fallbackKey];
				if (value === undefined) return key;
			}
			return value;
		}
		value = value[k];
	}

	return value || key;
}

export function getAvailableLocales(): { code: Locale; name: string }[] {
	return [
		{ code: 'en-US', name: 'English' },
		{ code: 'es-PY', name: 'Español' },
		{ code: 'zh-TW', name: '繁體中文' }
	];
}

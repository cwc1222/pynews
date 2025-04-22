import { addMessages, init } from 'svelte-i18n';

// Import translations
import en from './locales/en-US.json';
import es from './locales/es-PY.json';
import zh from './locales/zh-TW.json';

// Add messages
addMessages('en-US', en);
addMessages('es-PY', es);
addMessages('zh-TW', zh);

// Initialize with default locale
init({
	fallbackLocale: 'en-US',
	initialLocale: 'en-US'
});

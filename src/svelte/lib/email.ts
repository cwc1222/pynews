/// <reference types="@sveltejs/kit" />

import crypto from 'crypto';

export function generateToken(): string {
	// Use Web Crypto API instead of Node's crypto
	const array = new Uint8Array(32);
	crypto.getRandomValues(array);
	return Array.from(array)
		.map((b) => b.toString(16).padStart(2, '0'))
		.join('');
}

export async function sendConfirmationEmail(email: string, token: string, workerUrl: URL) {
	const confirmUrl = `${workerUrl.href}/api/confirm?email=${encodeURIComponent(email)}&token=${token}`;
	const unsubscribeUrl = `${workerUrl.href}/api/unsubscribe?email=${encodeURIComponent(email)}&token=${token}`;

	const html = `
        <h1>Welcome to PyNews!</h1>
        <p>Please click the link below to confirm your subscription:</p>
        <p><a href="${confirmUrl}">Confirm Subscription</a></p>
        <p>If you didn't request this subscription, you can ignore this email or <a href="${unsubscribeUrl}">unsubscribe</a>.</p>
    `;

	console.log(html);
}

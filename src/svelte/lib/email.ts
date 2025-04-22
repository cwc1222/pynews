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

interface EmailPlatform {
	env: {
		PUBLIC_APP_URL: string;
		GMAIL_SENDER: string;
	};
}

export async function sendConfirmationEmail(email: string, token: string, platform: EmailPlatform) {
	if (!platform?.env?.PUBLIC_APP_URL || !platform?.env?.GMAIL_SENDER) {
		throw new Error('Missing required environment variables');
	}

	const confirmUrl = `${platform.env.PUBLIC_APP_URL}/api/confirm?email=${encodeURIComponent(email)}&token=${token}`;
	const unsubscribeUrl = `${platform.env.PUBLIC_APP_URL}/api/unsubscribe?email=${encodeURIComponent(email)}&token=${token}`;

	const html = `
        <h1>Welcome to PyNews!</h1>
        <p>Please click the link below to confirm your subscription:</p>
        <p><a href="${confirmUrl}">Confirm Subscription</a></p>
        <p>If you didn't request this subscription, you can ignore this email or <a href="${unsubscribeUrl}">unsubscribe</a>.</p>
    `;

	// Send via Mailchannels
	const response = await fetch('https://api.mailchannels.net/tx/v1/send', {
		method: 'POST',
		headers: {
			'content-type': 'application/json'
		},
		body: JSON.stringify({
			personalizations: [
				{
					to: [{ email, name: email.split('@')[0] }]
				}
			],
			from: {
				email: platform.env.GMAIL_SENDER,
				name: 'PyNews'
			},
			subject: 'Confirm your subscription to PyNews',
			content: [
				{
					type: 'text/html',
					value: html
				}
			]
		})
	});

	if (!response.ok) {
		const error = await response.text();
		throw new Error(`Failed to send email: ${error}`);
	}
}

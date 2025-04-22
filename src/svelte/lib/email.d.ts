import type { Platform } from '../app';

export interface EmailPlatform extends Platform {}

export function generateToken(): string;
export function sendConfirmationEmail(
	email: string,
	token: string,
	platform: EmailPlatform
): Promise<void>;

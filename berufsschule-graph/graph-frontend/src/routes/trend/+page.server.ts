import { PUBLIC_URL_API } from "$env/static/public";
import { safeFetch } from "$lib/fetch";
import { error as svelteError } from "@sveltejs/kit";
import type { Channel } from "$application";

export async function load({ fetch }) {
	const [channels, error] = await safeFetch<Channel[]>({
		fn: fetch,
		url: `${PUBLIC_URL_API}/channels`,
		json: true
	});

	if (error) {
		throw svelteError(error.status, error.stack);
	}

	return { channels };
}
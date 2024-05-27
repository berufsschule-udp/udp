import { error as svelteError, json } from "@sveltejs/kit";
import { PUBLIC_URL_API } from "$env/static/public";
import { URL_BACKEND } from "$env/static/private";
import { safeFetch } from "$lib/fetch";

export async function handle({ event, resolve }) {
	if (!event.url.pathname.startsWith(PUBLIC_URL_API)) {
		return await resolve(event);
	}

	const [response, error] = await safeFetch({
		fn: fetch,
		url: `${URL_BACKEND}${event.url.pathname}${event.url.search}`,
		json: true
	});

	if (error) {
		svelteError(error.status, error.stack);
	}

	return json(response);
}
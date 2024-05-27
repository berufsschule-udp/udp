export class FetchError extends Error {
	status: number;

	constructor(status: number, message: string) {
		super(message);
		this.status = status;
	}
}

export async function safeFetch<T = Response>(args: {
	fn: typeof fetch,
	url: string,
	json?: boolean
}): Promise<[T, null] | [null, FetchError]> {
	try {
		const response = await args.fn(args.url);

		if (response.status >= 300) {
			const error = new FetchError(response.status, response.statusText);
			return [null, error];
		}

		return [args.json ? await response.json() : response, null];
	} catch (error: any) {
		const status = error?.status ?? 500;
		const message = error?.message ?? "Internal server error.";

		return [null, new FetchError(status, message)];
	}
}
import adapter from "@sveltejs/adapter-auto";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

/** @type {import("@sveltejs/kit").Config} */
export default {
	kit: {
		adapter: adapter(),
		alias: {
			"$application": "src/app.d"
		}
	},
	preprocess: vitePreprocess()
};
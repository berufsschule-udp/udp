import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		cors: true,
		host: "127.0.0.1",
		port: 3000
	},
	preview: {
		cors: true,
		host: "127.0.0.1",
		port: 3000
	}
});

const sveltePreprocess = require("svelte-preprocess");
const vercel = require('@sveltejs/adapter-vercel');
const pkg = require('./package.json');

/** @type {import('@sveltejs/kit').Config} */
module.exports = {
	preprocess: [
		sveltePreprocess({
			defaults: {
				style: "postcss",
			},
			postcss: true
		}),
	],
	kit: {
		adapter: vercel(),
		target: '#svelte',

		vite: {
			optimizeDeps: {
				include: ['clipboard-copy']
			},
			ssr: {
				noExternal: Object.keys(pkg.dependencies || {})
			}
		}
	}
};

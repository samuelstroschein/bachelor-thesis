const vercel = require('@sveltejs/adapter-vercel');
const pkg = require('./package.json');

/** @type {import('@sveltejs/kit').Config} */
module.exports = {
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

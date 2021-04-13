<script lang="ts">
	import { algorithm } from '../../store';
	// @ts-ignore
	import { Column } from 'svelte-fluttered';
	import { TextInput, Button } from 'carbon-components-svelte';

	let endRange;
	let startRange;

	function advanceAlgortihm() {}
</script>

<h3>Step {$algorithm.stepRanges.length}</h3>
<Column>
	<TextInput inline bind:value={endRange} labelText="Best segment" placeholder="a,b,c,d,e or f" />
	<div class="h-2" />
	<TextInput
		inline
		bind:value={startRange}
		labelText="Second best segment"
		placeholder="a,b,c,d,e or f"
	/>
</Column>
<div class="h-4" />
<Button on:click={advanceAlgortihm}>Download gcode</Button>

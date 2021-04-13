<script lang="ts">
	import { algorithm } from '../../store';
	// @ts-ignore
	import { Column } from 'svelte-fluttered';
	import { TextInput, Button } from 'carbon-components-svelte';

	let bestSegment: string;
	let secondBestSegment: string;

	function alphabetCharacterToIndex(character: string) {
		if (character == 'f') return 5;
		else if (character == 'e') return 4;
		else if (character == 'd') return 3;
		else if (character == 'c') return 2;
		else if (character == 'b') return 1;
		else if (character == 'a') return 0;
		else throw Error('Unexpected Character');
	}

	function nextStep() {
		const x = alphabetCharacterToIndex(bestSegment);
		const y = alphabetCharacterToIndex(secondBestSegment);
		const newRange: [number, number] = x > y ? [x, y] : [y, x];
		$algorithm.step(newRange);
	}
</script>

<h3>Step {$algorithm.stepRanges.length}</h3>
<Column>
	<TextInput
		inline
		invalid={!'abcdef'.includes(bestSegment) || bestSegment == ''}
		bind:value={bestSegment}
		labelText="Best segment"
		placeholder="fill in a,b,c,d,e or f"
	/>
	<div class="h-2" />
	<TextInput
		inline
		invalid={!'abcdef'.includes(secondBestSegment) || secondBestSegment == ''}
		bind:value={secondBestSegment}
		labelText="Second best segment"
		placeholder="fill in a,b,c,d,e or f"
	/>
</Column>
<div class="h-4" />
<Button
	disabled={!'abcdef'.includes(bestSegment) ||
		!'abcdef'.includes(secondBestSegment) ||
		secondBestSegment == '' ||
		bestSegment == '' ||
		secondBestSegment == bestSegment}
	on:click={() => null}>Next Step</Button
>
<Button kind="secondary" on:click={() => null}>No More Improvement</Button>

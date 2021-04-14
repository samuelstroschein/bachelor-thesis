<script lang="ts">
	import { algorithm } from '../../store';
	// @ts-ignore
	import { Column } from 'svelte-fluttered';
	import { TextInput, Button } from 'carbon-components-svelte';
	import {
		downloadGcode,
		gcodeAsBlob,
		generateRetractionGcode
	} from './../typescript/generate_gcode';
	import type { SegmentVariables } from './../typescript/generate_gcode';

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
		const index1 = alphabetCharacterToIndex(bestSegment);
		const index2 = alphabetCharacterToIndex(secondBestSegment);
		const x = $algorithm.stepSegments[$algorithm.stepSegments.length - 1][index1];
		const y = $algorithm.stepSegments[$algorithm.stepSegments.length - 1][index2];
		const newRange: [number, number] = x > y ? [x, y] : [y, x];
		const nextStep = $algorithm.step(newRange);
		// forcefully refreshing the state
		algorithm.update((_) => $algorithm);
		const segments: SegmentVariables[] = nextStep.map((retractionDistance) => {
			return <SegmentVariables>{
				retractionDistance: retractionDistance,
				retractionSpeed: 40,
				extraRestartDistance: 0,
				prime: 40,
				zHop: 0
			};
		});
		const file = gcodeAsBlob(generateRetractionGcode([220, 220], 200, 60, segments));
		const stepNumber = $algorithm.stepRanges.length;
		downloadGcode(document, file, `retraction${stepNumber}.gcode`);
	}

	function showBestSetting() {
		alert(
			`Your best Retraction Distance is in the range of ${
				$algorithm.stepRanges[$algorithm.stepRanges.length - 1][0]
			} and ${$algorithm.stepRanges[$algorithm.stepRanges.length - 1][1]}`
		);
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
	on:click={nextStep}>Next Step</Button
>
<Button kind="secondary" on:click={showBestSetting}>No More Improvement</Button>

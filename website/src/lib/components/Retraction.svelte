<script lang="ts">
	import Step from './Step.svelte';
	import type { SegmentVariables } from './../typescript/generate_gcode';
	import {
		gcodeAsBlob,
		generateRetractionGcode,
		downloadGcode
	} from './../typescript/generate_gcode';
	import { NumberInput, Button } from 'carbon-components-svelte';
	import { AlgorithmV1 } from '../typescript/algorithm_v1';
	// @ts-ignore
	import { Column, Row } from 'svelte-fluttered';
	import { algorithm } from '../../store';

	let endRange: number = 6;
	let startRange: number = 2;

	function initAlgorithm() {
		algorithm.set(new AlgorithmV1());
		const firstStep = $algorithm.step([endRange, startRange]);
		const segments: SegmentVariables[] = firstStep.map((retractionDistance) => {
			return <SegmentVariables>{
				retractionDistance: retractionDistance,
				retractionSpeed: 40,
				extraRestartDistance: 0,
				prime: 40,
				zHop: 0
			};
		});
		const file = gcodeAsBlob(generateRetractionGcode([220, 220], 200, 60, segments));
		downloadGcode(document, file, 'retraction1.gcode');
	}
</script>

<h2>Retraction Distance</h2>

<div class="h-2" />

<h3 class="mb-1">Step 0</h3>
<h4>Instructions:</h4>
<p>
	1. Select a starting range to initialize the algorithm. The end range must be bigger than the
	start range.
</p>
<p>2. Download the gcode and print it. The file is split in segemnts as shown on the right.</p>
<p>3. Proceed with the next step which will show when you downloaded the gcode.</p>

<div class="my-4" />

<Row mainAxisAlignment="between">
	<div>
		<Column>
			<NumberInput bind:value={endRange} label="End Range in mm" />
			<div class="h-2" />
			<NumberInput bind:value={startRange} label="Start Range in mm" />
		</Column>
		<div class="h-4" />
		{#if $algorithm.stepRanges.length == 0}
			<Button on:click={initAlgorithm}>Download gcode</Button>
		{:else}
			<Button kind="tertiary" on:click={initAlgorithm}>Restart</Button>
		{/if}
	</div>
	<div class="w-96">
		<img src="retraction_diagram.jpeg" alt="" />
	</div>
</Row>

<div class="h-4" />

{#if $algorithm.stepRanges.length > 0}
	{#each $algorithm.stepRanges as _}
		<Step />
		<div class="h-4" />
	{/each}
{/if}

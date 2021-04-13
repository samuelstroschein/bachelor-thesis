<script lang="ts">
	import { NumberInput, Button } from 'carbon-components-svelte';
	import { AlgorithmV1 } from '../typescript/algorithm_v1';
	// @ts-ignore
	import { Column, Row } from 'svelte-fluttered';

	let algorithm: AlgorithmV1;
	let endRange: number = 6;
	let startRange: number = 2;

	function initAlgorithm() {
		algorithm = new AlgorithmV1([endRange, startRange]);
		const step = algorithm.step();
		// alert(algorithm.step());
	}
</script>

<h2>Retraction Distance</h2>

<div class="h-2" />

<Row crossAxisAlignment="center">
	<div>
		<Column>
			<NumberInput bind:value={endRange} label="End Range in mm" />
			<div class="h-2" />
			<NumberInput bind:value={startRange} label="Start Range in mm" />
		</Column>
		<div class="h-4" />
		<Button on:click={initAlgorithm}>Generate gcode</Button>
	</div>
	<div class="w-96">
		<img src="retraction_diagram.jpeg" alt="" />
	</div>
</Row>

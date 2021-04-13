<script lang="ts">
	import { AlgorithmV1 } from './../typescript/algorithm_v1.ts';
	import { NumberInput, Button } from 'carbon-components-svelte';
	// @ts-ignore
	import { Column, Row } from 'svelte-fluttered';
	import { onMount } from 'svelte';

	let algoV1: AlgorithmV1
	let endRange: numeric = 6
	let startRange: numeric = 2

	onMount(() => {
		algoV1 = new AlgorithmV1()
	})

</script>

<h2>Retraction Distance</h2>

<div class="h-2"></div>

<Row crossAxisAlignment="center">
	<div>
		<Column>
			<NumberInput bind:value= {endRange} label="End Range in mm" />
			<div class="h-2"></div>
			<NumberInput bind:value= {startRange} label="Start Range in mm" />
		</Column>
		<div class="h-4"></div>
		<Button on:click={() => alert(`${endRange}`)}>Generate gcode</Button>
	</div>
	<div class="w-96">
		<img src="retraction_diagram.jpeg" alt="">
	</div>
</Row>
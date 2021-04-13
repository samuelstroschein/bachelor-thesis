<script lang="ts">
	import type { SegmentVariables } from './../typescript/generate_gcode';
	import { gcodeAsBlob, generateRetractionGcode } from './../typescript/generate_gcode';
	import { NumberInput, Button } from 'carbon-components-svelte';
	import { AlgorithmV1 } from '../typescript/algorithm_v1';
	// @ts-ignore
	import { Column, Row } from 'svelte-fluttered';
	import { algorithm } from '../../store';

	let endRange: number = 6;
	let startRange: number = 2;

	function download(blob, fileName) {
		var a = document.createElement('a');
		a.download = fileName;
		a.href = URL.createObjectURL(blob);
		a.dataset.downloadurl = ['text/plain', a.download, a.href].join(':');
		a.style.display = 'none';
		document.body.appendChild(a);
		a.click();
		document.body.removeChild(a);
		setTimeout(function () {
			URL.revokeObjectURL(a.href);
		}, 1500);
	}

	function initAlgorithm() {
		// algorithm.set(new AlgorithmV1([endRange, startRange]));
		algorithm.set(new AlgorithmV1([endRange, startRange]));
		const firstStep = $algorithm.step();
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
		download(file, 'retraction1.gcode');
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

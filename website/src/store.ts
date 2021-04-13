import { AlgorithmV1 } from './lib/typescript/algorithm_v1';
import { derived, writable, Writable } from "svelte/store";


export const algorithm = writable(new AlgorithmV1([6, 2]))
export class AlgorithmV1 {
    stepRanges: Array<[number, number]>

    constructor(startingRange: [number, number]) {
        this.stepRanges = [startingRange]
    }

    step(): Array<number> {
        let result = []
        const currentRange = this.stepRanges[this.stepRanges.length - 1]
        const valuesToGenerate = 6
        const stepSize = (currentRange[0] - currentRange[1]) / (valuesToGenerate - 1)
        let nextValue = currentRange[1]
        for (let i = 0; i < valuesToGenerate; i++) {
            result.push(nextValue)
            nextValue = Number((nextValue + stepSize).toFixed(2))
        }
        return result
    }

    setNextStepRange(range: [number, number]): void {
        this.stepRanges.push(range)
    }
}
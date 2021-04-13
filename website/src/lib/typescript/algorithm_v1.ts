export class AlgorithmV1 {
    stepRanges: Array<[number, number]> = [];

    step(range: [number, number]): Array<number> {
        this.stepRanges.push(range)
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
}
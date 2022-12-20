var RED_COLOR = "#ED9595";
var GRAY_COLOR = "#EAEAEA";
var GREEN_COLOR = "#96DBC8";

/**
 * Abstract Class MyGraph.
 *
 * @class MyGraph
 */
class MyGraph {
    constructor(cancer) {
        if (this.constructor == MyGraph) {
            throw new Error("Abstract classes can't be instantiated.");
        }
    }

    drawGraph(idx) {
        throw new Error("Method 'drawGraph()' must be implemented.");
    }

    // setSection() {
    //     throw new Error("Method 'setSection()' must be implemented.");
    // }
}

/**
 * 2SectionGraph.
 *
 * @class 2SectionGraph
 * @extends {MyGraph}
 */
class TwoSectionGraph extends MyGraph {
    chartData = [];
    cancer = "";
    value = 40;

    constructor(cancer) {
        super();
        this.cancer = cancer;
    }

    drawGraph(idx, mid) {
        this.chartData.push({
            value: this.value, //triangle 위치
            indicator: "point",
            shape: "triangle",
            width: 12,
            height: -12,
            offset: 0,
            color: "gray",
            colorRanges: [
                {
                    startpoint: 0,
                    breakpoint: mid,
                    color: "green",
                },
                {
                    startpoint: mid,
                    breakpoint: mid * 2,
                    color: "gray",
                },
            ],
        });
        var chtID = document.getElementById(this.cancer + idx).getContext("2d");
        return new Chart(chtID).Linear(this.chartData, {
            range: {
                startValue: 0,
                endValue: mid * 2,
            },
            responsive: true,
            // animationSteps: 1, //몇번에 걸쳐서 애니메이션을 보여줄것인가. 0: 없음, 1: 바로 보여주기
            animation: false,
            axisColor: GRAY_COLOR,
            axisWidth: 20,
            axisHeight: 20,
            tickLabels: {
                interval: 1,
                customValues: [mid],
                offset: 15, // label 높이 지정
                color: "gray",
            },
            geometry: "horizontal",
            scaleColorRanges: [
                {
                    // 그래프의 영역 색깔지정
                    start: 0,
                    end: mid,
                    color: GREEN_COLOR,
                },
            ],
        });
    }
}

/**
 * 3SectionGraph.
 *
 * @class 3SectionGraph
 * @extends {MyGraph}
 */
class ThreeSectionGraph extends MyGraph {
    chartData = [];
    cancer = "";
    value = 30;

    constructor(cancer) {
        super();
        this.cancer = cancer;
    }

    drawGraph(idx, min, max) {
        this.chartData.push({
            value: this.value, //triangle 위치
            indicator: "point",
            shape: "triangle",
            width: 12,
            height: -12,
            offset: 0,
            color: "gray",
            colorRanges: [
                {
                    startpoint: 0,
                    breakpoint: min,
                    color: "gray",
                },
                {
                    startpoint: min,
                    breakpoint: max,
                    color: "gray",
                },
                {
                    startpoint: max,
                    breakpoint: min + max,
                    color: "red",
                },
            ],
        });
        var chtID = document.getElementById(this.cancer + idx).getContext("2d");
        return new Chart(chtID).Linear(this.chartData, {
            range: {
                //그래프의 총 범위
                startValue: 0,
                endValue: min + max,
            },
            responsive: true,
            // animationSteps: 1, //몇번에 걸쳐서 애니메이션을 보여줄것인가. 0: 없음, 1: 바로 보여주기
            animation: false,
            axisColor: GRAY_COLOR,
            axisWidth: 20,
            axisHeight: 20,
            minorTicks: {
                interval: 1,
                customValues: [min],
                height: 1,
                width: 15,
                offset: 0,
                color: "gray",
            },
            tickLabels: {
                interval: 1,
                customValues: [min, max],
                offset: 15, // label 높이 지정
                color: "gray",
            },
            geometry: "horizontal",
            scaleColorRanges: [
                // 그래프의 영역별 색깔지정
                {
                    start: max,
                    end: min + max,
                    color: RED_COLOR,
                },
            ],
        });
    }
}

class GraphDrawer {
    constructor(cancer, indexes) {
        this.cancer = cancer;
        this.indexes = indexes;
        this.twoSecGraph = new TwoSectionGraph(cancer);
        this.threeSecGraph = new ThreeSectionGraph(cancer);
    }

    drawGraphs() {
        for (const [idx, key] of Object.keys(this.indexes).entries()) {
            if (this.indexes[key]["min"] == 0) {
                const mid = this.indexes[key]["max"];
                this.twoSecGraph.drawGraph(idx, mid);
            } else {
                const min = this.indexes[key]["min"];
                const max = this.indexes[key]["max"];
                this.threeSecGraph.drawGraph(idx, min, max);
            }
        }
    }

    getMinMaxValue() {}
}

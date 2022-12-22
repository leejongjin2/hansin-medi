var RED_COLOR = "#ED9595";
var GRAY_COLOR = "#EAEAEA";
var GREEN_COLOR = "#96DBC8";
var GRAY_BAR_COLOR = "#c4c4c4";

/**
 * Abstract Class MyGraph.
 *
 * @class MyGraph
 */
class MyGraph {
    chartData = [];

    constructor(cancer) {
        if (this.constructor == MyGraph) {
            throw new Error("Abstract classes can't be instantiated.");
        }
    }

    drawGraph(idx) {
        throw new Error("Method 'drawGraph()' must be implemented.");
    }

    adjustValue() {
        throw new Error("Method 'adjustValue()' must be implemented.");
    }

    resetChartData() {
        this.chartData = [];
    }
}

/**
 * Basic2SectionGraph.
 *
 * @class Basic2SectionGraph
 * @extends {MyGraph}
 */
class Basic2SectionGraph extends MyGraph {
    cancer = "";

    constructor(cancer) {
        super();
        this.cancer = cancer;
    }

    adjustValue() {
        this.value = Math.max(0, this.value);
        this.value = Math.min(this.mid * 2, this.value);
    }

    drawGraph(idx, mid, value) {
        this.resetChartData();
        this.mid = mid;
        this.value = value;
        this.adjustValue();

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
                    breakpoint: mid / 2,
                    color: "green",
                },
                {
                    startpoint: mid / 2,
                    breakpoint: mid + mid / 2,
                    color: "gray",
                },
                {
                    // breakpoint: mid + mid / 2,
                    breakpoint: mid * 2 + 1,
                    color: "red",
                },
            ],
        });
        var chtID = document.getElementById(this.cancer + idx).getContext("2d");
        return new Chart(chtID).Linear(this.chartData, this.getChartConfig());
    }

    getChartConfig() {
        if (this.value <= this.mid) {
            return {
                range: {
                    startValue: 0,
                    endValue: this.mid * 2,
                },
                responsive: true,
                // animationSteps: 999,
                animation: false,
                axisColor: GRAY_COLOR,
                axisWidth: 20,
                axisHeight: 20,
                minorTicks: {
                    interval: 1,
                    customValues: [this.mid],
                    height: 1,
                    width: 15,
                    offset: 0,
                    color: GRAY_BAR_COLOR,
                },
                tickLabels: {
                    interval: 1,
                    customValues: [this.mid],
                    offset: 15, // label 높이 지정
                    color: "gray",
                },
                geometry: "horizontal",
                scaleColorRanges: [
                    {
                        // 그래프의 영역 색깔지정
                        start: 0,
                        end: this.mid,
                        color: GREEN_COLOR,
                    },
                ],
            };
        } else {
            return {
                range: {
                    startValue: 0,
                    endValue: this.mid * 2,
                },
                responsive: true,
                // animationSteps: 999,
                animation: false,
                axisColor: GRAY_COLOR,
                axisWidth: 20,
                axisHeight: 20,
                minorTicks: {
                    interval: 1,
                    customValues: [this.mid],
                    height: 1,
                    width: 15,
                    offset: 0,
                    color: GRAY_BAR_COLOR,
                },
                tickLabels: {
                    interval: 1,
                    customValues: [this.mid],
                    offset: 15, // label 높이 지정
                    color: "gray",
                },
                geometry: "horizontal",
                scaleColorRanges: [
                    {
                        // 그래프의 영역 색깔지정
                        start: this.mid,
                        end: this.mid * 2,
                        color: RED_COLOR,
                    },
                ],
            };
        }
    }
}

/**
 * Basic3SectionGraph.
 *
 * @class Basic3SectionGraph
 * @extends {MyGraph}
 */
class Basic3SectionGraph extends MyGraph {
    cancer = "";

    constructor(cancer) {
        super();
        this.cancer = cancer;
    }

    adjustValue() {
        this.value = Math.max(0, this.value);
        this.value = Math.min(this.min + this.max, this.value);
    }

    drawGraph(idx, min, max, value) {
        this.resetChartData();
        this.min = min;
        this.max = max;
        this.value = value;
        this.adjustValue();

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
                    color: "red",
                },
                {
                    breakpoint: min,
                    color: "gray",
                },
                {
                    startpoint: min,
                    breakpoint: max,
                    color: "green",
                },
                {
                    breakpoint: max,
                    color: "gray",
                },
                {
                    startpoint: max,
                    breakpoint: min + max + 1,
                    color: "red",
                },
            ],
        });
        var chtID = document.getElementById(this.cancer + idx).getContext("2d");
        return new Chart(chtID).Linear(this.chartData, this.getChartConfig());
    }

    getChartConfig() {
        if (this.value <= this.min)
            return {
                range: {
                    //그래프의 총 범위
                    startValue: 0,
                    endValue: this.min + this.max,
                },
                responsive: true,
                // animationSteps: 999,
                animation: false,
                axisColor: GRAY_COLOR,
                axisWidth: 20,
                axisHeight: 20,
                minorTicks: {
                    interval: 1,
                    customValues: [this.min, this.max],
                    height: 1,
                    width: 15,
                    offset: 0,
                    color: GRAY_BAR_COLOR,
                },
                tickLabels: {
                    interval: 1,
                    customValues: [this.min, this.max],
                    offset: 15, // label 높이 지정
                    color: "gray",
                },
                geometry: "horizontal",
                scaleColorRanges: [
                    // 그래프의 영역별 색깔지정
                    {
                        start: 0,
                        end: this.min,
                        color: RED_COLOR,
                    },
                ],
            };
        else if (this.value >= this.max)
            return {
                range: {
                    //그래프의 총 범위
                    startValue: 0,
                    endValue: this.min + this.max,
                },
                responsive: true,
                // animationSteps: 999,
                animation: false,
                axisColor: GRAY_COLOR,
                axisWidth: 20,
                axisHeight: 20,
                minorTicks: {
                    interval: 1,
                    customValues: [this.min, this.max],
                    height: 1,
                    width: 15,
                    offset: 0,
                    color: GRAY_BAR_COLOR,
                },
                tickLabels: {
                    interval: 1,
                    customValues: [this.min, this.max],
                    offset: 15, // label 높이 지정
                    color: "gray",
                },
                geometry: "horizontal",
                scaleColorRanges: [
                    // 그래프의 영역별 색깔지정
                    {
                        start: this.max,
                        end: this.min + this.max,
                        color: RED_COLOR,
                    },
                ],
            };
        else
            return {
                range: {
                    //그래프의 총 범위
                    startValue: 0,
                    endValue: this.min + this.max,
                },
                responsive: true,
                // animationSteps: 999,
                animation: false,
                axisColor: GRAY_COLOR,
                axisWidth: 20,
                axisHeight: 20,
                minorTicks: {
                    interval: 1,
                    customValues: [this.min, this.max],
                    height: 1,
                    width: 15,
                    offset: 0,
                    color: GRAY_BAR_COLOR,
                },
                tickLabels: {
                    interval: 1,
                    customValues: [this.min, this.max],
                    offset: 15, // label 높이 지정
                    color: "gray",
                },
                geometry: "horizontal",
                scaleColorRanges: [
                    // 그래프의 영역별 색깔지정
                    {
                        start: this.min,
                        end: this.max,
                        color: GREEN_COLOR,
                    },
                ],
            };
    }
}

/**
 * Longer3SectionGraph.
 *
 * @class Longer3SectionGraph
 * @extends {MyGraph}
 */
class Longer3SectionGraph extends MyGraph {
    cancer = "";

    constructor(cancer) {
        super();
        this.cancer = cancer;
    }

    adjustValue() {
        this.value = Math.max(0, this.value);
        this.value = Math.min(-this.min + this.max * 2, this.value);
    }

    drawGraph(idx, min, max, value) {
        this.resetChartData();
        this.min = min;
        this.max = max;
        this.value = value;
        this.adjustValue();

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
                    color: "red",
                },
                {
                    breakpoint: min,
                    color: "gray",
                },
                {
                    startpoint: min,
                    breakpoint: max,
                    color: "green",
                },
                {
                    breakpoint: max,
                    color: "gray",
                },
                {
                    startpoint: max,
                    breakpoint: -this.min + this.max * 2 + 1,
                    color: "red",
                },
            ],
        });
        var chtID = document.getElementById(this.cancer + idx).getContext("2d");
        return new Chart(chtID).Linear(this.chartData, this.getChartConfig());
    }

    getChartConfig() {
        if (this.value <= this.min)
            return {
                range: {
                    //그래프의 총 범위
                    startValue: 0,
                    endValue: -this.min + this.max * 2,
                },
                responsive: true,
                // animationSteps: 999,
                animation: false,
                axisColor: GRAY_COLOR,
                axisWidth: 20,
                axisHeight: 20,
                minorTicks: {
                    interval: 1,
                    customValues: [this.min, this.max],
                    height: 1,
                    width: 15,
                    offset: 0,
                    color: GRAY_BAR_COLOR,
                },
                tickLabels: {
                    interval: 1,
                    customValues: [this.min, this.max],
                    offset: 15, // label 높이 지정
                    color: "gray",
                },
                geometry: "horizontal",
                scaleColorRanges: [
                    // 그래프의 영역별 색깔지정
                    {
                        start: 0,
                        end: this.min,
                        color: RED_COLOR,
                    },
                ],
            };
        else if (this.value >= this.max)
            return {
                range: {
                    //그래프의 총 범위
                    startValue: 0,
                    endValue: -this.min + this.max * 2,
                },
                responsive: true,
                // animationSteps: 999,
                animation: false,
                axisColor: GRAY_COLOR,
                axisWidth: 20,
                axisHeight: 20,
                minorTicks: {
                    interval: 1,
                    customValues: [this.min, this.max],
                    height: 1,
                    width: 15,
                    offset: 0,
                    color: GRAY_BAR_COLOR,
                },
                tickLabels: {
                    interval: 1,
                    customValues: [this.min, this.max],
                    offset: 15, // label 높이 지정
                    color: "gray",
                },
                geometry: "horizontal",
                scaleColorRanges: [
                    // 그래프의 영역별 색깔지정
                    {
                        start: this.max,
                        end: -this.min + this.max * 2,
                        color: RED_COLOR,
                    },
                ],
            };
        else
            return {
                range: {
                    //그래프의 총 범위
                    startValue: 0,
                    endValue: -this.min + this.max * 2,
                },
                responsive: true,
                // animationSteps: 999,
                animation: false,
                axisColor: GRAY_COLOR,
                axisWidth: 20,
                axisHeight: 20,
                minorTicks: {
                    interval: 1,
                    customValues: [this.min, this.max],
                    height: 1,
                    width: 15,
                    offset: 0,
                    color: GRAY_BAR_COLOR,
                },
                tickLabels: {
                    interval: 1,
                    customValues: [this.min, this.max],
                    offset: 15, // label 높이 지정
                    color: "gray",
                },
                geometry: "horizontal",
                scaleColorRanges: [
                    // 그래프의 영역별 색깔지정
                    {
                        start: this.min,
                        end: this.max,
                        color: GREEN_COLOR,
                    },
                ],
            };
    }
}

/**
 * 요단백Graph.
 *
 * @class 요단백Graph
 * @extends {MyGraph}
 */
class 요단백Graph extends MyGraph {
    cancer = "";
    요단백min = 0;
    요단백max = 5;

    constructor(cancer) {
        super();
        this.cancer = cancer;
    }

    adjustValue() {
        this.value = Math.max(this.요단백min, this.value);
        this.value = Math.min(this.요단백max, this.value);
    }

    drawGraph(idx, min, max, value) {
        this.resetChartData();
        this.min = min;
        this.max = max;
        this.value = value;
        this.adjustValue();

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
                    startpoint: this.요단백min,
                    breakpoint: min,
                    color: "green",
                },
                {
                    startpoint: min,
                    breakpoint: max,
                    color: "gray",
                },
                {
                    startpoint: max,
                    breakpoint: this.요단백max + 1,
                    color: "red",
                },
            ],
        });
        var chtID = document.getElementById(this.cancer + idx).getContext("2d");
        return new Chart(chtID).Linear(this.chartData, this.getChartConfig());
    }

    getChartConfig() {
        if (this.value < this.min)
            return {
                range: {
                    //그래프의 총 범위
                    startValue: this.요단백min,
                    endValue: this.요단백max,
                },
                responsive: true,
                // animationSteps: 999,
                animation: false,
                axisColor: GRAY_COLOR,
                axisWidth: 20,
                axisHeight: 20,
                minorTicks: {
                    interval: 1,
                    customValues: [0, 1, 2, 3, 4, 5],
                    height: 1,
                    width: 15,
                    offset: 0,
                    color: GRAY_BAR_COLOR,
                },
                tickLabels: {
                    interval: 1,
                    customValues: [0, 1, 2, 3, 4, 5],
                    offset: 15, // label 높이 지정
                    color: "gray",
                },
                geometry: "horizontal",
                scaleColorRanges: [
                    // 그래프의 영역별 색깔지정
                    {
                        start: this.요단백min,
                        end: this.min,
                        color: GREEN_COLOR,
                    },
                ],
            };
        else if (this.value >= this.max)
            return {
                range: {
                    //그래프의 총 범위
                    startValue: this.요단백min,
                    endValue: this.요단백max,
                },
                responsive: true,
                // animationSteps: 999,
                animation: false,
                axisColor: GRAY_COLOR,
                axisWidth: 20,
                axisHeight: 20,
                minorTicks: {
                    interval: 1,
                    customValues: [0, 1, 2, 3, 4, 5],
                    height: 1,
                    width: 15,
                    offset: 0,
                    color: GRAY_BAR_COLOR,
                },
                tickLabels: {
                    interval: 1,
                    customValues: [0, 1, 2, 3, 4, 5],
                    offset: 15, // label 높이 지정
                    color: "gray",
                },
                geometry: "horizontal",
                scaleColorRanges: [
                    // 그래프의 영역별 색깔지정
                    {
                        start: this.max,
                        end: this.요단백max,
                        color: RED_COLOR,
                    },
                ],
            };
        else
            return {
                range: {
                    //그래프의 총 범위
                    startValue: this.요단백min,
                    endValue: this.요단백max,
                },
                responsive: true,
                // animationSteps: 999,
                animation: false,
                axisColor: GRAY_COLOR,
                axisWidth: 20,
                axisHeight: 20,
                minorTicks: {
                    interval: 1,
                    customValues: [0, 1, 2, 3, 4, 5],
                    height: 1,
                    width: 15,
                    offset: 0,
                    color: GRAY_BAR_COLOR,
                },
                tickLabels: {
                    interval: 1,
                    customValues: [0, 1, 2, 3, 4, 5],
                    offset: 15, // label 높이 지정
                    color: "gray",
                },
                geometry: "horizontal",
                scaleColorRanges: [
                    // 그래프의 영역별 색깔지정
                    {
                        start: this.min,
                        end: this.max,
                        color: GRAY_BAR_COLOR,
                    },
                ],
            };
    }
}

/**
 * 비만도Graph.
 *
 * @class 비만도Graph
 * @extends {MyGraph}
 */
class 비만도Graph extends MyGraph {
    cancer = "";

    constructor(cancer) {
        super();
        this.cancer = cancer;
    }

    adjustValue() {
        this.비만도min = this.min - 5;
        this.비만도max = this.max + 5;
        this.value = Math.max(this.비만도min, this.value);
        this.value = Math.min(this.비만도max, this.value);
    }

    drawGraph(idx, min, max, value) {
        this.resetChartData();
        this.min = min;
        this.max = max;
        this.value = value;
        this.adjustValue();

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
                    startpoint: this.비만도min,
                    breakpoint: this.min,
                    color: "red",
                },
                {
                    startpoint: this.min,
                    breakpoint: this.max,
                    color: "green",
                },
                {
                    startpoint: this.max,
                    breakpoint: this.비만도max + 1,
                    color: "red",
                },
            ],
        });
        var chtID = document.getElementById(this.cancer + idx).getContext("2d");
        return new Chart(chtID).Linear(this.chartData, this.getChartConfig());
    }

    getChartConfig() {
        if (this.value < this.min)
            return {
                range: {
                    //그래프의 총 범위
                    startValue: this.비만도min,
                    endValue: this.비만도max,
                },
                responsive: true,
                // animationSteps: 999,
                animation: false,
                axisColor: GRAY_COLOR,
                axisWidth: 20,
                axisHeight: 20,
                minorTicks: {
                    interval: 1,
                    customValues: [this.min, this.max],
                    height: 1,
                    width: 15,
                    offset: 0,
                    color: GRAY_BAR_COLOR,
                },
                tickLabels: {
                    interval: 1,
                    customValues: [this.min, this.max],
                    offset: 15, // label 높이 지정
                    color: "gray",
                },
                geometry: "horizontal",
                scaleColorRanges: [
                    // 그래프의 영역별 색깔지정
                    {
                        start: this.비만도min,
                        end: this.min,
                        color: RED_COLOR,
                    },
                ],
            };
        else if (this.value >= this.max)
            return {
                range: {
                    //그래프의 총 범위
                    startValue: this.비만도min,
                    endValue: this.비만도max,
                },
                responsive: true,
                // animationSteps: 999,
                animation: false,
                axisColor: GRAY_COLOR,
                axisWidth: 20,
                axisHeight: 20,
                minorTicks: {
                    interval: 1,
                    customValues: [this.min, this.max],
                    height: 1,
                    width: 15,
                    offset: 0,
                    color: GRAY_BAR_COLOR,
                },
                tickLabels: {
                    interval: 1,
                    customValues: [this.min, this.max],
                    offset: 15, // label 높이 지정
                    color: "gray",
                },
                geometry: "horizontal",
                scaleColorRanges: [
                    // 그래프의 영역별 색깔지정
                    {
                        start: this.max,
                        end: this.비만도max,
                        color: RED_COLOR,
                    },
                ],
            };
        else
            return {
                range: {
                    //그래프의 총 범위
                    startValue: this.비만도min,
                    endValue: this.비만도max,
                },
                responsive: true,
                // animationSteps: 999,
                animation: false,
                axisColor: GRAY_COLOR,
                axisWidth: 20,
                axisHeight: 20,
                minorTicks: {
                    interval: 1,
                    customValues: [this.min, this.max],
                    height: 1,
                    width: 15,
                    offset: 0,
                    color: GRAY_BAR_COLOR,
                },
                tickLabels: {
                    interval: 1,
                    customValues: [this.min, this.max],
                    offset: 15, // label 높이 지정
                    color: "gray",
                },
                geometry: "horizontal",
                scaleColorRanges: [
                    // 그래프의 영역별 색깔지정
                    {
                        start: this.min,
                        end: this.max,
                        color: GREEN_COLOR,
                    },
                ],
            };
    }
}

class GraphDrawer {
    constructor(cancer, indexes) {
        this.cancer = cancer;
        this.indexes = indexes;
        this.twoSecGraph = new Basic2SectionGraph(cancer);
        this.threeSecGraph = new Basic3SectionGraph(cancer);
    }

    drawGraphs() {
        for (const [idx, key] of Object.keys(this.indexes).entries()) {
            const min = this.indexes[key]["min"];
            const max = this.indexes[key]["max"];
            const value = this.indexes[key]["v"];

            if (key == "요단백") {
                const 요단백 = new 요단백Graph(this.cancer);
                요단백.drawGraph(idx, min, max, value);
            } else if (key == "비만도") {
                const 비만도 = new 비만도Graph(this.cancer);

                비만도.drawGraph(idx, min, max, value);
            } else if (key == "고밀도지단백콜레스테롤") {
                this.twoSecGraph.drawGraph(idx, min, value);
            } else {
                if (min == 0) {
                    this.twoSecGraph.drawGraph(idx, max, value);
                } else {
                    if (min / (min + max) < 0.2) {
                        const longer3SectionGraph = new Longer3SectionGraph(
                            this.cancer
                        );
                        longer3SectionGraph.drawGraph(idx, min, max, value);
                    } else {
                        this.threeSecGraph.drawGraph(idx, min, max, value);
                    }
                }
            }
        }
    }
}

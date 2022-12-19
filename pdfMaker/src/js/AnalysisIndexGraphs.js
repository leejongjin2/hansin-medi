// /**
//  * Abstract Class MyGraph.
//  *
//  * @class MyGraph
//  */
// class MyGraph {
//     constructor(cancer) {
//         if (this.constructor == MyGraph) {
//             throw new Error("Abstract classes can't be instantiated.");
//         }
//     }

//     drawGraph() {
//         throw new Error("Method 'drawGraph()' must be implemented.");
//     }

//     setSection() {
//         throw new Error("Method 'setSection()' must be implemented.");
//     }
// }

// /**
//  * 2SectionGraph.
//  *
//  * @class 2SectionGraph
//  * @extends {MyGraph}
//  */
// class TwoSectionGraph extends MyGraph {
//     barChartData_01 = [];
//     cancer = "";

//     constructor(cancer) {
//         super();
//         this.cancer = cancer;
//     }

//     drawGraph() {
//         this.barChartData_01.push({
//             value: graph01_position, //triangle 위치
//             indicator: "point",
//             shape: "triangle",
//             width: 12,
//             height: -12,
//             offset: 0,
//             color: "gray",
//             colorRanges: [
//                 {
//                     startpoint: 0,
//                     breakpoint: graph01_index,
//                     color: "green",
//                 },
//                 {
//                     startpoint: graph01_index,
//                     breakpoint: graph01_index * 2,
//                     color: "gray",
//                 },
//             ],
//         });
//         var ctx01 = document.getElementById("two").getContext("2d");
//         return new Chart(ctx01).Linear(barChartData_01, {
//             range: {
//                 startValue: 0,
//                 endValue: graph01_index * 2,
//             },
//             responsive: true,
//             // animationSteps: 1, //몇번에 걸쳐서 애니메이션을 보여줄것인가. 0: 없음, 1: 바로 보여주기
//             animation: false,
//             axisColor: GRAY_COLOR,
//             axisWidth: 20,
//             axisHeight: 20,
//             tickLabels: {
//                 interval: 1,
//                 customValues: [graph01_index],
//                 offset: 15, // label 높이 지정
//                 color: "gray",
//             },
//             geometry: "horizontal",
//             scaleColorRanges: [
//                 {
//                     // 그래프의 영역 색깔지정
//                     start: 0,
//                     end: graph01_index,
//                     color: GREEN_COLOR,
//                 },
//             ],
//         });
//     }
// }

// /**
//  * 3SectionGraph.
//  *
//  * @class 3SectionGraph
//  * @extends {MyGraph}
//  */
// class ThreeSectionGraph extends MyGraph {
//     barChartData_02 = [];
//     cancer = "";

//     constructor(cancer) {
//         super();
//         this.cancer = cancer;
//     }

//     drawGraph() {
//         this.barChartData_02.push({
//             value: graph02_position, //triangle 위치
//             indicator: "point",
//             shape: "triangle",
//             width: 12,
//             height: -12,
//             offset: 0,
//             color: "gray",
//             colorRanges: [
//                 {
//                     startpoint: 0,
//                     breakpoint: graph02_index_lower,
//                     color: "gray",
//                 },
//                 {
//                     startpoint: graph02_index_lower,
//                     breakpoint: graph02_index_upper,
//                     color: "gray",
//                 },
//                 {
//                     startpoint: graph02_index_upper,
//                     breakpoint: graph02_index_lower + graph02_index_upper,
//                     color: "red",
//                 },
//             ],
//         });
//         var ctx02 = document.getElementById("three").getContext("2d");
//         return new Chart(ctx02).Linear(barChartData_02, {
//             range: {
//                 //그래프의 총 범위
//                 startValue: 0,
//                 endValue: graph02_index_lower + graph02_index_upper,
//             },
//             responsive: true,
//             animationSteps: 1, //몇번에 걸쳐서 애니메이션을 보여줄것인가. 0: 없음, 1: 바로 보여주기
//             axisColor: GRAY_COLOR,
//             axisWidth: 20,
//             axisHeight: 20,
//             minorTicks: {
//                 interval: 1,
//                 customValues: [graph02_index_lower],
//                 height: 1,
//                 width: 15,
//                 offset: 0,
//                 color: "gray",
//             },
//             tickLabels: {
//                 interval: 1,
//                 customValues: [graph02_index_lower, graph02_index_upper],
//                 offset: 15, // label 높이 지정
//                 color: "gray",
//             },
//             geometry: "horizontal",
//             scaleColorRanges: [
//                 // 그래프의 영역별 색깔지정
//                 {
//                     start: graph02_index_upper,
//                     end: graph02_index_lower + graph02_index_upper,
//                     color: RED_COLOR,
//                 },
//             ],
//         });
//     }
// }

// class GraphDrawer {
//     twoSecGraph = new TwoSectionGraph();
//     threeSecGraph = new ThreeSectionGraph();

//     diseases = ["간암", "위암"];
//     analysisIndexLiver = ["아세테이트", "알라닌", "알카라인"];
//     analysisIndexStomach = ["종양표지자", "고밀도지단백"];
//     valueLiver = [35, 2, 150];
//     valueStomach = [5.5, 25];

//     constructor(disease_info, user_info) {
//         this.disease_info = disease_info;
//         this.user_info = user_info;
//     }

//     drawGraphs() {
//         for (let disease of this.diseases) {
//             // for let indexer in analysisIndex
//             if (disease == "간암") {
//                 // assert this.analysisIndexLiver.length == this.valueLiver

//                 for (let i = 0; i < this.analysisIndexLiver.length; i++) {
//                     //get_analysisIndex_minmax(index, gender)
//                     if (
//                         this.analysisIndexLiver[i] == "아세테이트" ||
//                         this.analysisIndexLiver[i] == "알라닌"
//                     ) {
//                         let min = 4;
//                         let max = 40;

//                         if (min != 0) {
//                             this.threeSecGraph.drawGraph(
//                                 disease,
//                                 this.analysisIndexLiver[i],
//                                 this.valueLiver[i],
//                                 min,
//                                 max
//                             );
//                         } else {
//                             throw new Error("min =4인데 0이래-_-");
//                         }
//                     } else if (this.analysisIndexLiver[i] == "알카라인") {
//                         let min = 35;
//                         let max = 130;

//                         if (min != 0) {
//                             this.threeSecGraph.drawGraph(
//                                 disease,
//                                 this.analysisIndexLiver[i],
//                                 this.valueLiver[i],
//                                 min,
//                                 max
//                             );
//                         } else {
//                             throw new Error("min =35인데 0이래-_-");
//                         }
//                     } else {
//                         throw new Error("이상행~");
//                     }
//                 }
//             } else if (disease == "위암") {
//                 // assert this.analysisIndexStomach.length == this.valueStomach
//                 for (let i = 0; i < this.analysisIndexStomach.length; i++) {
//                     if (this.analysisIndexStomach[i] == "종양표지자") {
//                         let min = 0;
//                         let max = 4.7;

//                         if (min != 0) {
//                             throw new Error("min =0인데 아니래-_-");
//                         } else {
//                             this.twoSecGraph.drawGraph(
//                                 disease,
//                                 this.analysisIndexStomach[i],
//                                 this.valueStomach[i],
//                                 max
//                             );
//                         }
//                     } else if (this.analysisIndexStomach[i] == "고밀도지단백") {
//                         let min = 60;
//                         let max = 999;

//                         if (min != 0) {
//                             this.threeSecGraph.drawGraph(
//                                 disease,
//                                 this.analysisIndexStomach[i],
//                                 this.valueStomach[i],
//                                 min,
//                                 max
//                             );
//                         } else {
//                             throw new Error("min =60인데 0이래-_-");
//                         }
//                     } else {
//                         throw new Error("이상행~");
//                     }
//                 }
//             }
//         }
//     }

//     getGender() {
//         return "남성";
//     }

//     draw2SecGraph(disease, analysisIndex, value, mid) {
//         return new Chart();
//     }

//     draw3SecGraph(disease, analysisIndex, value, min, max) {
//         return new Chart();
//     }

//     getMinMaxValue() {}
// }

// function getCanvas() {
//     gd = new GraphDrawer(0, 0);
//     gd.drawGraphs();
// }

/*
유방암 위험도 분석
그래프 색깔 : RED_COLOR, GRAY_COLOR, GREEN_COLOR
분석 지표 별 구간
    - 2구간: 중간것 하나
*/

var RED_COLOR = "#ED9595";
var GRAY_COLOR = "#EAEAEA";
var GREEN_COLOR = "#96DBC8";

var graph01_position = 1; // min, max값 설정해줘야함
var graph01_index = 129;

var graph02_position = 180; // min, max값 설정해줘야함
var graph02_index_lower = 130;
var graph02_index_upper = 199;

var barChartData_01 = [];
barChartData_01.push({
    value: graph01_position, //triangle 위치
    indicator: "point",
    shape: "triangle",
    width: 12,
    height: -12,
    offset: 0,
    color: "gray",
    colorRanges: [
        {
            startpoint: 0,
            breakpoint: graph01_index,
            color: "green",
        },
        {
            startpoint: graph01_index,
            breakpoint: graph01_index * 2,
            color: "gray",
        },
    ],
});

var barChartData_02 = [];
barChartData_02.push({
    value: graph02_position, //triangle 위치
    indicator: "point",
    shape: "triangle",
    width: 12,
    height: -12,
    offset: 0,
    color: "gray",
    colorRanges: [
        {
            startpoint: 0,
            breakpoint: graph02_index_lower,
            color: "gray",
        },
        {
            startpoint: graph02_index_lower,
            breakpoint: graph02_index_upper,
            color: "gray",
        },
        {
            startpoint: graph02_index_upper,
            breakpoint: graph02_index_lower + graph02_index_upper,
            color: "red",
        },
    ],
});

function drawIndexGraph() {
    var ctx01 = document.getElementById("간암0").getContext("2d");
    new Chart(ctx01).Linear(barChartData_01, {
        range: {
            startValue: 0,
            endValue: graph01_index * 2,
        },
        responsive: true,
        // animationSteps: 1, //몇번에 걸쳐서 애니메이션을 보여줄것인가. 0: 없음, 1: 바로 보여주기
        animation: false,
        axisColor: GRAY_COLOR,
        axisWidth: 20,
        axisHeight: 20,
        tickLabels: {
            interval: 1,
            customValues: [graph01_index],
            offset: 15, // label 높이 지정
            color: "gray",
        },
        geometry: "horizontal",
        scaleColorRanges: [
            {
                // 그래프의 영역 색깔지정
                start: 0,
                end: graph01_index,
                color: GREEN_COLOR,
            },
        ],
    });

    var ctx01 = document.getElementById("간암1").getContext("2d");
    new Chart(ctx01).Linear(barChartData_01, {
        range: {
            startValue: 0,
            endValue: graph01_index * 2,
        },
        responsive: true,
        // animationSteps: 1, //몇번에 걸쳐서 애니메이션을 보여줄것인가. 0: 없음, 1: 바로 보여주기
        animation: false,
        axisColor: GRAY_COLOR,
        axisWidth: 20,
        axisHeight: 20,
        tickLabels: {
            interval: 1,
            customValues: [graph01_index],
            offset: 15, // label 높이 지정
            color: "gray",
        },
        geometry: "horizontal",
        scaleColorRanges: [
            {
                // 그래프의 영역 색깔지정
                start: 0,
                end: graph01_index,
                color: GREEN_COLOR,
            },
        ],
    });

    // var ctx02 = document.getElementById("간암0").getContext("2d");
    // new Chart(ctx02).Linear(barChartData_02, {
    //     range: {
    //         //그래프의 총 범위
    //         startValue: 0,
    //         endValue: graph02_index_lower + graph02_index_upper,
    //     },
    //     responsive: true,
    //     animationSteps: 1, //몇번에 걸쳐서 애니메이션을 보여줄것인가. 0: 없음, 1: 바로 보여주기
    //     axisColor: GRAY_COLOR,
    //     axisWidth: 20,
    //     axisHeight: 20,
    //     minorTicks: {
    //         interval: 1,
    //         customValues: [graph02_index_lower],
    //         height: 1,
    //         width: 15,
    //         offset: 0,
    //         color: "gray",
    //     },
    //     tickLabels: {
    //         interval: 1,
    //         customValues: [graph02_index_lower, graph02_index_upper],
    //         offset: 15, // label 높이 지정
    //         color: "gray",
    //     },
    //     geometry: "horizontal",
    //     scaleColorRanges: [
    //         // 그래프의 영역별 색깔지정
    //         {
    //             start: graph02_index_upper,
    //             end: graph02_index_lower + graph02_index_upper,
    //             color: RED_COLOR,
    //         },
    //     ],
    // });
}

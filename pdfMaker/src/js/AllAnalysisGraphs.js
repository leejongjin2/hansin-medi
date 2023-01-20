/*
Chart.js에 Range Chart가 없어서 Bar Chart를 응용한 것입니다.
수직형 barchart를 그린 후, x, y축을 반전시키고, label을 변경했습니다.

LIST_DISEAE와 TARGET_LIST에 맞추어서 CONFIG만 차지해주면 될듯
 */

const NORMAL = [0, 1];
const ATTENTION = [1, 2];
const CAUTION = [2, 3];
const ALERT = [3, 4];
const DANGER = [4, 5];

const COLOR_NORMAL = "#64D3B5";
const COLOR_ATTENTION = "#A7E55F";
const COLOR_CAUTION = "#FAE63F";
const COLOR_ALERT = "#FD871F";
const COLOR_DANGER = "#E85555";

// const target_list = ["정상", "관심", "위험", "경계", "주의", "주의"];
var cancerRanges = [];
var chronicRanges = [];

function getCancerRanges() {
    for (const key in cancers) {
        cancerRanges.push(cancers[key]["dangerRange"]);
    }
    for (const key in chronics) {
        chronicRanges.push(chronics[key]["dangerRange"]);
    }
    return cancerRanges, chronicRanges;
}

cancerRanges, (chronicRanges = getCancerRanges());

//그래프의 영역을 설정해주는 부분
function getData(target, target_pos, target_list) {
    const result = new Array(Object.keys(cancers).length);
    for (const [index, element] of target_list.entries()) {
        // result[index] = element == target ? target_pos : 0;
        if (element == target) {
            result[index] = target_pos;
        } else {
            result[index] = 0;
        }
    }

    return result;
}

const cancerData = {
    labels: Object.keys(cancers),
    datasets: [
        {
            label: "정상",
            data: getData("정상", NORMAL, cancerRanges),
            backgroundColor: COLOR_NORMAL,
        },
        {
            label: "관심",
            data: getData("관심", ATTENTION, cancerRanges),
            backgroundColor: COLOR_ATTENTION,
        },
        {
            label: "주의",
            data: getData("주의", CAUTION, cancerRanges),
            backgroundColor: COLOR_CAUTION,
        },
        {
            label: "경계",
            data: getData("경계", ALERT, cancerRanges),
            backgroundColor: COLOR_ALERT,
        },
        {
            label: "위험",
            data: getData("위험", DANGER, cancerRanges),
            backgroundColor: COLOR_DANGER,
        },
    ],
};

const cancerConfig = {
    type: "bar",
    data: cancerData,
    options: {
        animation: false,
        indexAxis: "y",
        plugins: {
            legend: {
                align: "center",
                // padding: ,
                labels: {
                    font: {
                        size: 15,
                    },
                },
                ticks: {
                    font: {
                        size: 15,
                    },
                },
            },
        },
        responsive: false,
        scales: {
            x: {
                stacked: true,
                ticks: {
                    callback: function (value) {
                        if (value == 1) return "정상";
                        else if (value == 2) return "관심";
                        else if (value == 3) return "주의";
                        else if (value == 4) return "경계";
                        else if (value == 5) return "위험";
                    },
                    display: false,
                },
                min: 0,
                max: 5,
            },
            y: {
                stacked: true,
                ticks: {
                    font: {
                        size: 15,
                    },
                },
            },
        },
    },
};

const chronicData = {
    labels: Object.keys(chronics),
    datasets: [
        {
            label: "정상",
            data: getData("정상", NORMAL, chronicRanges),
            backgroundColor: COLOR_NORMAL,
        },
        {
            label: "관심",
            data: getData("관심", ATTENTION, chronicRanges),
            backgroundColor: COLOR_ATTENTION,
        },
        {
            label: "주의",
            data: getData("주의", CAUTION, chronicRanges),
            backgroundColor: COLOR_CAUTION,
        },
        {
            label: "경계",
            data: getData("경계", ALERT, chronicRanges),
            backgroundColor: COLOR_ALERT,
        },
        {
            label: "위험",
            data: getData("위험", DANGER, chronicRanges),
            backgroundColor: COLOR_DANGER,
        },
    ],
};

const chronicConfig = {
    type: "bar",
    data: chronicData,
    options: {
        animation: false,
        indexAxis: "y",
        plugins: {
            legend: {
                align: "center",
                // padding: ,
                labels: {
                    font: {
                        size: 15,
                    },
                },
                ticks: {
                    font: {
                        size: 15,
                    },
                },
            },
        },
        responsive: false,
        scales: {
            x: {
                stacked: true,
                ticks: {
                    callback: function (value) {
                        if (value == 1) return "정상";
                        else if (value == 2) return "관심";
                        else if (value == 3) return "주의";
                        else if (value == 4) return "경계";
                        else if (value == 5) return "위험";
                    },
                    display: false,
                },
                min: 0,
                max: 5,
            },
            y: {
                stacked: true,
                ticks: {
                    font: {
                        size: 15,
                    },
                },
            },
        },
    },
};

function drawAllAnalysisGraphs() {
    const ctx01 = document.getElementById("allCancers");
    new Chart(ctx01, cancerConfig);

    const ctx02 = document.getElementById("allChronics");
    new Chart(ctx02, chronicConfig);
}

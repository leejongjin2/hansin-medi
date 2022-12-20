var NORMAL = [0, 1];
var ATTENTION = [1, 2];
var CAUTION = [2, 3];
var ALERT = [3, 4];
var DANGER = [4, 5];

var COLOR_NORMAL = "#64D3B5";
var COLOR_ATTENTION = "#A7E55F";
var COLOR_CAUTION = "#FAE63F";
var COLOR_ALERT = "#FD871F";
var COLOR_DANGER = "#E85555";

var LIST_DISEASE = ["간암", "위암", "폐암", "대장암", "갑상선암", "유방암"];
var target_list = ["정상", "관심", "위험", "경계", "주의", "주의"];

function get_data(target, target_pos, target_list) {
    const result = new Array(LIST_DISEASE.length);
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

const data = {
    labels: LIST_DISEASE,
    datasets: [
        {
            label: "정상",
            data: get_data("정상", NORMAL, target_list),
            backgroundColor: COLOR_NORMAL,
        },
        {
            label: "관심",
            data: get_data("관심", ATTENTION, target_list),
            backgroundColor: COLOR_ATTENTION,
        },
        {
            label: "주의",
            data: get_data("주의", CAUTION, target_list),
            backgroundColor: COLOR_CAUTION,
        },
        {
            label: "경계",
            data: get_data("경계", ALERT, target_list),
            backgroundColor: COLOR_ALERT,
        },
        {
            label: "위험",
            data: get_data("위험", DANGER, target_list),
            backgroundColor: COLOR_DANGER,
        },
    ],
};

const config = {
    type: "bar",
    data: data,
    options: {
        animation: false,
        // animation: {
        //     duration: 0,
        //     hover: {
        //         animationDuration: 0, // duration of animations when hovering an item
        //     },
        //     responsiveAnimationDuration: 0, // animation duration after a resize
        // },
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

function drawCanvas() {
    const ctx01 = document.getElementById("allCancers");
    new Chart(ctx01, config);

    const ctx02 = document.getElementById("allChronics");
    new Chart(ctx02, config);
}

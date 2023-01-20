var percent = 30;
function get_percent() {
    return percent;
}

function getDangerRangeImage(dangerRange) {
    if (dangerRange == "정상") {
        return "img/정상.jpg";
    } else if (dangerRange == "관심") {
        return "img/관심.jpg";
    } else if (dangerRange == "주의") {
        return "img/주의.jpg";
    } else if (dangerRange == "경계") {
        return "img/경계.jpg";
    } else if (dangerRange == "위험") {
        return "img/위험.jpg";
    } else {
        console.error("Invalid dangerRange");
    }
}

function writeHTMLs() {
    for (const cancer in cancers) {
        writeHtml(cancer, cancers[cancer], cancers[cancer]["habit"]);
    }
    for (const chronic in chronics) {
        writeHtml(chronic, chronics[chronic], chronics[chronic]["habit"]);
    }
}

/**
 * AnalysisIndex = 모든 종류 그래프 형태 확인용
 */
// function writeHTMLs() {
//     //get cancerList
//     const allCancerIndexes = getIndexPerCancers();
//     for (const cancer of Object.keys(allCancerIndexes)) {
//         writeHtml(cancer, allCancerIndexes[cancer]);
//     }
// }

// function getIndexPerCancers() {
//     const indexes = JSON.parse(JSON.stringify(AnalysisIndex));
//     if (indexes == null) {
//         console.error("No Index data");
//     }
//     return indexes;
// }

function writeHtml(disease, indexes, habit) {
    document.write("<body>");
    document.write('<div class="page">');
    document.write("<header>");
    document.write('<div class="base">');
    document.write('<div class="inner">');
    document.write('<div id="headline">OK AI CHECK</div>');
    document.write("</div>");
    document.write("</div>");
    document.write("</header>");
    document.write("<main>");
    document.write('<div class="inner">');
    document.write('<div id="title">');
    document.write("<h1>" + disease + " 위험도 분석</h1>");
    document.write("</div>");
    document.write('<section class="indexBlock">');
    document.write('<div id="warning">');
    document.write('<div id="percent">');
    document.write('<p id="percentInfo">AI예측, 5년 내 발병 위험도</p>');
    document.write('<div id="percentValue">');
    document.write(indexes["percent"] + "%");
    document.write("</div>");
    document.write("</div>");
    document.write('<a class="disableClick" href="src/">');
    document.write(
        `<img class="warningImg" id="${disease}warningImg" src="" />`
    );
    document.getElementById(disease + "warningImg").src = getDangerRangeImage(
        indexes["dangerRange"]
    );
    document.write("</a>");
    document.write("</div>");
    document.write("<hr />");
    document.write('<p id="warningInfo">');
    document.write("* 발병 위험도는 1%~99% 의 구간을 가지며 발병율이 높을");
    document.write("수록 위험도가 높다는 의미입니다. <br />");
    document.write("정상 1~20%, 관심 21~40%, 주의 41~60%, 경계 61~80%, 위험");
    document.write("81~99% 로 구분됩니다");
    document.write("</p>");
    document.write("<hr />");
    document.write("</section>");
    document.write("<h2>분석 지표</h2>");
    document.write("        ");
    document.write('<div class="indexBlock">');
    writeHTMLGraphs(disease, indexes);
    document.write("</div>");
    const graphDrawer = new GraphDrawer(disease, indexes);
    graphDrawer.drawGraphs();
    document.write("        ");
    document.write("<h2>위험도를 낮추기 위한 생활습관 가이드</h2>");
    document.write('<div class="indexBlock">');
    document.write('<p id="habitGuidance">');
    document.write(habit);
    // document.write("- 고른 식사와 규칙적 운동이 중요합니다.<br />");
    // document.write("- 지나친 음주는 삼가합니다.<br />");
    // document.write("- 흡연을 하지 않습니다.<br />");
    // document.write("- 정기적인 건강검진을 통해 간 기능을 체크합니다.<br />");
    // document.write("- B형간염 바이러스에 대한 항체가 없다면 B형간염 백신을");
    // document.write("맞습니다.<br />");
    // document.write("- 우상복부 통증, 체중감소, 피로감 등이 발견되면 의사와");
    // document.write("상의합니다.<br />");
    // document.write("- 만성 간질환의 경우 정기적인 초음파검사와 피검사를");
    // document.write("받습니다.<br />");
    document.write("</p>");
    document.write("    ");
    document.write("</div>");
    document.write("</main>");
    document.write("    ");
    document.write("<footer>");
    document.write('<div class="base">');
    document.write('<div class="inner">');
    document.write('<div id="footline">');
    document.write('<p class="desc">');
    document.write("서울대 공식 자회사 SNUAiLAB과 INFINITYCARE 공동");
    document.write("연구 개발&nbsp");
    document.write("</p>");
    document.write("    ");
    document.write('<a class="disableClick" href="src/">');
    document.write('<img id="logo" src="img/infinity_logo.png" />');
    document.write("</a>");
    document.write("    ");
    document.write('<div id="logoDesc">');
    document.write("인피니티케어<br />R&D 연구센터");
    document.write("</div>");
    document.write("</div>");
    document.write("</div>");
    document.write("</div>");
    document.write("</footer>");
    document.write("</div>");
    document.write("<!-- </div> -->");
    document.write("</body>");
    document.write("</html>");
}

function writeHTMLGraphs(disease, indexes) {
    for (let i = 1; i < 7; i++) {
        document.write('<div class="graphWrapper">');
        document.write(
            `<div class="indexName">- ${indexes["index" + i]["name"].replace(
                /\s/g,
                ""
            )}</div>`
        ); //정규표현식 : 공백제거
        document.write('<div class="indexGraph">');
        document.write(
            `<canvas id="${disease}${i}" style="width: 11cm; height:1.25cm;""></canvas>`
        );
        document.write("</div>");
        document.write("<div>" + indexes["index" + i]["value"] + "</div>");
        document.write("</div>");
    }
}

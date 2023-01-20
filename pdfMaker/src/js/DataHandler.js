var userInfo;
var cancers = {};
var chronics = {};

//여기서 데이터를 받아오면 됩니다.
function setData() {
    const data = JSON.parse(JSON.stringify(Data));
    if (data == null) {
        console.error("No Data");
    }

    userInfo = data["userInfo"];
    cancers, (chronics = getDiseases(data));
}

function getUserName() {
    return userInfo["name"];
}
function getGender() {
    return userInfo["gender"];
}
function getAge() {
    return userInfo["age"];
}
function getInspcDate() {
    return userInfo["inspcDate"];
}

function getDiseases(data) {
    for (const key in data["diseases"]) {
        if (key.endsWith("암")) {
            cancers[key] = data["diseases"][key];
            cancers[key]["dangerRange"] = setDangerRange(cancers[key]);
        } else {
            chronics[key] = data["diseases"][key];
            chronics[key]["dangerRange"] = setDangerRange(chronics[key]);
        }
    }

    return cancers, chronics;
}

function setDangerRange(data) {
    const percent = data["percent"];
    if (percent >= 0 && percent <= 20) {
        return "정상";
    } else if (percent > 20 && percent <= 40) {
        return "관심";
    } else if (percent > 40 && percent <= 60) {
        return "주의";
    } else if (percent > 60 && percent <= 80) {
        return "경계";
    } else if (percent > 80 && percent <= 100) {
        return "위험";
    } else {
        console.error("Invalid percent");
    }
}

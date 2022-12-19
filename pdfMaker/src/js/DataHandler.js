var userName = "None";
var gender = "None";
var age = "None";
var examinationDate = "None";

function setData() {
    const data = JSON.parse(JSON.stringify(User));
    if (data == null) {
        console.error("No Data");
    }
    userName = data["name"];
    gender = data["gender"];
    age = data["age"];
}

function getUserName() {
    if (userName == "None") {
        console.error("No userName Data");
    }
    return userName;
}
function getGender() {
    if (gender == "None") {
        console.error("No gender Data");
    }
    return gender;
}
function getAge() {
    if (age == "None") {
        console.error("No age Data");
    }
    return age;
}
function getExaminationDate() {
    if (examinationDate == "None") {
        console.error("No examinationDate Data");
    }
    return examinationDate;
}

var percent = 80;
function get_percent() {
    return percent;
}

function logo_info() {
    if (percent >= 1 && percent <= 20) {
        return "img/정상.jpg";
    } else if (percent > 20 && percent <= 40) {
        return "img/관심.jpg";
    } else if (percent > 40 && percent <= 60) {
        return "img/주의.jpg";
    } else if (percent > 60 && percent <= 80) {
        return "img/경계.jpg";
    } else if (percent > 80 && percent <= 99) {
        return "img/위험.jpg";
    } else {
        console.error("Invalid percent");
    }
}

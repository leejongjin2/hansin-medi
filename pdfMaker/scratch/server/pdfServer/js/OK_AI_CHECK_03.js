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

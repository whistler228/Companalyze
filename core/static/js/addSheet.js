function checkCompanyId(obj) {
    const companyId = obj.val()
    if (validCompanyId(companyId)) {
        toggleValidView(obj, "is-valid")
        return true
    } else {
        toggleValidView(obj, "is-invalid")
        return false
    }
}

function toggleValidView(obj, toState) {
    if (toState === "is-invalid") {
        obj.removeClass("is-valid")
        obj.addClass("is-invalid")
    } else if (toState === "is-valid") {
        obj.removeClass("is-invalid")
        obj.addClass("is-valid")
    }
}

function validCompanyId(companyId) {
    console.log(companyId)
    if (companyId[0] !== "r") {
        return false
    }
    if (companyId.length !== 10) {
        return false
    }
    return true
}

function getCompanyData(companyId, url) {
    url = url + "?" + $.param({companyId: companyId})
    const xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.responseType = "json";
    xhr.onload = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                setCompanyData(xhr.response)
            } else {
                console.log(xhr.statusText);
            }
        } else {
            return 0;
        }
    }

    xhr.send(null);
}

function setCompanyData(json) {
    if (json["status"] === true) {
        const data = json["data"]
        $("#addInputCompanyName").val(data["name"])
        setSubDomain(data["sub_domain"])
        setMainDomain(data["main_domain"])
        setPrefecture(data["prefecture"])
        $("#addInputFounded").val(data["year_founded"].match(/\d{4}-\d{2}/g)[0])
        $("#addInputEmployee").val(data["employee"])
        $("#addInputBenefits").val(data["benefit"])
        $("#addInputMotto").val(data["motto"])
        $("#addInputBusiness").val(data["business"])


        setLabels(data)
    } else {
        console.log("failed to get company data")
    }

    function setSubDomain(value) {
        const obj = $("#addInputSubDomain")
        const options = obj.find("option")
        value.forEach(v => {
            if (options.toArray().every(op => op.text !== v)) {
                const opt = $("<option>").text(v);
                obj.append(opt)
            }
        })
        obj.val(value)
    }

    function setMainDomain(value) {
        const obj = $("#addInputMainDomain")
        const options = obj.find("option")
        if (options.toArray().every(op => op.text !== value)) {
            const opt = $("<option>").text(value);
            obj.append(opt)
        }
        obj.val(value)
    }

    function setPrefecture(value) {
        const obj = $("#addInputPlace")
        const prefs = value.map(v => {
            if (v[v.length - 1] !== "県") {
                return v + "県"
            }
        })
        obj.val(prefs)
    }
    function setLabels(data) {
        $("#addInputCompanyName").labels().attr({"data-toggle":"tooltip", "title": data["name"]})
        $("#addInputEmployee").labels().attr({"data-toggle":"tooltip", "title": data["employee"]})
        $("#addInputCapital").labels().attr({"data-toggle":"tooltip", "title": data["capital"]})
        $("#addInputRevenue").labels().attr({"data-toggle":"tooltip", "title": data["revenue"]})
        $("#addInputWorkingTimeStart").labels().attr({"data-toggle":"tooltip", "title": data["working_time"]})
        $("#addInputWorkingTimeEnd").labels().attr({"data-toggle":"tooltip", "title": data["working_time"]})
        $("#addInputPlace").labels().attr({"data-toggle":"tooltip", "title": data["offices"]})
        $("#addInputSalary").labels().attr({"data-toggle":"tooltip", "title": data["salary"]})

        $("[data-toggle='tooltip']").tooltip()
    }
}

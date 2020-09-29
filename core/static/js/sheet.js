FAVORITE_COLOR = "favorite"
function company_list(url) {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.responseType = "json";
    xhr.onload = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                show_company_list(xhr.response)
                return xhr.response;
            } else {
                console.log(xhr.statusText);
            }
        } else {
            return 0;
        }
    }

    xhr.send(null);
}

function show_company_list(company_json) {
    const table = $("#company-list")
    company_json["company"].forEach((company, i) => {
        const list = `<a href='/sheet/${company["company_id"]}'>${company["name"]}</a>`
        const companyId = `${company["company_id"]}`
        const mainDomain = `${company["main_domain"]}`
        const subDomain = `${company["sub_domain"]}`
        let isFavorite = ""
        let favIcon = "far fa-star"
        console.log(company_json)
        if (company["is_favorite"]) {
            isFavorite = FAVORITE_COLOR
            favIcon = "fas fa-star"
        }
        const row = `<tr class="${isFavorite}">
<th scope="row">${i}</th>
<td>${list}</td>
<td>${mainDomain}</td>
<td><small>${subDomain}</small></td>
<td>
<a class="button" href="/sheet/${company['company_id']}/edit">Edit</a>
<button type="button" class="btn btn-sm btn-info" onclick='setFavorite("${companyId}", $(this))'><i class="${favIcon}"></i></button>
</td>
</tr>`;
        table.append(row);
    })
}

function setFavorite(company_id, obj) {
    obj.addClass("disabled")
    const url = "/api/toggle_favorite"
    $.getJSON(url, {companyId: company_id}, function (json) {
        obj.removeClass("disabled");
        if (json["data"]) {
            obj.parent().parent().addClass(FAVORITE_COLOR)
            obj.find("svg")[0].setAttribute("data-prefix", "fas")
        } else {
            obj.parent().parent().removeClass(FAVORITE_COLOR)
            obj.find("svg")[0].setAttribute("data-prefix", "far")
        }
    })
}
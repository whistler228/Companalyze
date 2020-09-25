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
        const mainDomain = `${company["main_domain"]}`
        const subDomain = `${company["sub_domain"]}`
        const row = `<tr class="">
<th scope="row">${i}</th>
<td>${list}</td>
<td>${mainDomain}</td>
<td><small>${subDomain}</small></td>
<td><a class="button" href="/sheet/${company['company_id']}/edit">Edit</a></td>
</tr>`;
        table.append(row);
    })
}


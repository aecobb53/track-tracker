async function pagination(target, page_size, record_size, update=false) {
    console.log('Pagination Management');
    console.log('target: ' + target);
    console.log('page_size: ' + page_size);
    console.log('record_size: ' + record_size);
    console.log('update: ' + update);

    // Div
    var pagination_div = document.getElementsByClassName('pagination-div')[0];
    pagination_div.innerHTML = '';

    // Leading
    var leading_button = document.createElement("button");
    leading_button.innerHTML = '<<';  // '&laquo;'
    leading_button.classList.add('pagination-button');
    var leading_target = target - 1;
    leading_button.setAttribute('onclick', "applyFilterForm(" + leading_target + ", " + page_size + ", " + record_size + ")");
    pagination_div.appendChild(leading_button);


    // Middle
    var min_page = Math.max(1, target - 3);
    console.log('min_page: ' + min_page);
    var max_page = Math.min(min_page + 6, Math.ceil(record_size / page_size));
    console.log('max_page: ' + max_page);

    var page_numbers = Array.from({length: max_page - min_page + 1}, (_, i) => i + min_page);
    console.log('page_numbers: ' + page_numbers);

    for (var i = 0; i < page_numbers.length; i++) {
        var page_button = document.createElement("button");
        page_button.innerHTML = page_numbers[i];
        page_button.classList.add('pagination-button');
        if (page_numbers[i] == target) {
            page_button.classList.add('active');
        }
        page_button.setAttribute('onclick', "applyFilterForm(" + page_numbers[i] + ", " + page_size + ", " + record_size + ")");
        pagination_div.appendChild(page_button);
    }


    // Trailing
    var trailing_button = document.createElement("button");
    trailing_button.innerHTML = '>>';  // '&raquo;'
    trailing_button.classList.add('pagination-button');
    var trailing_target = target + 1;
    trailing_button.setAttribute('onclick', "applyFilterForm(" + trailing_target + ", " + page_size + ", " + record_size + ")");
    pagination_div.appendChild(trailing_button);
    console.log('Pagination Management Complete');

    if (update) {
        console.log('Updating Table');
        await applyFilterForm(target);
    }
}

// window.onload = pagination();

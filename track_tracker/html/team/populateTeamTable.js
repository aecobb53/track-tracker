async function populateTeamTable(filterResults, page, page_size, page_count) {
    console.log('Populating Team table');

    var skipColumnArray = ['results', 'records', 'uid'];

    // DIV
    console.log('Clearing table...');
    var table_div = document.getElementById('table-div');
    table_div.innerHTML = '';

    // TABLE
    var table_element = document.createElement('table');
    // table_element.style.width = '100%';
    // table_element.style.height = '100%';
    // table_element.style.border = '5px solid black';

    if (filterResults.length == 0) {
        // No results
        var table_item = document.createElement('th');
        table_item.innerHTML = 'No results found';

        var table_row = document.createElement('tr');
        table_row.appendChild(table_item);

        var table_header = document.createElement('thead');
        // table_header.style.width = '100%';
        // table_header.style.fontWeight = 'bold';
        // table_header.style.padding = '5px';
        table_header.appendChild(table_row);

        table_element.appendChild(table_header);
        table_div.appendChild(table_element);
        return;
    }

    // HEADER
    var table_header = document.createElement('thead');
    // table_header.style.width = '100%';
    // table_header.style.fontWeight = 'bold';
    // table_header.style.padding = '5px';
    var header_values = Object.keys(filterResults[0]);
    var table_row = document.createElement('tr');
    for(var i = 0; i < header_values.length; i++) {
        if (skipColumnArray.includes(header_values[i])) {
            break;
        }
        var class_name = header_values[i].toLowerCase().replaceAll(' ', '-') + '-data';
        var table_item = document.createElement('th');
        table_item.innerHTML = header_values[i];
        table_item.classList.add(class_name);
        table_row.appendChild(table_item);
    }
    table_header.appendChild(table_row);
    table_element.appendChild(table_header);

    // console.log('HERE 1');
    // console.log(filterResults.length);

    // var condensed_list = {};
    // for(var i = 0; i < condensed_list.length; i++) {
    //     console.log('HERE 2');
    //     console.log(filterResults[i]);
    //     for (const [key, value] of Object.entries(filterResults[i])) {
    //         if (key == 'Athlete Count') {
    //             console.log('Athlete Count');
    //             console.log(value);
    //             if (value <= 10) {
    //                 continue;
    //             }
    //         }
    //         else {
    //             condensed_list[key] = value;
    //         }
    //     }
    // }

    var condensed_list = [];
    for(var i = 0; i < filterResults.length; i++) {
        console.log('HERE 2');
        console.log(filterResults[i]);
        console.log(filterResults[i]['Athlete Count']);
        if (filterResults[i]['Athlete Count'] >= 2) {
            condensed_list.push(filterResults[i]);
        }
    }




    // BODY
    var table_body = document.createElement('tbody');
    for(var i = 0; i < filterResults.length; i++) {
        // for(var i = 0; i < condensed_list.length; i++) {
        // ROW
        var table_row = document.createElement('tr');
        // table_row.style.padding = '5px';

        // Data
        for (const [key, value] of Object.entries(filterResults[i])) {
        // for (const [key, value] of Object.entries(filterResults[i])) {

            if (skipColumnArray.includes(key)) {
                break;
            }
            var class_name = key.toLowerCase().replaceAll(' ', '-') + '-data';
            var table_item = document.createElement('td');
            table_item.classList.add(class_name);


            if (key == 'Team') {
                // Link to athlete page
                table_item.innerHTML = '<a class="team-link" href="' + value + '">' +
                value + '</a>';
            } else {
                table_item.innerHTML = value;
            }
            table_row.appendChild(table_item);
        }

        // Additional Formatting
        if(i % 2 == 0) {
            table_row.classList.add('even-row');
            // table_row.style.backgroundColor = '#2c2d2e';
        }
        else {
            table_row.classList.add('odd-row');
            // table_row.style.backgroundColor = '#35363b';
        }
        table_body.appendChild(table_row);
    }

    table_element.appendChild(table_body);
    table_div.appendChild(table_element);

    // Pagination
    pagination(page, page_size, page_count, false);

}
// window.onload = populateTable();

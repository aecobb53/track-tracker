async function populateAthleteTable(filterResults, page, page_size, page_count) {
    console.log('Populating Athlete table');

    // var tracking_project_name_hashtable = {};

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

    console.log('Creating table header');
    console.log(filterResults[0]);


    var header_values = Object.keys(filterResults[0]);
    var table_row = document.createElement('tr');
    for(var i = 0; i < header_values.length; i++) {
        console.log('HEADER VALUE: ' + header_values[i]);
        if (skipColumnArray.includes(header_values[i])) {
            console.log('Skipping column: ' + header_values[i]);
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

    // BODY
    var table_body = document.createElement('tbody');
    for(var i = 0; i < filterResults.length; i++) {
        // ROW
        var table_row = document.createElement('tr');
        // table_row.style.padding = '5px';

        // Data
        for (const [key, value] of Object.entries(filterResults[i])) {

            if (skipColumnArray.includes(key)) {
                // continue;
                break;
            }
            var class_name = key.toLowerCase().replaceAll(' ', '-') + '-data';
            var table_item = document.createElement('td');
            // table_item.style.padding = '1px 25px';
            table_item.classList.add(class_name);

            console.log(filterResults[i]);

            if (key == 'First Name') {
                // Link to athlete page
                table_item.innerHTML = '<a class="athlete-link" href="' + filterResults[i]['uid'] + '">' +
                value + '</a>';
                // table_item.classList.add('athlete-link');
            } else if (key == 'Last Name') {
                // Link to athlete page
                table_item.innerHTML = '<a class="athlete-link" href="' + filterResults[i]['uid'] + '">' +
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
            // table_row.style.backgroundColor = '#35363b';
            table_row.classList.add('odd-row');
        }
        table_body.appendChild(table_row);
    }

    table_element.appendChild(table_body);
    table_div.appendChild(table_element);

    // Pagination
    pagination(page, page_size, page_count, false);
}
// window.onload = populateTable();

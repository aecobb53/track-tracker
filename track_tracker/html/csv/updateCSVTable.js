async function updateCSVTable(csv_data) {
    console.log('Populating Athlete table');
    var csv = csv_data['csv'];
    var csv_update = csv_data['csv_update'];
    if (csv_update.length > 0) {
        console.log('Updating CSV Table');
    } else {
        console.log('Populating CSV');

        // DIV
        console.log('Clearing table...');
        var table_div = document.getElementById('table-div');
        table_div.innerHTML = '';

        // TABLE
        var table_element = document.createElement('table');

        // No Data

        // Populating
        for (var i = 0; i < csv.length; i++) {
            // console.log('Row ' + i + ': ' + JSON.stringify(csv[i]));
            var table_row = document.createElement('tr');
            for (var key in csv[i]) {
                var table_item = document.createElement('td');
                var input = document.createElement('input');
                input.type = 'text';
                input.value = csv[i][key];
                input.setAttribute('onchange', "runUpdate()");
                table_item.appendChild(input);
                table_row.appendChild(table_item);
            }
            table_element.appendChild(table_row);
        }
        table_div.appendChild(table_element);

    }
}

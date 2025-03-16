async function populateCSV() {
    console.log('Populating CSV');

    var csv = [];

    // DIV
    var table_rows = document.getElementsByTagName('tr');
    for (var i = 0; i < table_rows.length; i++) {
        var table_row = table_rows[i];
        var table_items = table_row.getElementsByTagName('td');
        var row_data = [];
        for (var j = 0; j < table_items.length; j++) {
            var table_item = table_items[j];
            var input = table_item.getElementsByTagName('input')[0];
            if (input) {
                row_data.push(input.value);
            } else {
                row_data.push('');
            }
        }
        csv.push(row_data);
    }
    return csv
}

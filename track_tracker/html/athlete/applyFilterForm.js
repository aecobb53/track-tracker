async function applyFilterForm(page=1, page_size=null, record_size=null) {
    console.log('Applying Filter Form');
    console.log('page: ' + page);
    console.log('page_size: ' + page_size);
    console.log('record_size: ' + record_size);
    var params = {};

    let filterLabel = document.getElementsByClassName("filter-label");
    for ( i = 0; i < filterLabel.length; i++) {
        let inputTag = filterLabel[i].getElementsByClassName("filter-select")[0];

        let key = inputTag.id.replaceAll('-', '_').replace('_input', '');
        key = key.replace('_select', '');
        let old_value = params[key] || '';
        let data_value = '';
        if (old_value != '') {
            data_value = old_value + ',';
        }

        if (inputTag.value != "") {
            let inputModifier = filterLabel[i].getElementsByTagName("select")[0];
                if (inputModifier != undefined && !inputModifier.classList.contains('standalone-select')) {
                console.log(inputModifier);
                data_value = data_value + inputModifier.value;
            }
            data_value = data_value + inputTag.value;
        }
        params[key] = data_value;
    }

    let arrangeLabel = document.getElementsByClassName("arrange-label");
    for ( i = 0; i < arrangeLabel.length; i++) {
        let inputTag = arrangeLabel[i].getElementsByClassName("arrange-select")[0];

        let key = inputTag.id.replaceAll('-', '_').replace('_input', '');
        key = key.replace('_select', '');
        let old_value = params[key] || '';
        let data_value = '';
        if (old_value != '') {
            data_value = old_value + ',';
        }

        if (inputTag.value != "") {
            let inputModifier = arrangeLabel[i].getElementsByTagName("select")[0];
                if (inputModifier != undefined && !inputModifier.classList.contains('standalone-select')) {
                console.log(inputModifier);
                data_value = data_value + inputModifier.value;
            }
            data_value = data_value + inputTag.value;
        }
        params[key] = data_value;

        if (key == 'limit') {
            page_size = inputTag.value;
        }
    }

    var offset = page - 1;
    offset = offset * page_size;
    params['offset'] = offset
    const queryResults = await GETFilterAthlete(params);

    filterResults = queryResults['athletes'];
    query_max_count = queryResults['query_max_count'];
    console.log('Max result count:' + query_max_count);
    console.log('len: ' + filterResults.length);
    page_count = Math.round(query_max_count / page_size);
    console.log('Page count: ' + page_count);

    populateAthleteTable(filterResults, page, page_size, page_count);
    applyDisplayFilters();
}

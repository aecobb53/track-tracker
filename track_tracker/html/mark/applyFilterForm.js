async function applyFilterForm() {
    console.log('Applying Filter Form');
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
    }


    const filterResults = await GETFilterMark(params);

    populateMarkTable(filterResults);
    applyDisplayFilters();
}

async function applyFilterForm() {
    console.log('Applying Filter Form');
    var params = {};
    let filterLabel = document.getElementsByClassName("filter-label");
    for ( i = 0; i < filterLabel.length; i++) {
        let inputTag = filterLabel[i].getElementsByTagName("input")[0];

        // console.log('OLD VALUE');
        let key = inputTag.id.replaceAll('-', '_').replace('_input', '');
        // console.log('Key: ' + key);
        let old_value = params[key] || '';
        // console.log('OLD VALUE: ' + old_value);
        let data_value = '';
        if (old_value != '') {
            // console.log('Looking for Key: ' + key);
            // console.log('OLD Value: ' + old_value);
            // console.log('looking at old value: ' + old_value.value);
            data_value = old_value + ',';
        // } else {
        //     console.log('No old value found');
        }

        // console.log('DATA VALUE: ' + data_value);
        // console.log('INPUT TAG: ' + inputTag.value);



        if (inputTag.value != "") {
            // console.log('INPUT TAG FOUND');
            // let data_value = inputTag.value;
            let inputModifier = filterLabel[i].getElementsByTagName("select")[0];
            if (inputModifier != undefined) {
                console.log(inputModifier);
                data_value = data_value + inputModifier.value;
                // params[inputTag.id.replaceAll('-', '_').replace('_input', '')] = data_value;
            }
            data_value = data_value + inputTag.value;
            // console.log('DATA VALUE: ' + data_value);
        }


        params[key] = data_value;
    }
    const filterResults = await GETFilterAthlete(params);

    populateMarkTable(filterResults);
    applyDisplayFilters();
}

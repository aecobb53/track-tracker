async function applyFilterForm() {
    console.log('Applying Filter Form');
    var params = {};
    let filterLabel = document.getElementsByClassName("filter-label");
    for ( i = 0; i < filterLabel.length; i++) {
        let inputTag = filterLabel[i].getElementsByTagName("input")[0];
        params[inputTag.id.replaceAll('-', '_').replace('_input', '')] = inputTag.value;
    }

    const filterResults = await GETFilterMark(params);

    populateMarkTable(filterResults);
    // applyDisplayFilters();
}

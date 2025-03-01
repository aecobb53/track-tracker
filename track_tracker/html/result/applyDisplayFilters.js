async function applyDisplayFilters() {
    console.log('Applying Display Filters');
    let displayCheckboxInput = document.getElementsByClassName("display-checkbox-input");
    // console.log('displayCheckboxInput:');
    // console.log(displayCheckboxInput);
    for ( i = 0; i < displayCheckboxInput.length; i++) {
        // console.log(displayCheckboxInput[i]);
        // console.log(displayCheckboxInput[i].checked);
        let displayCheckboxData = document.getElementsByClassName(displayCheckboxInput[i].id.replace('-input', '-data'));
        // console.log('displayCheckboxData:');
        // console.log(displayCheckboxData);
        for ( ii = 0; ii < displayCheckboxData.length; ii++) {
            if (displayCheckboxInput[i].checked) {
                displayCheckboxData[ii].style.display = "";
            } else {
                displayCheckboxData[ii].style.display = "none";
            }
        }
    }
}

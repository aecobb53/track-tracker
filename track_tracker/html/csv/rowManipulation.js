function addAthlete(rowIndex, athleteIndex) {
    console.log('Adding Athlete Slot: ' + rowIndex + ', ' + athleteIndex);
}

function removeAthlete(rowIndex, athleteIndex) {
    console.log('Removing Athlete Slot: ' + rowIndex + ', ' + athleteIndex);
}

function addEvent(rowIndex) {
    console.log('Adding Event Slot: ' + rowIndex);
    // DIV
    var table_div = document.getElementById('meet-table');
    // console.log(table_div);
    var dataRows = table_div.getElementsByClassName('meet-row');
    for (var i = 0; i < dataRows.length - 1; i++) {
        console.log('');
        console.log(i);
        console.log(dataRows[i]);
        if (i === rowIndex) {
            console.log('MATCH: ' + i);

            table_div.children[i+1].insertAdjacentElement('afterend', dataRows[i+1].cloneNode(true));
        }
    }
}

function removeEvent(rowIndex) {
    console.log('Removing Event Slot: ' + rowIndex);
    // DIV
    var table_div = document.getElementById('meet-table');
    // console.log(table_div);
    var dataRows = table_div.getElementsByClassName('meet-row');
    for (var i = 0; i < dataRows.length; i++) {
        console.log('');
        console.log(i);
        console.log(dataRows[i]);
        if (i === rowIndex) {
            console.log('MATCH: ' + i);

            table_div.removeChild(dataRows[i]);
            runUpdate();

            // table_div.children[i+1].insertAdjacentElement('afterend', dataRows[i+1].cloneNode(true));
        }
    }
    // runUpdate();
}

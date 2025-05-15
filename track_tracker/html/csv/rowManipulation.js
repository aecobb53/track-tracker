function addMSAthlete(rowIndex, athleteIndex) {
    console.log('Adding MSAthlete Slot: ' + rowIndex + ', ' + athleteIndex);
    if (athleteIndex === undefined) {
        athleteIndex = 0;
    }
    // DIV
    var table_div = document.getElementById('meet-table');
    var dataRows = table_div.getElementsByClassName('meet-row');

    for (var i = 0; i < dataRows.length - 1; i++) {
        if (i === rowIndex) {
            var athleteColumn = dataRows[i].children[2];
            for (var j = 0; j < athleteColumn.children.length; j++) {
                if (j === athleteIndex) {
                    addSpecificMSAthlete(dataRows[i], 2, athleteIndex);
                    addSpecificMSAthlete(dataRows[i], 3, athleteIndex);
                    addSpecificMSAthlete(dataRows[i], 4, athleteIndex);
                    addSpecificMSAthlete(dataRows[i], 5, athleteIndex);
                    addSpecificMSAthlete(dataRows[i], 6, athleteIndex);
                    addSpecificMSAthlete(dataRows[i], 7, athleteIndex);
                    addSpecificMSAthlete(dataRows[i], 8, athleteIndex);
                }
            }
        }
    }
    runUpdate();
}

function removeMSAthlete(rowIndex, athleteIndex) {
    console.log('Removing MSAthlete Slot: ' + rowIndex + ', ' + athleteIndex);
    // DIV
    var table_div = document.getElementById('meet-table');
    var dataRows = table_div.getElementsByClassName('meet-row');
    for (var i = 0; i < dataRows.length - 1; i++) {
        if (i === rowIndex) {
            removeSpecificMSAthlete(dataRows[i], 2, athleteIndex);
            removeSpecificMSAthlete(dataRows[i], 3, athleteIndex);
            removeSpecificMSAthlete(dataRows[i], 4, athleteIndex);
            removeSpecificMSAthlete(dataRows[i], 5, athleteIndex);
            removeSpecificMSAthlete(dataRows[i], 6, athleteIndex);
            removeSpecificMSAthlete(dataRows[i], 7, athleteIndex);
            removeSpecificMSAthlete(dataRows[i], 8, athleteIndex);
            removeSpecificMSAthlete(dataRows[i], 9, athleteIndex);
            removeSpecificMSAthlete(dataRows[i], 10, athleteIndex);
        }
    }
    runUpdate();
}

function addEvent(rowIndex) {
    console.log('Adding Event Slot: ' + rowIndex);
    // DIV
    var table_div = document.getElementById('meet-table');
    // console.log(table_div);
    var dataRows = table_div.getElementsByClassName('meet-row');
    for (var i = 0; i < dataRows.length - 1; i++) {
        // console.log('');
        // console.log(i);
        // console.log(dataRows[i]);
        if (i === rowIndex) {
            // console.log('MATCH: ' + i);

            table_div.children[i].insertAdjacentElement('afterend', dataRows[i].cloneNode(true));
        }
    }
    runUpdate();
}

function removeEvent(rowIndex) {
    console.log('Removing Event Slot: ' + rowIndex);
    // DIV
    var table_div = document.getElementById('meet-table');
    // console.log(table_div);
    var dataRows = table_div.getElementsByClassName('meet-row');
    for (var i = 0; i < dataRows.length; i++) {
        // console.log('');
        // console.log(i);
        // console.log(dataRows[i]);
        if (i === rowIndex) {
            // console.log('MATCH: ' + i);

            table_div.removeChild(dataRows[i]);
            runUpdate();

            // table_div.children[i+1].insertAdjacentElement('afterend', dataRows[i+1].cloneNode(true));
        }
    }
    runUpdate();
}




function addSpecificMSAthlete(containingDiv, columnIndex, athleteIndex) {
    // DIV
    var athleteColumn = containingDiv.children[columnIndex];
    for (var j = 0; j < athleteColumn.children.length; j++) {
        if (j === athleteIndex) {
            var meetItem = createMeetInputItem(['-']);
            athleteColumn.insertBefore(meetItem, athleteColumn.children[j]);
        }
    }
}


function removeSpecificMSAthlete(containingDiv, columnIndex, athleteIndex) {
    // DIV
    var meetItem = containingDiv.getElementsByClassName('meet-item');
    for (var i = 0; i < meetItem.length; i++) {
        if (i === columnIndex) {
            var eventColumns = meetItem[i].getElementsByClassName('event-data-row');
            for (var j = 0; j < eventColumns.length; j++) {
                if (j === athleteIndex) {
                    eventColumns[j].removeChild(eventColumns[j].children[0]);
                }
            }
        }
    }
}

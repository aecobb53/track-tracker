function addAthlete(rowIndex, athleteIndex) {
    console.log('Adding Athlete Slot: ' + rowIndex + ', ' + athleteIndex);
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
                    addSpecificAthlete(dataRows[i], 2, athleteIndex);
                    addSpecificAthlete(dataRows[i], 3, athleteIndex);
                    addSpecificAthlete(dataRows[i], 4, athleteIndex);
                    addSpecificAthlete(dataRows[i], 5, athleteIndex);
                    addSpecificAthlete(dataRows[i], 6, athleteIndex);
                    addSpecificAthlete(dataRows[i], 7, athleteIndex);
                    addSpecificAthlete(dataRows[i], 8, athleteIndex);
                }
            }
        }
    }
    runUpdate();
}

function removeAthlete(rowIndex, athleteIndex) {
    console.log('Removing Athlete Slot: ' + rowIndex + ', ' + athleteIndex);
    // DIV
    var table_div = document.getElementById('meet-table');
    var dataRows = table_div.getElementsByClassName('meet-row');
    for (var i = 0; i < dataRows.length - 1; i++) {
        if (i === rowIndex) {
            removeSpecificAthlete(dataRows[i], 2, athleteIndex);
            removeSpecificAthlete(dataRows[i], 3, athleteIndex);
            removeSpecificAthlete(dataRows[i], 4, athleteIndex);
            removeSpecificAthlete(dataRows[i], 5, athleteIndex);
            removeSpecificAthlete(dataRows[i], 6, athleteIndex);
            removeSpecificAthlete(dataRows[i], 7, athleteIndex);
            removeSpecificAthlete(dataRows[i], 8, athleteIndex);
            removeSpecificAthlete(dataRows[i], 9, athleteIndex);
            removeSpecificAthlete(dataRows[i], 10, athleteIndex);
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




function addSpecificAthlete(containingDiv, columnIndex, athleteIndex) {
    // DIV
    var athleteColumn = containingDiv.children[columnIndex];
    for (var j = 0; j < athleteColumn.children.length; j++) {
        if (j === athleteIndex) {
            var meetItem = createMeetInputItem(['-']);
            athleteColumn.insertBefore(meetItem, athleteColumn.children[j]);
        }
    }
}


function removeSpecificAthlete(containingDiv, columnIndex, athleteIndex) {
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

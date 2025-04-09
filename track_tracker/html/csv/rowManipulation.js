function addAthlete(rowIndex, athleteIndex) {
    console.log('Adding Athlete Slot: ' + rowIndex + ', ' + athleteIndex);
    // DIV
    var table_div = document.getElementById('meet-table');
    var dataRows = table_div.getElementsByClassName('meet-row');

    for (var i = 0; i < dataRows.length - 1; i++) {
        if (i === rowIndex) {
            // console.log('ROW MATCH: ' + i);
            // console.log(dataRows[i]);
            var athleteColumn = dataRows[i].children[2];
            // console.log(athleteColumn);
            for (var j = 0; j < athleteColumn.children.length; j++) {
                // console.log(athleteColumn.children[j]);
                if (j === athleteIndex) {
                    // console.log('ATHLETE MATCH: ' + j);
                    // console.log(athleteColumn.children[j]);
                    // var meetItem = createMeetInputItem(['-']);
                    // console.log(meetItem);
                    // athleteColumn.insertBefore(meetItem, athleteColumn.children[j]);

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
    // console.log(table_div);
    var dataRows = table_div.getElementsByClassName('meet-row');
    for (var i = 0; i < dataRows.length - 1; i++) {
        // console.log('');
        // console.log(i);
        // console.log(dataRows[i]);
        if (i === rowIndex) {
            console.log('ROW MATCH: ' + i);
            console.log(dataRows[i]);
            removeSpecificAthlete(dataRows[i], 2, athleteIndex);
            removeSpecificAthlete(dataRows[i], 3, athleteIndex);
            removeSpecificAthlete(dataRows[i], 4, athleteIndex);
            removeSpecificAthlete(dataRows[i], 5, athleteIndex);
            removeSpecificAthlete(dataRows[i], 6, athleteIndex);
            removeSpecificAthlete(dataRows[i], 7, athleteIndex);
            removeSpecificAthlete(dataRows[i], 8, athleteIndex);
            removeSpecificAthlete(dataRows[i], 9, athleteIndex);
            removeSpecificAthlete(dataRows[i], 10, athleteIndex);

            // for (var j = 0; j < dataRows[i][2].children.length; j++) {
            //     console.log('J: ' + j);
            //     console.log(dataRows[i].children[j]);
            //     if (j === athleteIndex) {
            //         console.log('MATCH: ' + j);
            //         console.log(dataRows[i].children[j]);
            //         // dataRows[i].removeChild(dataRows[i].children[j]);
            //         dataRows[i].children[j].style.backgroundColor = 'red';
            //     }
            // }

            // for (var j = 0; j < dataRows[i].children.length; j++) {
            //     // console.log('J: ' + j);
            //     // console.log(dataRows[i].children[j]);
            //     if (j === athleteIndex) {
            //     console.log(dataRows[i].children[j]);
            //         console.log('MATCH: ' + j);
            //         console.log(dataRows[i].children[j]);
            //         // dataRows[i].removeChild(dataRows[i].children[j]);
            //         dataRows[i].children[j].style.backgroundColor = 'red';
            //     }
            // }

            // table_div.children[i+1].insertAdjacentElement('afterend', dataRows[i+1].cloneNode(true));
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




function addSpecificAthlete(containingDiv, columnIndex, athleteIndex) {
    console.log('Adding Athlete Slot: ' + athleteIndex);

    // DIV
    // console.log('ROW MATCH: ' + i);
    // console.log(dataRows[i]);
    var athleteColumn = containingDiv.children[columnIndex];
    // // console.log(athleteColumn);
    for (var j = 0; j < athleteColumn.children.length; j++) {
        // console.log(athleteColumn.children[j]);
        if (j === athleteIndex) {
            console.log('ATHLETE MATCH: ' + j);
            console.log(athleteColumn.children[j]);
            var meetItem = createMeetInputItem(['-']);
            console.log(meetItem);
            athleteColumn.insertBefore(meetItem, athleteColumn.children[j]);
        }
    }
}


function removeSpecificAthlete(containingDiv, columnIndex, athleteIndex) {
    // console.log('Removing Athlete Slot: ' + athleteIndex);

    // DIV
    console.log(containingDiv);
    var meetItem = containingDiv.getElementsByClassName('meet-item');
    console.log(meetItem);
    for (var i = 0; i < meetItem.length; i++) {
        if (i === columnIndex) {
            var eventColumns = meetItem[i].getElementsByClassName('event-data-row');
            console.log(eventColumns);
            for (var j = 0; j < eventColumns.length; j++) {
                if (j === athleteIndex) {
                    console.log('ATHLETE MATCH: ' + j);
                    console.log(eventColumns[j]);
                    eventColumns[j].removeChild(eventColumns[j].children[0]);
                    // containingDiv.removeChild(containingDiv.children[j]);
                    // eventColumns[j].style.backgroundColor = 'red';
                    // eventColumns[j].style.padding = '10px';
                }
            }
        }
    }
}

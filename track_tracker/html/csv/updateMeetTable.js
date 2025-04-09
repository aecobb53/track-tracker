function createMeetInputItem(value, added_div_class, added_input_class) {
    var input_div = document.createElement('div');
    var input = document.createElement('input');
    input.type = 'text';
    input.value = value;
    input.setAttribute('onchange', "runUpdate()");
    if (added_input_class) {
        input.className = added_input_class;
    }
    if (added_div_class) {
        input_div.className = added_div_class;
    }
    input_div.classList.add('event-data-row');
    input_div.appendChild(input);
    return input_div;
}

function createMeetDivItem(value, added_class) {
    var input_div = document.createElement('div');
    var input = document.createElement('div');
    // input.type = 'text';
    input.innerHTML = value;
    // input.value = value;
    // input.setAttribute('onchange', "runUpdate()");
    input_div.className = added_class;
    input_div.classList.add('event-data-row');
    input_div.appendChild(input);
    return input_div;
}

function createMeetItem(value, validation = null, input = true) {
    if (!validation) {
        validation = [];
        for (var i = 0; i < value.length; i++) {
            validation.push('SKIP');
        }
    }
    var item = document.createElement('div');
    item.className = 'meet-item';
    for (var i = 0; i < value.length; i++) {
        if (validation[i] != null && validation[i] != 'SKIP') {
            // Validated value
            if (input) {
                var val = createMeetInputItem(value[i], null, 'validated');
            } else {
                var val = createMeetDivItem(value[i], 'validated');
            }
            // val = val + ' ☑';
        } else if (validation[i] == 'SKIP') {
            // Generic header
            if (input) {
                var val = createMeetInputItem(value[i]);
            } else {
                var val = createMeetDivItem(value[i]);
            }
        } else {
            // Value that is not validated by the database
            if (value[i] == '' || value[i] == null || value[i] == '-') {
                if (input) {
                    var val = createMeetInputItem(value[i]);
                } else {
                    var val = createMeetDivItem(value[i]);
                }
            } else {
                if (input) {
                    var val = createMeetInputItem(value[i], null, 'partially-validated');
                } else {
                    var val = createMeetDivItem(value[i], 'partially-validated');
                }
            }
            // val = val + ' ☒';
        }
        item.appendChild(val, 'meet-item');
        // if (input) {
        //     item.appendChild(val, 'meet-item');
        // } else {
        //     item.appendChild(val, 'meet-item');
        // }
    }
    return item;
}


function createMeetButtonItem(value, added_class, functionText) {
    var button_div = document.createElement('div');
    var button = document.createElement('button');
    button.innerHTML = value;
    button.setAttribute('onclick', functionText);
    button_div.className = added_class;
    button_div.appendChild(button);
    button_div.classList.add('event-data-row');
    return button_div;
}

function createMeetRowManipulation(value, buttonText, functionName, rowIndex) {
    var item = document.createElement('div');
    if (value.length === 1) {
        item.className = 'meet-item';
        for (var i = 0; i < value.length; i++) {
            item.appendChild(createMeetButtonItem(buttonText, 'meet-item', functionName + '(' + rowIndex + ')'));
        }
    } else {
        item.className = 'meet-item';
        for (var i = 0; i < value.length; i++) {
            item.appendChild(createMeetButtonItem(buttonText, 'meet-multiline-item', functionName + '(' + rowIndex + ', ' + i + ')'));
        }
    }
    return item;
}


function createMeetRow(event, index) {
    var table_row = document.createElement('div');
    table_row.className = 'meet-row';

    // Time
    var time_item = createMeetItem([event['time']]);
    time_item.classList.add('col-width-time');
    table_row.appendChild(time_item);

    // Event
    var event_item = createMeetItem([event['event']]);
    event_item.classList.add('col-width-event');
    table_row.appendChild(event_item);

    // Athletes
    var athlete_item = createMeetItem(
        event['athletes'].map(a => a['name']),
        event['athletes'].map(a => a['athlete_uid'])
    );
    athlete_item.classList.add('col-width-athlete');
    table_row.appendChild(athlete_item);

    // Heat Late Flight
    var athlete_item = createMeetItem(event['athletes'].map(a => a['Heat/Lane/Flight']));
    athlete_item.classList.add('col-width-heat');
    table_row.appendChild(athlete_item);

    // Seed
    var athlete_item = createMeetItem(
        event['athletes'].map(a => a['seed']),
        event['athletes'].map(a => a['seed_uid'])
    );
    athlete_item.classList.add('col-width-seed');
    table_row.appendChild(athlete_item);

    // Time/Mark
    var athlete_item = createMeetItem(
        event['athletes'].map(a => a['result']),
        event['athletes'].map(a => a['result_uid'])
    );
    athlete_item.classList.add('col-width-result');
    table_row.appendChild(athlete_item);

    // Place
    var athlete_item = createMeetItem(event['athletes'].map(a => a['place']));
    athlete_item.classList.add('col-width-place');
    table_row.appendChild(athlete_item);

    // New PR
    var athlete_item = createMeetItem(event['athletes'].map(a => a['pr']), null, false);
    athlete_item.classList.add('col-width-pr');
    table_row.appendChild(athlete_item);

    // Points
    var athlete_item = createMeetItem(event['athletes'].map(a => a['points']), null, false);
    athlete_item.classList.add('col-width-points');
    table_row.appendChild(athlete_item);





    // Athlete Row Manipulation
    // Add Athlete
    var button_item = createMeetRowManipulation(event['athletes'].map(a => a['result']), 'Add Athlete', 'addAthlete', index + 1);
    button_item.classList.add('col-width-button');
    table_row.appendChild(button_item);

    // Remove Athlete
    var button_item = createMeetRowManipulation(event['athletes'].map(a => a['result']), 'Remove Athlete', 'removeAthlete', index + 1);
    button_item.classList.add('col-width-button');
    table_row.appendChild(button_item);

    // Add Event
    var button_item = createMeetRowManipulation([null], 'Add Event', 'addEvent', index + 1);
    button_item.classList.add('col-width-button');
    table_row.appendChild(button_item);

    // Remove Event
    var button_item = createMeetRowManipulation([null], 'Remove Event', 'removeEvent', index + 1);
    button_item.classList.add('col-width-button');
    table_row.appendChild(button_item);


    return table_row;
}

async function updateMeetTable(meet_data) {
    // console.log('Populating Meet table');
    var data_timestamp = meet_data['data_timestamp'];
    var meet_specific_data = meet_data['meet_data'];
    var event_header = meet_data['event_header'];
    var event_data = meet_data['event_data'];
    var meet_data_update = meet_data['meet_data_update'];

    // DIV
    var udpate_datetime_element = document.getElementById('page-identifier-update-time');
    udpate_datetime_element.innerHTML = data_timestamp;
    udpate_datetime_element.setAttribute('hidden', '');


    // var csv = csv_data['csv'];
    // var meet_data_update = csv_data['meet_data_update'];
    if (meet_data_update.length > 0) {
        console.log('Updating CSV Table');
    } else {
        console.log('Populating CSV');

        // DIV
        var table_div = document.getElementById('meet-table');
        table_div.innerHTML = '';

        // Header
        var table_row = document.createElement('div');
        table_row.className = 'meet-row';
        for (var i = 0; i < event_header.length; i++) {
            var header_item = createMeetItem([event_header[i]['name']], false);
            header_item.classList.add(event_header[i]['class']);
            table_row.appendChild(header_item);
        }
        table_div.appendChild(table_row);

        // Data
        for (var i = 0; i < event_data.length; i++) {
            row = createMeetRow(event_data[i], i);
            table_div.appendChild(row);
        }
    }
}

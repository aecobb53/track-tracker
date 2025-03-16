function returnRowInputValue(row) {
    // console.log('Returning Row Input Value');
    // console.log(row);
    var inputs = row.getElementsByTagName('input');
    if (inputs.length > 0) {
        var items = [];
        for (var i = 0; i < inputs.length; i++) {
            items.push(inputs[i].value);
        }
        return items;
    }
    // if (inputs.length == 1) {
    //     return inputs[0].value;
    // } else if (inputs.length > 0) {
    //     var items = [];
    //     for (var i = 0; i < inputs.length; i++) {
    //         items.push(inputs[i].value);
    //     }
    //     return items;
    // }
    return '';
}

async function createMeetUpdateBody() {
    console.log('Creating Meet Update Body');

    var events = [];

    var event_rows = document.getElementsByClassName('meet-row');
    var events_list = [];
    for (var i = 0; i < event_rows.length; i++) {
        var event_row_dict = {};
        var event_items = event_rows[i].getElementsByClassName('meet-item');
        for (var j = 0; j < event_items.length; j++) {
            // Time
            event_row_dict['time'] = returnRowInputValue(event_items[0]);

            // Event
            event_row_dict['event'] = returnRowInputValue(event_items[1]);

            // Athletes
            event_row_dict['athletes'] = returnRowInputValue(event_items[2]);

            // Heat Late Flight
            event_row_dict['heats'] = returnRowInputValue(event_items[3]);

            // Seed
            event_row_dict['seeds'] = returnRowInputValue(event_items[4]);

            // Time/Mark
            event_row_dict['result'] = returnRowInputValue(event_items[5]);

            // Place
            event_row_dict['place'] = returnRowInputValue(event_items[6]);
        }
        // console.log('Event Row Dict: ');
        // console.log(event_row_dict);
        if (event_row_dict['event'] != '') {
            events_list.push(event_row_dict);
        };
    }
    // events_list.pop(0);
    // delete events_list[0];
    // delete events_list[0];
    console.log('Event List: ');
    console.log(events_list);
    return events_list;
}

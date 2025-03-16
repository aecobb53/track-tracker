async function runUpdate() {
    console.log('Running Update');
    events = await createMeetUpdateBody();
    // console.log('CSV: ' + JSON.stringify(events));
    data = await GETMeetCSV('Quad', events);
    updateMeetTable(data);
}

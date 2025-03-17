async function runUpdate() {
    console.log('Running Update');
    events = await createMeetUpdateBody();
    // console.log('CSV: ' + JSON.stringify(events));
    data = await GETMeetCSV('Quad', events);
    updateMeetTable(data);
    // console.log(window.location.pathname);
    // console.log(window.location.search);
    // console.log(window.location.origin);

}

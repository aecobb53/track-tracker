async function runUpdate() {
    console.log('Running Update');
    events = await createMeetUpdateBody();
    // console.log('CSV: ' + JSON.stringify(events));

    var meet_name = document.getElementById('page-identifier-meet-name');
    data = await GETMeetCSV(meet_name.innerText, events);
    updateMeetTable(data);
    // console.log(window.location.pathname);
    // console.log(window.location.search);
    // console.log(window.location.origin);

}

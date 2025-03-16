async function runUpdate() {
    console.log('Running Update');
    csv = await populateCSV();
    console.log('CSV: ' + JSON.stringify(csv));
    data = await GETMeetCSV('Quad', csv);
    updateMeetTable(data);
}

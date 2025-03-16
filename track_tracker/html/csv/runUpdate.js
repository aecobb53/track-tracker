async function runUpdate() {
    console.log('Running Update');
    csv = await populateCSV();
    console.log('CSV: ' + JSON.stringify(csv));
    data = await GETCSV('2023-10-01', 'test', csv);
    updateCSVTable(csv_data=data);
}

async function GETMeetCSV(name, csv) {
    console.log('GETing to /meetday');
    var body = {
        name: name,
        csv: csv
    };
    // var url = '/meetday?' + new URLSearchParams(body).toString();
    var url = '/meetday';
    console.log('url: ' + url);

    console.log('body: ' + JSON.stringify(body));

    const response = await fetch(url, {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
    });
    const data = await response.json();
    console.log('Response: ');
    console.log(data);

    const status = response.status;
    console.log('Call status: ' + status);
    console.log('Call data: ');
    console.log(data);
    return data;
}

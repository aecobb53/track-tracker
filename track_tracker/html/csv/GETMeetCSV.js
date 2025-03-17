async function GETMeetCSV(name, events, data_time_version=null) {
    console.log('GETing to /meetday');
    // Get updated time
    var udpate_datetime_div = document.getElementById('page-identifier-update-time');

    var body = {
        name: name,
        events: events,
        data_time_version: udpate_datetime_div.innerHTML
    };
    // var url = '/meetday?' + new URLSearchParams(body).toString();
    var url = '/meetday';
    console.log('url: ' + url);

    // console.log(window.location.pathname);
    // console.log(window.location.search);
    // console.log(window.location.origin);
    const originalUrl = window.location.origin;
    const secureUrl = originalUrl.replace("http://", "https://");
    window.location.replace(secureUrl)

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

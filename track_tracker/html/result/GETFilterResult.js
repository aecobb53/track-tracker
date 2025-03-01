async function GETFilterResult(params) {
    console.log('GETing to /result/display');
    // var url = '/result/display';
    var url = '/result/display?' + new URLSearchParams(params).toString();
    console.log('url: ' + url);

    console.log('params: ' + JSON.stringify(params));

    const response = await fetch(url, {
        method: 'get',
        headers: {
            'Content-Type': 'application/json',
        },
        // params: JSON.stringify(params),
    });
    const data = await response.json();

    const status = response.status;
    console.log('Call status: ' + status);
    return data;
}
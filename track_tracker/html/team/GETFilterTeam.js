async function GETFilterTeam(params) {
    console.log('GETing to /team/display');
    // var url = '/result/display';


    // Fix this to a configurable thing later
    params['min_athlete_count'] = 5;



    var url = '/team/display?' + new URLSearchParams(params).toString();
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
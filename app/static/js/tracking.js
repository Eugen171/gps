var map = L.map('map', {minZoom: 1, maxZoom: 18});

var realtime = L.realtime(function(success, error) {
    fetch('/api/tracking')
    .then(function(response) { return response.json(); })
    .then(function(data) {
        console.log(data);
	success(data);
    })
    .catch(error);
}, {
    interval: 1000 * 60
}).addTo(map);

var i = 0;
realtime.on('update', function() {
    if (i == 0)
    {
	map.fitBounds([[0, 0], [0, 0]], {maxZoom: 0});
	++i;
    }
});
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(map);

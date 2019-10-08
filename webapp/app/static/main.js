var data = {};
var focus = ''
var charts = document.getElementById('charts');
var stats = document.getElementById('stats');


function loadMap(lat, lon, zoom, stations) {
    let mbUrl = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw'
    let mbAttr = 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
            '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
            'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>';

    let grayscale   = L.tileLayer(mbUrl, {id: 'mapbox.light', attribution: mbAttr});
    let streets  = L.tileLayer(mbUrl, {id: 'mapbox.streets',   attribution: mbAttr});
    //Stations layer
    stationsMarkers = []
    stations.forEach(station => {
        stationsMarkers.push(L.marker([station.latitud, station.longitud]).bindPopup(
                `<h1>${station.nameStation}</h1>`
            ).on('click', onMapClick)
        );
    });
    let stationsLayer = L.layerGroup(stationsMarkers)
    //load map
    var map = L.map('map', {
        center: [lat, lon],
        zoom: zoom,
        layers: [streets, stationsLayer]
    });
    //control layers
    var baseLayers = {
		"Grayscale": grayscale,
		"Streets": streets
	};
	var overlays = {
		"Stations": stationsLayer
	};
    L.control.layers(baseLayers, overlays).addTo(map);
    function onMapClick(e) {
        coords = this.getLatLng();
        stations.forEach(station => {
            if (station.longitud == coords.lng && station.latitud == coords.lat) {
                loadStationData(station.idStation);
                focus = station.idStation;
            }
        });
    }    
    map.on('click', onMapClick);
}





function getData(callback) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", 'http://localhost:5000/data', true); 
    xmlHttp.send(null);
}





window.onload = function(e) {
    var updatetime = 5;
    //load stations
    getData(function(response) {
        data = JSON.parse(response);
        //load mapa
        loadMap(19.423167, -99.130711, 11, data.stations);
        loadStationData('MER');
        focus='MER';
    });
    //setInterval(function() {
    //    getData(function(response) {
    //        data = JSON.parse(response);
    //        loadStationData(focus);
    //    });
    //}, 5000);
}




function loadStationData(idStation) {

    stations = data.stations
    parameters = data.parameters
    records = data.measurements
    stationInfo = getStationInfo(stations, idStation);

    //Datos Header
    let header = document.getElementById('header');
    let headerDate = document.getElementById('headerDate');
    let headerStationName = document.getElementById('headerStationName');
    dateTxt = document.createTextNode(data.datetime);
    stationTxt = document.createTextNode(stationInfo.name + ' (' + idStation + ')');
    headerDate.textContent = "";
    headerStationName.textContent = "";
    headerDate.appendChild(dateTxt);
    headerStationName.appendChild(stationTxt);


    stationData = {
        idStation: idStation,
        data: {}
    }

    //obtiene registros por parametro
    records.forEach(record => {
        if(record.idStation == idStation) {
            record.mediciones.forEach(medicion => {
                if (!(medicion.idParametro in stationData.data))
                    stationData.data[medicion.idParametro] = {}
                paramData = getMetaParam(parameters, medicion.idParametro)
                stationData.data[medicion.idParametro][record.dateTime] = {
                    valor: medicion.valor,
                    unidad: paramData.unidad,
                    nombre: paramData.nombre
                }
            });
        }
    });
    console.log(stationData)
    
    params = Object.keys(stationData.data)

    //sin datos
    if (params.length == 0) {
        console.log('SIN DATOS')
        let message = document.createElement('div');
        message.id = 'sinDatos';
        message.textContent = 'Sin datos';
        charts.appendChild(message)
    } else {
        let buttons = document.getElementById('buttons')
        //remove buttons
        while (buttons.firstChild) {
            buttons.removeChild(buttons.firstChild);
        }
            params.forEach(param => {
                let link = document.createElement('a');
                link.id = param;
                //PM2.5 defaul
                if (param == 'PM2.5')
                    link.classList.add('active')
                //add event
                let text = document.createTextNode(param);
                link.appendChild(text);
                link.addEventListener('click', focusParam);
                buttons.appendChild(link);
            });
    }


    //remove charts
    while (charts.firstChild) {
        charts.removeChild(charts.firstChild);
    }

    //remove stats
    while (stats.firstChild) {
        stats.removeChild(stats.firstChild);
    }
    

    params.forEach(param => {

        //get data formatted
        dataf = []
        dates = Object.keys(stationData.data[param])
        datesf = []
        unidad = stationData.data[param][dates[0]]['unidad'];
        dates.forEach(date => {
            d = new Date(date);
            strdatet = d.toDateString().split(' ')[1] + ' ' + d.toDateString().split(' ')[2] + ' ' + d.toTimeString().split(':')[0] + 'hr';
            datesf.push(strdatet);
        });
        dates.forEach(date => {
            dataf.push(stationData.data[param][date]['valor'])
        });

        //draw stats
        let stat = document.createElement('div');
        stat.id = param
        stat.classList.add('stat')
        stat.classList.add('hidde')
        //PM2.5 defaul
        if (param == 'PM2.5')
            stat.classList.toggle('hidde')
        let curr = document.createElement('span');
        let max = document.createElement('span');
        let min = document.createElement('span');
        let avg = document.createElement('span');
        let numData = dataf.map(Number);
        console.log(numData)
        let textCurr = document.createTextNode('Actual: '+dataf[numData.length-1].toString() + ' ' + unidad);
        let textMax = document.createTextNode('Max: '+Math.max.apply(Math, numData).toString() + ' ' + unidad);
        let textMin = document.createTextNode('Min: '+Math.min.apply(Math, numData).toString() + ' ' + unidad);
        let total = 0
        for (let i = 0; i < numData.length; i += 1) {
            total += numData[i];
        }
        let avgN = total / numData.length;
        let textAvg = document.createTextNode('Promedio: ' + avgN.toFixed(2) + ' ' + unidad);
        curr.appendChild(textCurr);
        max.appendChild(textMax);
        min.appendChild(textMin);
        avg.appendChild(textAvg);
        stat.appendChild(curr);
        stat.appendChild(max);
        stat.appendChild(min);
        stat.appendChild(avg);
        stats.appendChild(stat);

               

        // draw chart
        let canvas = document.createElement('canvas')
        canvas.id = param
        canvas.classList.add('chartStyle')
        canvas.classList.add('hidde')
        //PM2.5 defaul
        if (param == 'PM2.5')
            canvas.classList.toggle('hidde') 
        charts.appendChild(canvas)
        color = getRandomColor()
        var paramChart = new Chart(canvas, {
            type: 'line',
            data: {
                labels: datesf,
                datasets: [{
                    borderColor: color,
                    backgroundColor: color+'AA',
                    label: param,
                    data: dataf
                }]
            },
            options: {
                responsive: true,
                scales: {
                    xAxes: [{
                        ticks: {
                            autoSkipPadding: 10, 
                            padding: 20, 
                            maxRotation: 0, 
                            labelOffset: 15
                        }
                    }]
                }
            }
        });
    });
}


function focusParam(e) {
    this.classList.toggle('active')
    myid = this.id.replace('.', '\\.')
    id = `#${myid}`;
    charts.querySelector(id).classList.toggle('hidde')
}



function getMetaParam(parametros, idparam) {
    res = {}
    parametros.forEach(param => {
        if (idparam == param.idParameter){
            res = {
                unidad: param.unit,
                nombre: param.nameParameter
            };
        }
    });
    return res;
}

function getStationInfo(stations, idStation) {
    res = {}
    stations.forEach(station => {
        if (idStation == station.idStation){
            res = {
                name: station.nameStation,
                lat: station.latitud,
                lng: station.longitud,
                operation: station.operacion,
                elevation: station.elevacion
            };
        }
    });
    return res;
}

function getRandomColor() {
    let letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}


// var ctx = document.getElementById('myChart').getContext('2d');
// var myChart = new Chart(ctx, {
//     type: 'bar',
//     data: {
//         labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
//         datasets: [{
//             label: '# of Votes',
//             data: [12, 19, 3, 5, 2, 3],
//             backgroundColor: [
//                 'rgba(255, 99, 132, 0.2)',
//                 'rgba(54, 162, 235, 0.2)',
//                 'rgba(255, 206, 86, 0.2)',
//                 'rgba(75, 192, 192, 0.2)',
//                 'rgba(153, 102, 255, 0.2)',
//                 'rgba(255, 159, 64, 0.2)'
//             ],
//             borderColor: [
//                 'rgba(255, 99, 132, 1)',
//                 'rgba(54, 162, 235, 1)',
//                 'rgba(255, 206, 86, 1)',
//                 'rgba(75, 192, 192, 1)',
//                 'rgba(153, 102, 255, 1)',
//                 'rgba(255, 159, 64, 1)'
//             ],
//             borderWidth: 1
//         }]
//     },
//     options: {
//         scales: {
//             yAxes: [{
//                 ticks: {
//                     beginAtZero: true
//                 }
//             }]
//         }
//     }
// });
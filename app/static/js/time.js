var hms = time.split(":");
var sat = new Date();
sat.setHours(Number(hms[0]));
sat.setMinutes(Number(hms[1]));
sat.setSeconds(Number(hms[2]));
var diff = Date.now() - sat;

out = document.getElementById("time");


function format(num){
    if (num < 10)
        return ('0' + num);
    return ('' + num);
}
setInterval(() => {
    t = new Date(Date.now() - diff);
    out.innerHTML  = format(t.getHours());
    out.innerHTML += ":";
    out.innerHTML += format(t.getMinutes());
    out.innerHTML += ":";
    out.innerHTML += format(t.getSeconds());
}, 500)



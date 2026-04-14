async function scanTarget() {
    const target = document.getElementById('target').value;

    const response = await fetch('/scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target })
    });

    const data = await response.json();

    document.getElementById('ip').textContent = data.ip;

    // Ports
    const ports = document.getElementById('ports');
    ports.innerHTML = "";
    data.ports.forEach(p => {
        let li = document.createElement("li");
        li.textContent = "Port " + p + " OPEN";
        ports.appendChild(li);
    });

    // Headers
    document.getElementById('headers').textContent =
        JSON.stringify(data.headers, null, 2);
}
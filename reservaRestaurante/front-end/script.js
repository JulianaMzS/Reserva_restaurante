async function carregarReservas() {
    const resp = await fetch("http://127.0.0.1:5000/reservas");
    const reservas = await resp.json();
    const lista = document.getElementById("listaReservas");
    lista.innerHTML = "";
    reservas.forEach(r => {
        const li = document.createElement("li");
        li.textContent =` ${r.nome_cliente} - ${r.data} às ${r.hora} (${r.numero_pessoas} pessoas);`
        lista.appendChild(li);
    });
}

document.getElementById("formReserva").addEventListener("submit", async e => {
    e.preventDefault();
    const reserva = {
        nome_cliente: document.getElementById("nome_cliente").value,
        telefone_cliente: document.getElementById("telefone_cliente").value,
        data: document.getElementById("data").value,
        hora: document.getElementById("hora").value + ":00",
        numero_pessoas: parseInt(document.getElementById("numero_pessoas").value)
    };
    const resp = await fetch("http://127.0.0.1:5000/reservas", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(reserva)
    });
    const dataResp = await resp.json();
    document.getElementById("mensagem").textContent = dataResp.mensagem;
    carregarReservas();
    e.target.reset();
});

carregarReservas();
let usuarioLogado = "";
let privilegioUsuario = "";

async function login() {

    let usuario = document.getElementById("usuario").value;
    let senha = document.getElementById("senha").value;

    const resposta = await fetch("http://127.0.0.1:5000/login", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            usuario,
            senha
        })

    });

    const dados = await resposta.json();

    alert(dados.mensagem);

    if(dados.status === "sucesso") {

        usuarioLogado = dados.usuario;
        privilegioUsuario = dados.privilegio;

        document.getElementById("loginContainer")
        .classList.add("hidden");

        document.getElementById("reservaContainer")
        .classList.remove("hidden");

        listarReservas();
    }
}

async function listarReservas() {

    const resposta = await fetch("http://127.0.0.1:5000/reservas");

    const reservas = await resposta.json();

    let tabela = document.getElementById("listaReservas");

    tabela.innerHTML = "";

    reservas.forEach(reserva => {

        let botaoCancelar = "";

        if(privilegioUsuario === "admin") {

            botaoCancelar =
            `<button onclick="cancelarReserva(${reserva.id})">
                Cancelar
            </button>`;
        }

        tabela.innerHTML += `
            <tr>
                <td>${reserva.id}</td>
                <td>${reserva.sala}</td>
                <td>${reserva.data_reserva}</td>
                <td>${reserva.horario}</td>
                <td>${reserva.usuario}</td>
                <td>${botaoCancelar}</td>
            </tr>
        `;
    });
}

async function reservar() {

    let sala = document.getElementById("sala").value;
    let data = document.getElementById("data").value;
    let horario = document.getElementById("horario").value;

    const resposta = await fetch("http://127.0.0.1:5000/reservar", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            sala,
            data,
            horario,
            usuario: usuarioLogado
        })

    });

    const dados = await resposta.json();

    alert(dados.mensagem);

    listarReservas();
}

async function cancelarReserva(id) {

    const resposta = await fetch(
        `http://127.0.0.1:5000/cancelar/${id}`,
        {
            method: "DELETE"
        }
    );

    const dados = await resposta.json();

    alert(dados.mensagem);

    listarReservas();
}

// Aguarda o HTML ser completamente carregado
window.addEventListener('DOMContentLoaded', (event) => {
    
    // O seu código da máscara de CPF fica aqui dentro
    const inputCpf = document.getElementById('cpf');
    
    if (inputCpf) {
        inputCpf.addEventListener('input', (e) => {
            let value = e.target.value.replace(/\D/g, "");
            value = value.replace(/(\d{3})(\d)/, "$1.$2");
            value = value.replace(/(\d{3})(\d)/, "$1.$2");
            value = value.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
            e.target.value = value;
        });

        // IMPORTANTE: Isso faz com que o CPF já apareça formatado 
        // ao abrir a página de edição, sem precisar digitar nada!
        inputCpf.dispatchEvent(new Event('input'));
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var formulario = document.getElementById('meu_formulario');
    var inputBusca = document.getElementById('curso_busca');
    var list = document.getElementById('lista_cursos');
    var hiddenInput = document.getElementById('id_curso_enviar');

    // 1. Lógica para capturar o ID enquanto digita
    inputBusca.addEventListener('input', function() {
        var valorDigitado = inputBusca.value;
        hiddenInput.value = ""; // Reseta o ID provisoriamente

        for (var i = 0; i < list.options.length; i++) {
            var option = list.options[i];
            if (option.value === valorDigitado) {
                hiddenInput.value = option.getAttribute('data-id');
                break;
            }
        }
    });

    // 2. Lógica para BLOQUEAR o envio se o ID for inválido
    formulario.addEventListener('submit', function(event) {
        // Se o input oculto estiver vazio ou não numérico, cancela o envio imediatamente
        if (!hiddenInput.value || hiddenInput.value.trim() === "") {
            event.preventDefault(); // Para o envio para o servidor aqui!
            alert("Erro: Você precisa escolher um curso válido da lista suspensa.");
            inputBusca.focus();
        }
    });
});
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

document.addEventListener("DOMContentLoaded", () => {
  // 1. Pega o caminho da barra de endereços (ex: /alunos/editar-aluno/12)
  const caminhoAtual = window.location.pathname;

  // 2. Procura os links do menu do Bootstrap
  const linksMenu = document.querySelectorAll(".navbar-nav .nav-link");

  linksMenu.forEach(link => {
    const hrefLink = link.getAttribute("href");

    // REGRA ESPECIAL PARA A PÁGINA INICIAL (Home)
    if (hrefLink === "/") {
      if (caminhoAtual === "/") {
        link.classList.add("active");
      } else {
        link.classList.remove("active");
      }
    } 
    // REGRA PARA AS OUTRAS PÁGINAS (/alunos, /professores, etc.)
    else {
      // Se a URL atual começar com o texto do link, ele fica ativo!
      // Exemplo: "/alunos/editar" começa com "/alunos"? Sim! Então acende.
      if (caminhoAtual.startsWith(hrefLink)) {
        link.classList.add("active");
      } else {
        link.classList.remove("active");
      }
    }
  });
});
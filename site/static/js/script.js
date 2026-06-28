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
var menuItem = document.querySelectorAll('.item-menu')
function selectLink(event) {
    //event.preventDefault() // vamo impedir reload da pagina
    menuItem.forEach((item) =>
        item.classList.remove('ativo')
    )
    // garante que o LI receba a classe, mesmo clicando no img/span
    this.closest('.item-menu').classList.add('ativo')
}
menuItem.forEach((item) =>
    item.addEventListener('click', selectLink)
)

//expandir o menu
// 1. Expansão do Menu (Pode manter igual)
var btnExp = document.querySelector('#btn-exp')
var menuSide = document.querySelector('.menu-lateral')

btnExp.addEventListener('click', function(){
    menuSide.classList.toggle('expandir')
})

// 2. Lógica para deixar o item "Ativo" baseado na URL atual
// Isso roda toda vez que a página carrega/recarrega
document.addEventListener("DOMContentLoaded", function() {
    var currentLocation = window.location.pathname; // Pega ex: "/linha-do-tempo"
    var menuItem = document.querySelectorAll('.item-menu a'); // Seleciona o LINK dentro do item

    menuItem.forEach((link) => {
        // Se o href do link for igual a página atual
        if(link.getAttribute('href') === currentLocation){
            // Adiciona a classe 'ativo' no pai (li)
            link.parentElement.classList.add('ativo');
        }
    });
});
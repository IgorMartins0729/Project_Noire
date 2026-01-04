var menuItem = document.querySelectorAll('.item-menu')

function selectLink(event){
    //event.preventDefault() // vamo impedir reload da pagina
    
    menuItem.forEach((item)=>
        item.classList.remove('ativo')
    )
    // garante que o LI receba a classe, mesmo clicando no img/span
    this.closest('.item-menu').classList.add('ativo')
}

menuItem.forEach((item)=>
    item.addEventListener('click',selectLink)
)

//expandir o menu
var btnExp = document.querySelector('#btn-exp')
var menuSide = document.querySelector('.menu-lateral')

btnExp.addEventListener('click', function(){
    menuSide.classList.toggle('expandir')
}) 
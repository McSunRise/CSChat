const containerElement = document.querySelector(".container")

const openButton = document.querySelector('.etc-btn')

openButton.addEventListener('click', () => {
    openButton.classList.add('hidden')
    containerElement.classList.add('opened')
})
document.querySelector('.close-btn').addEventListener('click', ()=>{
    openButton.classList.remove('hidden')
    containerElement.classList.remove('opened')
})
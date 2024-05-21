
const containerElement = document.querySelector(".container")

const openButton = document.querySelector('.etc-btn')

const helpButton = document.querySelector('.secondary-button')

const backButton = document.querySelector('.back-btn')

openButton.addEventListener('click', () => {
    openButton.classList.add('hidden')
    containerElement.classList.add('opened')
})
document.querySelector('.close-btn').addEventListener('click', ()=>{
    openButton.classList.remove('hidden')
    containerElement.classList.remove('opened')
})

helpButton.addEventListener('click', () => {
    document.querySelector('#buttons').classList.add('hidden')
    document.querySelector('#feedback-form').classList.remove('hidden')
})

backButton.addEventListener('click', () => {
    document.querySelector('#buttons').classList.remove('hidden')
    document.querySelector('#feedback-form').classList.add('hidden')
})



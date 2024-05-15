const actionsContainer = document.querySelector('.actions')
const openButton = document.querySelector('.open-btn')

openButton.addEventListener('click',() => {
    const opened = actionsContainer.classList.contains('hidden')
    
    if (opened){
        openButton.classList.add('opened')
        actionsContainer.classList.remove('hidden')
    }
    else{
        actionsContainer.classList.add('hidden')
        openButton.classList.remove('opened')
    }
})
const messages = document.querySelectorAll('.messages-letters');
messages[messages.length - 1].scrollIntoView()


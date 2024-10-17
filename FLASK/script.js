// Função para carregar o JSON e criar os cards automaticamente
function loadCards() {
    fetch('teste.json')
    .then(response => response.json())
    .then(events => {
        const container = document.getElementById('cards-container');
        
        events.forEach(event => {
            // Criando os elementos para o card
            const card = document.createElement('div');
            card.classList.add('card');

            const img = document.createElement('img');
            img.src = event.imageUrl;
            img.alt = event.title;

            const cardContent = document.createElement('div');
            cardContent.classList.add('card-content');

            const title = document.createElement('h2');
            title.textContent = event.title;

            const date = document.createElement('p');
            date.classList.add('date');
            date.textContent = `Data: ${event.date}`;

            const location = document.createElement('p');
            location.classList.add('location');
            location.textContent = `Local: ${event.location}`;

            const description = document.createElement('p');
            description.textContent = event.description;

            // Montando a estrutura do card
            cardContent.appendChild(title);
            cardContent.appendChild(date);
            cardContent.appendChild(location);
            cardContent.appendChild(description);

            card.appendChild(img);
            card.appendChild(cardContent);

            // Adicionando o card ao container
            container.appendChild(card);
        });
    })
    .catch(error => {
        console.error('Erro ao carregar o arquivo JSON:', error);
    });
}

// Carregar os cards quando a página for carregada
window.onload = loadCards;

window.onload = function() {
    function loadEvents() {
        fetch('http://127.0.0.1:5000/events')
            .then(response => response.json())
            .then(data => {
                const eventList = document.getElementById('event-list');
                data.forEach((event, index) => {
                    const eventCard = document.createElement('div');
                    eventCard.className = 'event-card';

                    // Limita a descrição a 100 caracteres inicialmente
                    let shortDescription = event.descricao.slice(0, 100);
                    let isDescriptionExpanded = false;
                    let arePricesVisible = false;
                    let isEditing = false;  // Variável para controlar o estado de edição

                    // Montar a lista de tickets e preços
                    let ticketsHTML = '';
                    if (event.tickets && event.tickets.length > 0) {
                        event.tickets.forEach(ticket => {
                            ticketsHTML += `<li>${ticket.name}: R$${ticket.price} (Taxa: R$${ticket.tax})</li>`;
                        });
                    } else {
                        ticketsHTML = '<li>Ingressos não disponíveis</li>';
                    }

                    // Inicialmente, os preços estarão ocultos
                    let hiddenPricesHTML = `<ul id="tickets-${index}" class="tickets-list" style="display:none;">${ticketsHTML}</ul>`;

                    // Montar o card com as informações do evento
                    eventCard.innerHTML = `
                        <img src="${event.url_imagem}" alt="${event.nome}">
                        <input type="text" id="name-${index}" value="${event.nome}" disabled class="event-input">
                        <p><strong>Data:</strong> <input type="text" id="date-${index}" value="${event.data_inicio} - ${event.data_fim}" disabled class="event-input"></p>
                        <p><strong>Local:</strong> <input type="text" id="local-${index}" value="${event.local}" disabled class="event-input"></p>
                        <p class="description" id="desc-${index}">${shortDescription}${event.descricao.length > 100 ? '...' : ''}</p>
                        ${event.descricao.length > 100 ? `<button class="toggle-description" id="toggle-desc-${index}">Ver mais</button>` : ''}
                        <div class="button-container">
                            <button class="toggle-prices" id="toggle-prices-${index}">Ver ingressos</button>
                            <button class="edit-btn" id="edit-${index}">Editar</button>
                        </div>
                        ${hiddenPricesHTML}
                        <label>
                            <input type="checkbox" id="event-${index}" name="event-selection" value="${event.nome}">
                            Selecionar este evento
                        </label>
                    `;
                    eventList.appendChild(eventCard);

                    // Função para alternar entre edição e visualização
                    const editButton = document.getElementById(`edit-${index}`);
                    editButton.addEventListener('click', function() {
                        const nameField = document.getElementById(`name-${index}`);
                        const dateField = document.getElementById(`date-${index}`);
                        const localField = document.getElementById(`local-${index}`);
                        
                        if (!isEditing) {
                            // Habilitar os inputs para edição
                            nameField.disabled = false;
                            dateField.disabled = false;
                            localField.disabled = false;
                            editButton.innerText = 'Salvar';
                        } else {
                            // Desabilitar os inputs e salvar as alterações
                            nameField.disabled = true;
                            dateField.disabled = true;
                            localField.disabled = true;
                            editButton.innerText = 'Editar';

                            // Salvar valores (aqui você pode enviar para o backend se necessário)
                            event.nome = nameField.value;
                            event.data_inicio = dateField.value.split(' - ')[0];
                            event.data_fim = dateField.value.split(' - ')[1];
                            event.local = localField.value;
                        }

                        isEditing = !isEditing;  // Alternar o estado de edição
                    });

                    // Adicionar funcionalidade de 'Ver mais' e 'Ver menos' para a descrição
                    if (event.descricao.length > 100) {
                        const toggleDescButton = document.getElementById(`toggle-desc-${index}`);
                        const descriptionElement = document.getElementById(`desc-${index}`);

                        toggleDescButton.addEventListener('click', function() {
                            if (isDescriptionExpanded) {
                                descriptionElement.classList.remove('description-expanded');
                                descriptionElement.classList.add('description');
                                toggleDescButton.innerHTML = 'Ver mais';
                            } else {
                                descriptionElement.classList.remove('description');
                                descriptionElement.classList.add('description-expanded');
                                toggleDescButton.innerHTML = 'Ver menos';
                            }
                            isDescriptionExpanded = !isDescriptionExpanded;
                        });
                    }

                    // Função para alternar entre "Ver preços" e "Ocultar preços"
                    const togglePricesButton = document.getElementById(`toggle-prices-${index}`);
                    const ticketsElement = document.getElementById(`tickets-${index}`);

                    togglePricesButton.addEventListener('click', function() {
                        if (arePricesVisible) {
                            ticketsElement.style.display = 'none';
                            togglePricesButton.innerHTML = 'Ver Ingressos';  // Muda a seta para baixo
                        } else {
                            ticketsElement.style.display = 'block';
                            togglePricesButton.innerHTML = 'Ocultar';  // Muda a seta para cima
                        }
                        arePricesVisible = !arePricesVisible;
                    });
                });
            })
            .catch(error => console.error('Erro ao carregar eventos:', error));
    }

    document.getElementById('submit-selection').addEventListener('click', function() {
        const selectedEvents = [];
        const checkboxes = document.querySelectorAll('input[name="event-selection"]:checked');
        checkboxes.forEach(checkbox => {
            selectedEvents.push(checkbox.value);
        });

        alert('Eventos Selecionados: ' + selectedEvents.join(', '));
    });

    loadEvents();
};

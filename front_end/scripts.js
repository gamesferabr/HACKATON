window.onload = function() {
    let currentPage = 1;
    const pageSize = 10;

    function loadEvents(page = 1) {
        fetch(`http://127.0.0.1:8000/api/scrap/eventos/elasticsearch?page=${page}&size=${pageSize}`)
            .then(response => response.json())
            .then(data => {
                const eventList = document.getElementById('event-list');

                // Limpar a lista de eventos antes de carregar novos
                eventList.innerHTML = '';

                // Adicionar eventos à lista
                data.eventos.forEach((event, index) => {
                    const eventCard = document.createElement('div');
                    eventCard.className = 'event-card';

                    let shortDescription = event.descricao.slice(0, 100);

                    let hiddenPricesHTML = `<ul id="tickets-${index}" class="tickets-list" style="display:none;">${event.valor}</ul>`;

                    eventCard.innerHTML = `
                        <img src="${event.url_imagem}" alt="${event.nome}">
                        <input type="text" id="name-${index}" value="${event.nome}" disabled class="event-input">
                        <p><strong>Data:</strong> <input type="text" id="date-${index}" value="${event.data_inicio} - ${event.data_fim}" disabled class="event-input"></p>
                        <p><strong>Local:</strong> <input type="text" id="local-${index}" value="${event.local}" disabled class="event-input"></p>
                        <p class="description" id="desc-${index}">${shortDescription}${event.descricao.length > 100 ? '...' : ''}</p>
                        ${event.descricao.length > 100 ? `<button class="toggle-description" id="toggle-desc-${index}">Ver mais</button>` : ''}
                        <div class="button-container">
                            <button class="toggle-prices" id="toggle-prices-${index}">Ver preço</button>
                            <button class="edit-btn" id="edit-${index}">Editar</button>
                        </div>
                        ${hiddenPricesHTML}
                        <label>
                            <input type="checkbox" id="event-${index}" name="event-selection" value="${event.nome}">
                            Selecionar este evento
                        </label>
                    `;
                    eventList.appendChild(eventCard);

                    // Funções para editar, expandir descrição e ver preços
                    setupEventActions(index, event);
                });

                // Atualizar a paginação
                updatePagination(data.total_documentos, page);
            })
            .catch(error => console.error('Erro ao carregar eventos:', error));
    }

    function setupEventActions(index, event) {
        const editButton = document.getElementById(`edit-${index}`);
        const nameField = document.getElementById(`name-${index}`);
        const dateField = document.getElementById(`date-${index}`);
        const localField = document.getElementById(`local-${index}`);
        const toggleDescButton = document.getElementById(`toggle-desc-${index}`);
        const descriptionElement = document.getElementById(`desc-${index}`);
        const togglePricesButton = document.getElementById(`toggle-prices-${index}`);
        const ticketsElement = document.getElementById(`tickets-${index}`);

        let isDescriptionExpanded = false;
        let arePricesVisible = false;
        let isEditing = false;

        // Função para alternar entre edição e visualização
        editButton.addEventListener('click', function() {
            if (!isEditing) {
                nameField.disabled = false;
                dateField.disabled = false;
                localField.disabled = false;
                editButton.innerText = 'Salvar';
            } else {
                nameField.disabled = true;
                dateField.disabled = true;
                localField.disabled = true;
                editButton.innerText = 'Editar';

                // Salvar valores (pode enviar para o backend se necessário)
                event.nome = nameField.value;
                event.data_inicio = dateField.value.split(' - ')[0];
                event.data_fim = dateField.value.split(' - ')[1];
                event.local = localField.value;
            }
            isEditing = !isEditing;
        });

        // Função para alternar entre 'Ver mais' e 'Ver menos' para a descrição
        if (toggleDescButton) {
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
        togglePricesButton.addEventListener('click', function() {
            if (arePricesVisible) {
                ticketsElement.style.display = 'none';
                togglePricesButton.innerHTML = 'Ver Ingressos';
            } else {
                ticketsElement.style.display = 'block';
                togglePricesButton.innerHTML = 'Ocultar';
            }
            arePricesVisible = !arePricesVisible;
        });
    }

    function updatePagination(totalDocuments, currentPage) {
        const totalPages = Math.ceil(totalDocuments / pageSize);
        const paginationContainer = document.getElementById('pagination');
        paginationContainer.innerHTML = ''; // Limpa a paginação anterior

        // Adiciona botões numerados para cada página
        for (let i = 1; i <= totalPages; i++) {
            const pageButton = document.createElement('button');
            pageButton.className = 'page-button';
            pageButton.innerText = i;
            if (i === currentPage) {
                pageButton.classList.add('active'); // Marca a página atual
            }

            pageButton.addEventListener('click', function() {
                loadEvents(i);
            });

            paginationContainer.appendChild(pageButton);
        }
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

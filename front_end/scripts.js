window.onload = function() {
    let allEvents = []; // Armazena todos os eventos
    let filteredEvents = []; // Armazena eventos filtrados
    const pageSize = 9;
    let currentPage = 1;

    // Mapeamento de cidades para exibição no front-end
    const cityDisplayNames = {
        "são+vicente": "São Vicente",
        "praia+grande": "Praia Grande",
        "guarujá": "Guarujá",
        "santos": "Santos",
        "mongaguá": "Mongaguá",
        "bertioga": "Bertioga"
    };

    // Função para carregar todos os eventos de várias páginas e preencher o filtro de cidades
    function loadAllEvents() {
        fetch('http://127.0.0.1:8000/api/save/eventos/elasticsearch?page=1&size=1')
            .then(response => response.json())
            .then(data => {
                const totalDocuments = data.total_documentos;
                const totalPages = Math.ceil(totalDocuments / pageSize);
                const citySet = new Set();

                const requests = [];
                for (let page = 1; page <= totalPages; page++) {
                    requests.push(
                        fetch(`http://127.0.0.1:8000/api/save/eventos/elasticsearch?page=${page}&size=${pageSize}`)
                            .then(response => response.json())
                            .then(data => {
                                data.eventos.forEach(event => {
                                    allEvents.push(event);
                                    if (event.area) {
                                        citySet.add(event.area);
                                    }
                                });
                            })
                    );
                }

                Promise.all(requests).then(() => {
                    filteredEvents = allEvents;
                    displayEvents(filteredEvents, 1);
                    updatePagination(filteredEvents.length, 1);
                    populateCityFilter(Array.from(citySet).sort());
                }).catch(error => console.error('Erro ao carregar os eventos:', error));
            });
    }

    function displayEvents(events, page) {
        const eventList = document.getElementById('event-list');
        eventList.innerHTML = '';

        const start = (page - 1) * pageSize;
        const end = start + pageSize;
        const paginatedEvents = events.slice(start, end);

        paginatedEvents.forEach((event, index) => {
            const eventCard = document.createElement('div');
            eventCard.className = 'event-card';
            const price = event.valor !== undefined ? event.valor : "Não informado";
            const cityDisplay = cityDisplayNames[event.area] || event.area;

            eventCard.innerHTML = `
                <img src="${event.url_imagem}" alt="${event.nome}">
                <input type="text" id="name-${index}" value="${event.nome}" disabled class="event-input">
                <p><strong>Data:</strong> <input type="text" id="date-${index}" value="${event.data_inicio} - ${event.data_fim}" disabled class="event-input"></p>
                <p><strong>Local:</strong> <input type="text" id="local-${index}" value="${event.local}" disabled class="event-input"></p>
                <p><strong>Cidade:</strong> ${cityDisplay}</p>
                <p class="description" id="desc-${index}" style="max-height: 100px; overflow-y: auto;">${event.descricao}</p>
                <p class="ticket-price"><strong>Preço:</strong> ${price}</p>
                <div class="button-container">
                    <button class="edit-btn" id="edit-${index}">Editar</button>
                    <button class="save-btn" id="save-${index}" style="display:none;">Salvar</button>
                </div>
                <label>
                    <input type="checkbox" id="event-${index}" name="event-selection" value="${event.nome}">
                    Selecionar este evento
                </label>
            `;
            eventList.appendChild(eventCard);
            setupEventActions(index, event);
        });
    }

    function populateCityFilter(cities) {
        const citySelect = document.getElementById('city-select');
        while (citySelect.options.length > 1) {
            citySelect.remove(1);
        }

        cities.forEach(city => {
            const option = document.createElement('option');
            option.value = city;
            option.text = cityDisplayNames[city] || city;
            citySelect.appendChild(option);
        });
    }

    function filterEventsByCity(city) {
        filteredEvents = city ? allEvents.filter(event => event.area === city) : allEvents;
        currentPage = 1;
        displayEvents(filteredEvents, currentPage);
        updatePagination(filteredEvents.length, currentPage);
    }

    function setupEventActions(index, event) {
        const editButton = document.getElementById(`edit-${index}`);
        const saveButton = document.getElementById(`save-${index}`);
        const nameField = document.getElementById(`name-${index}`);
        const dateField = document.getElementById(`date-${index}`);
        const localField = document.getElementById(`local-${index}`);
        
        let isEditing = false;

        editButton.addEventListener('click', function() {
            if (!isEditing) {
                nameField.disabled = false;
                dateField.disabled = false;
                localField.disabled = false;
                editButton.style.display = 'none';
                saveButton.style.display = 'inline-block';
            }
        });

        saveButton.addEventListener('click', function() {
            nameField.disabled = true;
            dateField.disabled = true;
            localField.disabled = true;
            editButton.style.display = 'inline-block';
            saveButton.style.display = 'none';

            event.nome = nameField.value;
            const dates = dateField.value.split(' - ');
            event.data_inicio = dates[0];
            event.data_fim = dates[1];
            event.local = localField.value;
        });
    }

    function updatePagination(totalDocuments, currentPage) {
        const totalPages = Math.ceil(totalDocuments / pageSize);
        const paginationContainer = document.getElementById('pagination');
        paginationContainer.innerHTML = '';

        for (let i = 1; i <= totalPages; i++) {
            const pageButton = document.createElement('button');
            pageButton.className = 'page-button';
            pageButton.innerText = i;
            if (i === currentPage) {
                pageButton.classList.add('active');
            }

            pageButton.addEventListener('click', function() {
                currentPage = i;
                displayEvents(filteredEvents, currentPage);
                updatePagination(filteredEvents.length, currentPage);
            });

            paginationContainer.appendChild(pageButton);
        }
    }

    document.getElementById('city-select').addEventListener('change', function() {
        const selectedCity = this.value;
        filterEventsByCity(selectedCity);
    });

    document.getElementById('submit-selection').addEventListener('click', function() {
        const selectedEvents = [];
        const checkboxes = document.querySelectorAll('input[name="event-selection"]:checked');
        checkboxes.forEach(checkbox => {
            selectedEvents.push(checkbox.value);
        });

        alert('Eventos Selecionados: ' + selectedEvents.join(', '));
    });

    loadAllEvents();
};

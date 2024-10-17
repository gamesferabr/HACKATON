import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

# Função para remover emojis
def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  
        u"\U0001F300-\U0001F5FF"  
        u"\U0001F680-\U0001F6FF" 
        u"\U0001F1E0-\U0001F1FF"  
        u"\U00002500-\U00002BEF" 
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55" 
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f" 
        u"\u3030"
        "]+", 
        flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

# Função para fazer scraping de uma página de evento
def scrape_articket_page(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extrair imagem
        image_container = soup.find('div', class_='flex items-center justify-center w-full h-100 lg:w-1/2')
        image_src = None
        if image_container:
            image = image_container.find('img')
            if image:
                image_src = image.get('src')

        # Extrair título, data e local
        event_info_container = soup.find('div', class_='flex flex-col items-center w-full lg:w-1/2')
        title = None
        event_date = None
        location = None
        if event_info_container:
            title = event_info_container.find('h1').get_text(strip=True) if event_info_container.find('h1') else None
            event_date = event_info_container.find('span', class_='text-red-300').get_text(strip=True) if event_info_container.find('span', class_='text-red-300') else None
            location = event_info_container.find('span', class_='m-1').get_text(strip=True) if event_info_container.find('span', class_='m-1') else None

        # Extrair ingressos
        tickets = []
        tickets_section = soup.find('section', id='tickets', class_='container p-3 mx-auto mb-6 bg-white shadow-lg lg:rounded-lg')
        if tickets_section:
            ticket_elements = tickets_section.find_all('tr', class_='ticket')
            for ticket in ticket_elements:
                ticket_name = remove_emojis(ticket.find('span', class_='ticket-title').get_text(strip=True))
                ticket_price_element = ticket.find('span', {'property': 'price'})
                ticket_price = ticket_price_element.get_text(strip=True) if ticket_price_element else "Preço não disponível"
                tickets.append({'name': ticket_name, 'price': ticket_price})

        # Extrair detalhes do evento
        details_section = soup.find('section', class_='container p-3 mx-auto bg-white shadow-lg lg:rounded-lg mb-6')
        event_details = ""
        if details_section:
            event_paragraphs = details_section.find_all('p')
            if event_paragraphs:
                event_details = "\n".join([remove_emojis(p.get_text(strip=True)) for p in event_paragraphs])

        # Retorna os dados como um dicionário (objeto)
        event_data = {
            'image_url': image_src,
            'title': title,
            'event_date': event_date,
            'location': location,
            'tickets': tickets,
            'event_details': event_details
        }
        return event_data
    else:
        return None

# Função para buscar os links dos eventos
def get_event_links(search_url):
    response = requests.get(search_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Procurar todos os links dos eventos na página de busca dentro da classe <div class="mt-5 mb-5">
        event_links = []
        event_cards = soup.find_all('div', class_='mt-5 mb-5')  # Buscando pelas divs
        for event_card in event_cards:
            link = event_card.find('a', href=True)  # Pega o href do <a> dentro da div
            if link:
                full_link = link['href']
                event_links.append(full_link)
        
        return event_links
    else:
        return []

# Rota para buscar todos os eventos e retornar os dados em formato JSON
@app.route('/events', methods=['GET'])
def get_events():
    search_url = "https://articket.com.br/busca?q=santos"

    # Buscar todos os links de eventos
    event_links = get_event_links(search_url)

    # Lista para armazenar os dados de todos os eventos
    events_data = []

    # Fazer scraping de cada página de evento
    for event_url in event_links:
        event_data = scrape_articket_page(event_url)
        if event_data:
            events_data.append(event_data)

    # Retorna os dados em formato JSON
    return jsonify(events_data)

if __name__ == "__main__":
    app.run(debug=True)
python app.py
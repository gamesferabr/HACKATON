import re
import requests
from bs4 import BeautifulSoup
from app.services.utils.elastic import es
import hashlib
from app.services.evento_services import EventoService
from app.api.schemas.evento_schema import EventoSchema

class Scrap:
    @staticmethod
    def generate_unique_id(event):
        unique_string = f"{event['nome']}_{event['local']}_{event['data_inicio']}"
        unique_id = hashlib.md5(unique_string.encode('utf-8')).hexdigest()
        return unique_id
    
    @staticmethod
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

    @staticmethod
    def validation_ticket_section(tickets_section, tickets):
        if tickets_section:
            ticket_elements = tickets_section.find_all('tr', class_='ticket')
            for ticket in ticket_elements:
                ticket_name = Scrap.remove_emojis(ticket.find('span', class_='ticket-title').get_text(strip=True))
                ticket_price, tax = Scrap.extract_ticket_price_and_tax(ticket)
                tickets.append({'name': ticket_name, 'tax': tax, 'price': ticket_price})
        
        return tickets

    @staticmethod
    def extract_ticket_price_and_tax(ticket):
        ticket_price_element = ticket.find('div', class_='p-3')
        ticket_price = ticket_price_element.get_text(strip=True) if ticket_price_element else "Preço não disponível"
        tax = ticket_price.split('(')[-1]
        tax = tax.replace('Taxas', '').replace(')', '').replace('+', '')
        ticket_price = ticket_price.split('(')[0]
        
        if 'Grátis' in ticket_price:
            tax = "0"
            ticket_price = ticket_price.replace('Grátis', '').strip()
        
        if 'R$' in ticket_price:
            ticket_price = ticket_price.replace('R$', '').strip()
        
        if 'R$' in tax:
            tax = tax.replace('R$', '').strip()
        
        if ',' in ticket_price:
            ticket_price = ticket_price.replace(',', '').strip()
        
        ticket_price = float(ticket_price) if ticket_price else 0.0
        tax = float(tax) if tax else 0.0

        return ticket_price, tax
    
    @staticmethod
    def scrape_articket_page(url):
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            image_src = Scrap.extract_image_src(soup)
            title, event_date, location = Scrap.extract_event_info(soup)
            event_details = Scrap.extract_event_details(soup)
            tickets = Scrap.extract_tickets(soup)

            event_data = {
                'link_validacao': url,
                'url_imagem': image_src,
                'nome': title,
                'event_date': event_date,
                'local': location,
                'descricao': event_details,
                'tickets': tickets
                }
            
            return event_data
        
        else:
            return None

    @staticmethod
    def extract_image_src(soup):
        image_container = soup.find('div', 
                                    class_='flex items-center justify-center w-full h-100 lg:w-1/2')
        if image_container:
            image = image_container.find('img')
            if image:
                return image.get('src')
        
        return None

    @staticmethod
    def extract_event_info(soup):
        event_info_container = soup.find('div',
                                         class_='flex flex-col items-center w-full lg:w-1/2')
        title = None
        event_date = None
        location = None
        
        if event_info_container:
            title = event_info_container.find('h1').get_text(strip=True) if event_info_container.find('h1') else None
            event_date = event_info_container.find('span', class_='text-red-300').get_text(strip=True) if event_info_container.find('span', class_='text-red-300') else None
            location = event_info_container.find('span', class_='m-1').get_text(strip=True) if event_info_container.find('span', class_='m-1') else None
        
        return title, event_date, location

    @staticmethod
    def extract_tickets(soup):
        tickets = []
        tickets_section = soup.find('section', 
                                    id='tickets', 
                                    class_='container p-3 mx-auto mb-6 bg-white shadow-lg lg:rounded-lg')
        
        return Scrap.validation_ticket_section(tickets_section, tickets)

    @staticmethod
    def extract_event_details(soup):
        details_section = soup.find('section', 
                                    class_='container p-3 mx-auto bg-white shadow-lg lg:rounded-lg mb-6')
        event_details = ""
        if details_section:
            event_paragraphs = details_section.find_all('p')
            if event_paragraphs:
                event_details = "\n".join([Scrap.remove_emojis(p.get_text(strip=True)) for p in event_paragraphs])
        
        return event_details

    @staticmethod
    def get_event_links(search_url):
        response = requests.get(search_url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            event_links = []
            event_cards = soup.find_all('div', class_='mt-5 mb-5')
            for event_card in event_cards:
                link = event_card.find('a', href=True)
                if link:
                    full_link = link['href']
                    event_links.append(full_link)
            
            return event_links
       
        else:
            return []

    @staticmethod
    def get_all(cidade):
        
        search_url = f"https://articket.com.br/busca?q={cidade}"
        event_links = Scrap.get_event_links(search_url)
        events_data = []
        cont = Scrap.count_elastic_documents()
            
        if cont == 0:
                cont = 0
                
        for event_url in event_links:
                event_data = Scrap.scrape_articket_page(event_url)
                event_data['area'] = cidade
                
                if event_data:
                    event_data['data_inicio'] = event_data['event_date'].split('-\n')[0].strip()
                    event_data['data_fim'] = event_data['event_date'].split('-\n')[1].strip()
                    del event_data['event_date']
                    
                    events_data.append(event_data)
            
        for event in events_data:
                tickets = event['tickets']
                
                if tickets:
                    prices = [ticket['price'] for ticket in tickets]
                    max_price = max(prices)
                    min_price = min(prices)
                    
                    event['valor'] = f"R${min_price} - R${max_price}"
                    del event['tickets']
            
        
        print(f"Encontrados {len(events_data)} eventos")
        print(events_data)
        
        return events_data
    
    @staticmethod
    def salvar_evento():
        cidade = ["santos",
                    "são+vicente",
                    "praia+grande",
                    "guarujá",
                    "bertioga",
                    "mongaguá"]
        
        
        dados = []
        
        for i in range(len(cidade)):
            eventos = Scrap.get_all(cidade[i])
            if len(eventos) > 0:
                dados.extend(eventos)
        
        len_dados = len(dados)
        
        print(f"Executando salvar_evento! {len_dados} eventos encontrados")
        
        try:
            print("Contando documentos existentes...")
            contador = Scrap.count_elastic_documents()
                            
            if contador == 0:
                contador = 0

            for dado in dados:
                if isinstance(dado, dict):
                    unique_id = Scrap.generate_unique_id(dado)
                    
                    # Verificar se o documento já existe no índice
                    if es.exists(index='eventos', id=unique_id):
                        print(f"Documento com ID {unique_id} já existe. Pulando...")
                        continue
                    
                    contador += 1
                    dado['contador'] = contador
                    print(f"Indexando documento {contador}...")
                    dado['id'] = unique_id
                    
                    # Indexa o documento usando o ID gerado e o contador atualizado
                    es.index(index='eventos', id=unique_id, body=dado)
                    print(dado)
                    
                    Scrap.salvar_evento_mysql(dado)
                    
        except Exception as e:
            print(f"Erro ao indexar documentos: {e}")
            return f"Erro ao indexar documentos: {e}"
        
        return "Documentos indexados com sucesso"

    @staticmethod
    def salvar_evento_mysql(dado):
        try:
            print("Salvando evento no MySQL...")
            
            # Criar a instância do modelo Evento com os dados
            evento_model = EventoSchema(
                id=dado.get('id', ''),
                link_validacao=dado.get('link_validacao', ''),
                url_imagem=dado.get('url_imagem', ''),
                nome=dado.get('nome', ''),
                data_inicio=dado.get('data_inicio', ''),
                data_fim=dado.get('data_fim', ''),
                local=dado.get('local', ''),
                descricao=dado.get('descricao', ''),
                valor=dado.get('valor', 'R$0.0 - R$0.0')  # Valor padrão caso esteja ausente
            )
            
            print(evento_model)
            
            # Utilizar o serviço para salvar o evento no banco de dados
            service = EventoService()
            service.create(evento_model)

            print("Evento salvo com sucesso")
            
            return "Evento salvo com sucesso"
        
        except Exception as e:
            print(f"Erro ao salvar evento no MySQL: {e}")
            return f"Erro ao salvar evento no MySQL: {e}"

    @staticmethod
    def get_elastic_events(page=1, size=10):
        """
        Recupera eventos ordenados pelo campo 'contador' para garantir que os mais recentes sejam listados primeiro.
        """
        query = {
            "query": {
                "match_all": {}
            },
            "sort": [
                {"contador": {"order": "desc"}}
            ],
            "from": (page - 1) * size,
            "size": size
        }
        
        response = es.search(index="eventos", body=query)
        return response['hits']['hits']
    
    @staticmethod
    def count_elastic_documents():
        response = es.count(index="eventos")
        return response['count']

import re
import requests
from bs4 import BeautifulSoup

class Scrap:
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
        
        import app.services.save_evento_services as SaveEventoService
        cont = SaveEventoService.SaveEventoService.count_elastic_documents()
            
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

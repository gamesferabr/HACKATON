from bs4 import BeautifulSoup
import requests
import sys
import re
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

class ScrapBilhetariaExpress:
    @staticmethod
    def get_image_links(soup):
        image_divs = soup.find_all("div", class_="product-image")
        links = []
        
        for image_card in image_divs:
            link_element = image_card.find("a")
            if link_element:
                link = link_element.get("href")
                links.append(link)
        
        return links

    @staticmethod
    def extract_links(cidades):
        print("Extracting links from Bilheteria Express...")
        print(f"Total cities: {len(cidades)}")
        print(cidades)
        
        all_links = {}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

        for cidade in cidades:
            print(f"Extracting links for {cidade}...")
            cidade_links = set()  
            page = 1
            has_more_items = True
            
            while has_more_items:
                if page == 1:
                    response = requests.get(
                        f"https://www.bilheteriaexpress.com.br/agendas/{cidade}.html#page=1", 
                        headers=headers)
                else:
                    response = requests.get(
                f"https://www.bilheteriaexpress.com.br/agendas/{cidade}.html?is_ajax=1&p={page}&is_scroll=1", 
                headers=headers)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    new_links = ScrapBilhetariaExpress.get_image_links(soup)

                    if not new_links:
                        print(f"Page {page}: No more items found.")
                        has_more_items = False
                        break

                    initial_size = len(cidade_links)
                    cidade_links.update(new_links)
                    
                    if len(cidade_links) == initial_size:
                        print(f"Page {page}: No new links found. Stopping pagination.")
                        has_more_items = False
                        break
                    
                    print(f"Page {page}: Found {len(new_links)} new links.")
                else:
                    print(f"Failed to retrieve page {page} for {cidade}, status code: {response.status_code}")
                    break

                page += 1

            all_links[cidade] = list(cidade_links)

        return all_links

    @staticmethod
    def extract_event_details(urls, cidade):
        event_details = []
        
        for url in urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            
            date_element = soup.find("img", {"data-src": lambda src: src and "ico_horario" in src})
            if date_element:
                date = date_element.find_next("td").text.strip()
            else:
                date = "Data não encontrada"
            
            local_element = soup.find("img", {"data-src": lambda src: src and "ico_local" in src})
            if local_element:
                local = local_element.find_next("td").text.strip()
            else:
                local = "Local não encontrado"
            
            valor_element = soup.find("img", {"data-src": lambda src: src and "ico_valor" in src})
            if valor_element:
                valor = valor_element.find_next("td").text.strip()
            else:
                valor = "Valor não encontrado"
                        
            info_element = soup.find("div", class_="product-info row")
            descricao = ""
            if info_element:
                std_element = info_element.find("div", class_="std")
                if std_element:
                    p_element = std_element.find_next("p")
                    if p_element:
                        for br in p_element.find_all("br"):
                            br.replace_with(" ") 
                        descricao = p_element.get_text(strip=True)
            
            info_image = soup.find("p", class_="product-image")
            
            if info_image:
                image = info_image.find("img")
                if image:
                    url_imagem = image.get("data-src")
                
                else:
                    url_imagem = ""
            
            # Tratar os valores
            prices = re.findall(r'\d+,\d+', valor)

            if len(prices) == 2:
                min_price = prices[0].replace(',', '.')
                max_price = prices[1].replace(',', '.')
                valor_tratado = f"R$ {min_price} - R$ {max_price}"
                
            elif len(prices) == 1:
                min_price = prices[0].replace(',', '.')
                valor_tratado = f"R$ {min_price}"
            else:
                valor_tratado = "Valor não disponível"

            # Tratar a data
            match = re.search(r"(\d{2}/\d{2}).*?(\d{1,2}h\d{2})", date)
            
            if match:
                date_part = match.group(1)  # "16/11"
                time_part = match.group(2)  # "20h00"
                
                time_part = time_part.replace("h", ":")                
                year = datetime.now().year
                
                full_date_str = f"{date_part}/{year} {time_part}"
                
                date_obj = datetime.strptime(full_date_str, "%d/%m/%Y %H:%M")
                
                formatted_date = date_obj.strftime("%d/%m/%Y %H:%M")
                date = str(formatted_date)
            
            nome = soup.find("div" , class_="price-review").find("p").text.strip()
            
            cidade = cidade.replace("-", "+")
            if cidade == "sao+vicente+sp":
                cidade = "são+vicente"
            
            elif cidade == "praia+grande+sp":
                cidade = "praia+grande"
            
            elif cidade == "guaruja":
                cidade = "guarujá"
            
            elif cidade == "mongagua":
                cidade = "mongaguá"
                
            event_details.append({
                "url_imagem": url_imagem,
                "link_validacao": url,
                "data_inicio": date,
                "data_fim": date,
                "local": local,
                "nome": nome,
                "valor": valor_tratado,
                "descricao": descricao,
                "area": cidade})
        
        return event_details
    
    @staticmethod
    def get_all_bilheteria_express():
        cidades = ["santos", "sao-vicente-sp", "praia-grande-sp", "guaruja", "bertioga", "mongagua"]
        links = ScrapBilhetariaExpress.extract_links(cidades)
        eventos = []
        for cidade, urls in links.items():
            eventos.extend(ScrapBilhetariaExpress.extract_event_details(urls, cidade))
        
        return eventos

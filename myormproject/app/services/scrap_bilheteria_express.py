from bs4 import BeautifulSoup
import requests
import sys

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
                    response = requests.get(f"https://www.bilheteriaexpress.com.br/agendas/{cidade}.html#page=1", headers=headers)
                else:
                    response = requests.get(f"https://www.bilheteriaexpress.com.br/agendas/{cidade}.html?is_ajax=1&p={page}&is_scroll=1", headers=headers)
                
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
    def extract_event_details(urls):
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
            
            info_image = soup.find("div", class_="product-image")
            if info_image:
                image = info_image.find("img")
                if image:
                    url_imagem = image.get("src")
                else:
                    url_imagem = ""
            else:
                url_imagem = ""
                
            event_details.append({
                "url_imagem": url_imagem,
                "url": url,
                "data": date,
                "local": local,
                "valor": valor,
                "descricao": descricao,
            })
        
        return event_details
    
    @staticmethod
    def get_all_bilheteria_express():
        cidades = ["santos", "sao-vicente-sp", "praia-grande-sp", "guaruja", "bertioga", "mongagua"]
        links = ScrapBilhetariaExpress.extract_links(cidades)
        eventos = []
        for cidade, urls in links.items():
            eventos.extend(ScrapBilhetariaExpress.extract_event_details(urls))
        
        return eventos

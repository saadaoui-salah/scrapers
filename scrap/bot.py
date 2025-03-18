import requests
from bs4 import BeautifulSoup

class Cach:
    filters = []

cach = Cach()

def fetch_products(page=1):
    url = "https://www.sofiaspa.it/wp-admin/admin-ajax.php"
    headers = {
        "Accept": "*/*",
        "Accept-Language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "DNT": "1",
        "Origin": "https://www.sofiaspa.it",
        "Pragma": "no-cache",
        "Referer": f"https://www.sofiaspa.it/catalogo/?swoof=1&reload=true&paged={page}",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Linux",
    }
    
    data = {
        "action": "woof_draw_products",
        "link": f"https://www.sofiaspa.it/catalogo/?swoof=1&reload=true&paged={page}",
        "page": str(page),
        "shortcode": f"woof_products is_ajax=1 page={page}",
        "woof_shortcode": "woof sections='product_cat+product_cat^Categorie prodotti,pa_colore+pa_colore^Colore,pa_pietra+pa_pietra^Pietra' sections_type='tabs_checkbox'",
    }
    
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


def paginate_products():
    response = requests.get('https://www.sofiaspa.it/catalogo/?reload=true')
    soup = BeautifulSoup(response.content, "html.parser")
    pages = soup.find_all('a', {'class':'page-numbers'})[-2].text.replace('.', '')
    pages = int(pages)
    for i in range(pages):
        page = i + 1
        print(f"Fetching page {page}...")
        data = fetch_products(page)
        if not data:
            print(f'Error in getting page {page}')  # Stop if no data is returned
            continue
        p_soup = BeautifulSoup(data['products'], 'html.parser')
        pdp_links = p_soup.find_all('a', {'class':'woocommerce-LoopProduct-link woocommerce-loop-product__link'})
        for product in pdp_links:
            url = product.get('href')
            if url not in cach.filters:
                cach.filters += [url]
                print('Fetching data from product -> ',url)
                yield requests.get(url)
            

def parse_details():
    import csv
    file =  open('./data.csv', 'w+', newline='', encoding='utf-8-sig')
    csv_file = csv.writer(file)
    try:
        csv_file.writerow(['Riferimento', 'Peso'])
        for response in paginate_products():
            soup = BeautifulSoup(response.content, "html.parser")
            riferimento = soup.find('span', {'class': 'sku qodef-woo-meta-value'}).text
            peso = soup.find('tr', {'class': 'woocommerce-product-attributes-item woocommerce-product-attributes-item--weight'}).find(
                'td', {'class':'woocommerce-product-attributes-item__value'}
            ).text
            csv_file.writerow([riferimento, peso])
    except:
        pass
    file.close()

print('stating bot ...')
parse_details()
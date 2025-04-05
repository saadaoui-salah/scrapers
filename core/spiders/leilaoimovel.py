import scrapy
from w3lib.html import remove_tags
import re

class LeilaoimovelSpider(scrapy.Spider):
    name = "leilaoimovel"
    start_urls = ["https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis"]
    url = "https://venda-imoveis.caixa.gov.br/sistema/carregaPesquisaImoveis.asp"
    headers = {
        "accept": "*/*",
        "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "dnt": "1",
        "origin": "https://venda-imoveis.caixa.gov.br",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            headers=self.headers,
            callback=self.parse
        )

    def parse(self, response):
        states = response.css('select[name="cmb_estado"] option::attr(value)').getall()
        modality = {
            '1º Leilão SFI':4,
            '2º Leilão SFI':5,
            'Licitação Aberta':21,
            'Venda Direta Online':34,
            'Venda Online':33,
            'Leilão SFI - Edital Único':14
        }
        for state in states:
            for mod, value in modality.items():
                pdp_data = {
                    "cmb_estado": state,
                    "cmb_cidade": "",
                    "cmb_modalidade": str(value),
                    "cmb_tp_imovel": "Selecione",
                    "cmb_quartos": "Selecione",
                    "cmb_vg_garagem": "Selecione",
                    "cmb_area_util": "Selecione",
                    "cmb_faixa_vlr": "Selecione",
                    "hdn_estado": state,
                    "hdn_cidade": "",
                    "hdn_bairro": "",
                    "hdn_nobairro": "",
                    "hdn_nocidade": "",
                    "hdn_tp_venda": "0",
                    "hdn_tp_imovel": "Selecione",
                    "hdn_quartos": "Selecione",
                    "hdn_vg_garagem": "Selecione",
                    "hdn_area_util": "Selecione",
                    "hdn_faixa_vlr": "Selecione",
                    "hdninteresse": "",
                    "hdn_modalidade": str(value),
                    "hdnNumLicit": "",
                    "hdnSgComissao": "",
                    "hdnNumTipoVenda": "0",
                    "hdnValorSimulador": "",
                    "hdnAceitaFGTS": "",
                    "hdnAceitaFinanciamento": "",
                    "hdnorigem": "buscaimovel",
                }
                data = {
                    "hdn_estado": state,
                    "hdn_cidade": "",
                    "hdn_bairro": "",
                    "hdn_tp_venda": str(value),
                    "hdn_tp_imovel": "Selecione",
                    "hdn_area_util": "Selecione",
                    "hdn_faixa_vlr": "Selecione",
                    "hdn_quartos": "Selecione",
                    "hdn_vg_garagem": "Selecione",
                    "strValorSimulador": "",
                    "strAceitaFGTS": "",
                    "strAceitaFinanciamento": ""
                }
                yield scrapy.FormRequest(self.url, method="POST", headers=self.headers, 
                formdata=data, callback=self.parse_pagination, meta={'modality': mod, 'payload':pdp_data})

    def update_payload(self, response):
        pdp_data = response.meta['payload']
        inputs = response.css('input')
        for inpt in inputs:
            key = inpt.css('::attr(name)').get()
            value = inpt.css('::attr(value)').get()
            pdp_data[str(key)] = str(value)
        response.meta['payload'] = pdp_data
        return response.meta

    def parse_pagination(self, response):
        ids = response.xpath('//input[contains(@id, "hdnImov")]/@value').getall()
        for list_id in ids:
            response.meta['ids'] = list_id
            data = {'hdnImov': list_id}
            yield scrapy.FormRequest('https://venda-imoveis.caixa.gov.br/sistema/carregaListaImoveis.asp', 
            method="POST", headers=self.headers, 
            formdata=data, callback=self.parse_properties, meta=self.update_payload(response))

    def parse_properties(self, response):
        ids = response.css('.control-group .control-item span strong a::attr(onclick)').getall()
        if not ids: 
            ids = response.css('.control-group .control-item a::attr(onclick)').getall()
        for list_id in ids:
            data = self.update_payload(response)['payload']
            try:
                data['hdnimovel'] = list_id.split('detalhe_imovel(')[1].split('); return false')[0]
            except IndexError:
                continue
        yield scrapy.FormRequest('https://venda-imoveis.caixa.gov.br/sistema/detalhe-imovel.asp', 
        method="POST", headers=self.headers, meta=response.meta,
        formdata=data, callback=self.parse_details)

    def parse_details(self, response):
        name = response.css('h5::text').get()
        property_id = response.css('[name="hdnimovel"]::attr(value)').get()
        city, state = remove_tags(response.xpath("//span[contains(text(), 'Comarca')]").get('')).replace('Comarca: ', '').split('-')
        address = response.xpath("//p/strong[contains(text(), 'Endereço')]/../text()").get()
        quartos = response.xpath("//span[contains(text(), 'Quartos')]/strong/text()").get()
        garagem = response.xpath("//span[contains(text(), 'Garagem')]/strong/text()").get()
        banheiros = '-'
        private_area = response.xpath("//span[contains(text(), 'Área privativa')]/strong/text()").get()
        public_area = response.xpath("//span[contains(text(), 'Área do terreno')]/strong/text()").get()
        type_ = response.xpath("//span[contains(text(), 'Tipo de imóvel')]/strong/text()").get()
        values = response.xpath("//p[contains(text(), 'Valor')]").get().split('<br>')

        fim_venda_online = response.xpath("//span[contains(text(), 'Data da Licitação Aberta')]/text()").get('').split('-')
        if len(fim_venda_online) > 1:
            fim_venda_online = '-'.join(fim_venda_online[1:])
        else:
            fim_venda_online = None

        fim_1 = response.xpath("//span[contains(text(), 'Data do 1º Leilão')]/text()").get('').split('-')
        fim_1 = '-'.join(fim_1[1:])
        fim_2 = response.xpath("//span[contains(text(), 'Data do 2º Leilão')]/text()").get('').split('-')
        fim_2 = '-'.join(fim_2[1:])

        if response.meta['modality'] == 'Venda Direta Online':
            fim_1 = fim_1 or 'N/A'
            fim_2 = fim_2 or 'N/A'
        else:
            fim_1 = fim_1 or '-'
            fim_2 = fim_2 or '-'
        
        description = response.xpath("//strong[contains(text(), 'Descrição')]/../text()").get()
        title = response.css('h5::text').get()
        inscricao_imobiliaria = response.xpath("//span[contains(text(), 'Inscrição imobiliária')]/strong/text()").get()
        matricula_number = response.xpath("//span[contains(text(), 'Matrícula(s):')]/strong/text()").get()
        edital_number = response.xpath("//span[contains(text(), 'Edital: ')]/text()").get()
        number_property_edital = response.xpath("//span[contains(text(), 'Número do item:')]/text()").get('').split(': ')
        if len(number_property_edital) == 2:
            number_property_edital = number_property_edital[-1]
        else:
            number_property_edital = 'N/A'

        js_code = response.xpath("//script[contains(text(), 'regrasVendaOnline')]/text()").get('')
        pattern = r'(?<!\/\/)window\.open\(["\']([^"\']+)["\']\)'
        matches = re.findall(pattern, js_code)
        regras_de_venda_url = [f"https://venda-imoveis.caixa.gov.br{matche}" for matche in matches if '/editais/regras-VOL/' in matche]
        regras_de_venda_url = regras_de_venda_url[0] if regras_de_venda_url else "N/A"
        
        if not fim_venda_online: 
            pattern = r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})'
            matches = re.search(pattern, js_code)
            fim_venda_online = matches.group(0) if matches else 'N/A'

        edital_url = response.xpath("//a/strong[contains(text(),'Baixar edital e anexos')]/../@onclick").get('')
        edital_url = edital_url.replace("javascript:ExibeDoc('", '').replace("')",'')
        edital_url = f"https://venda-imoveis.caixa.gov.br{edital_url}" if edital_url else 'N/A' 
        
        matricula_url = response.xpath("//a[contains(text(), 'Baixar matrícula do imóvel')]/@onclick").get('')
        matricula_url = matricula_url.replace("javascript:ExibeDoc('", '').replace("')", '')
        matricula_url = f"https://venda-imoveis.caixa.gov.br{matricula_url}" if matricula_url else 'N/A' 

        images = response.css('.thumbnails img::attr(src)').getall()
        images = [f"https://venda-imoveis.caixa.gov.br{image}" for image in images]

        aceita_financiamento = None
        aceita_FGTS = None
        aceita_parcelamento = None
        aceita_consorcio = None
        bullets = response.xpath("//p/i[contains(@class, 'fa-info-circle')]/../text()").getall()
        other_bullets = []
        for bullet in bullets:
            if 'financiamento' in bullet.lower():
                aceita_financiamento = bullet
                continue
            elif 'FGTS' in bullet:
                aceita_FGTS = bullet
                continue
            elif 'parcelamento' in bullet.lower():
                aceita_parcelamento = bullet
                continue
            elif 'consorcio' in bullet.lower() or 'consórcio' in bullet.lower():
                aceita_consorcio = bullet
                continue
            else:
                other_bullets += [bullet]

        item = {
            'url':f'https://venda-imoveis.caixa.gov.br/sistema/detalhe-imovel.asp?hdnOrigem=index&hdnimovel={property_id}',
            'id': property_id,
            'modality':response.meta['modality'],
            'state': state,
            'city': city,
            'address': address,
            'quartos': quartos or '-',
            'garagem': garagem or '-',
            'banheiros': banheiros,
            'private_area':private_area,
            'total_area':public_area or '-',
            'type':type_,
            'fim_1': fim_1,
            'fim_2': fim_2,
            'fim_venda_online':fim_venda_online,
            'description': description,
            'aceita_financiamento':aceita_financiamento,
            'aceita_FGTS':aceita_FGTS,
            'aceita_parcelamento':aceita_parcelamento,
            'aceita_consorcio':aceita_consorcio,
            'ps': other_bullets,
            'title':title,
            'inscricao_imobiliaria':inscricao_imobiliaria,
            'matricula_number':matricula_number,
            'number_property_edital':number_property_edital,
            'matricula_url':matricula_url,
            'regras_de_venda_url':regras_de_venda_url,
            'edital_url':edital_url,
            'images': images
        }
        for value in values:
            if 'Valor mínimo de venda 2º Leilão' in value:
                item['preco_venda'] = remove_tags(value)
            if 'Valor de avaliação' in value:
                item['preco_avaliacao'] = remove_tags(value).removeprefix('Valor de avaliação: R$ ')
            if 'Valor mínimo de venda' in value: 
                item['sale_value'] = remove_tags(value).removeprefix('Valor mínimo de venda: R$ ').split('(')[0].strip()
            if 'desconto' in value:
                pattern = r"(\d{1,3}(?:,\d{1,2})?)%"
                match = re.search(pattern, value)
                if match:
                    item['desconto'] = match.group(1)
                else:
                    item['desconto'] = "0%"


        yield item


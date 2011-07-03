#- coding: utf-8
from BeautifulSoup import BeautifulSoup
import cookielib
import re
import urllib
import urllib2

URL_CORREIOS = 'http://www.buscacep.correios.com.br/servicos/dnec/'

class Correios():
    def __init__(self, proxy=None):
        cj = cookielib.LWPCookieJar()
        cookie_handler = urllib2.HTTPCookieProcessor(cj)
        if proxy:
            proxy_handler = urllib2.ProxyHandler({'http': proxy})
            opener = urllib2.build_opener(proxy_handler, cookie_handler)
        else:
            opener = urllib2.build_opener(cookie_handler)
        urllib2.install_opener(opener)

    def _url_open(self, url, data=None, headers=None):
        if headers == None:
            headers = {}

        headers['User-agent'] = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        encoded_data = urllib.urlencode(data) if data else None
        url = URL_CORREIOS + url
        
        req = urllib2.Request(url, encoded_data, headers)
        handle = urllib2.urlopen(req)

        return handle

    def _parse_detalhe(self, html):
        soup = BeautifulSoup(html.decode('ISO-8859-1'))

        value_cells = soup.findAll('td', attrs={'class': 'value'})
        values = [cell.firstText(text=True) for cell in value_cells]
        localidade, uf = values[2].split('/')
        values_dict = {
            'Logradouro': values[0],
            'Bairro': values[1],
            'Localidade': localidade,
            'UF': uf,
            'CEP': values[3]
        }
        return values_dict              

    def _parse_linha_tabela(self, tr):
        values = [cell.firstText(text=True) for cell in tr.findAll('td')]        
        keys = ['Logradouro', 'Bairro', 'Localidade', 'UF', 'CEP']
        return dict(zip(keys, values))
        
    def _parse_tabela(self, html):
        soup = BeautifulSoup(html)
        linhas = soup.findAll('tr', attrs={
            'onclick': re.compile(r"javascript:detalharCep\('\d+','\d+'\);")
        })        
        return [self._parse_linha_tabela(linha) for linha in linhas]

    def detalhe(self, posicao=0):
        """Retorna o detalhe de um CEP da última lista de resultados"""
        handle = self._url_open('detalheCEPAction.do', {'Metodo': 'detalhe',
                                                        'TipoCep': 2,
                                                        'Posicao': posicao + 1,
                                                        'CEP': ''})
        html = handle.read()
        return self._parse_detalhe(html)
        
    def consulta(self, endereco, primeiro=False, 
                 uf=None, localidade=None, tipo=None, numero=None):
        """Consulta site e retorna lista de resultados"""
        
        if uf is None:
            url = 'consultaEnderecoAction.do'
            data = {
                'relaxation': endereco.encode('ISO-8859-1'),
                'TipoCep': 'ALL',
                'semelhante': 'N',
                'cfm': 1,
                'Metodo': 'listaLogradouro',
                'TipoConsulta': 'relaxation',
                'StartRow': '1',
                'EndRow': '10'
            }
        else:
            url = 'consultaLogradouroAction.do'
            data = {
                'Logradouro': endereco.encode('ISO-8859-1'),
                'UF': uf,
                'TIPO': tipo,
                'Localidade': localidade.encode('ISO-8859-1'),
                'Numero': numero,
                'cfm': 1,
                'Metodo': 'listaLogradouro',
                'TipoConsulta': 'logradouro',
                'StartRow': '1',
                'EndRow': '10'
            }
        
        h = self._url_open(url, data)
        html = h.read()
        
        if primeiro:
            return self.detalhe()
        else:
            return self._parse_tabela(html)

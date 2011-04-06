# url imports
from BeautifulSoup import BeautifulSoup
import cookielib
import urllib
import urllib2

URL = 'http://www.buscacep.correios.com.br/servicos/dnec/'

class Correios():
    def __init__(self, proxy=None):
        cj = cookielib.LWPCookieJar()
        cookie_handler = urllib2.HTTPCookieProcessor(cj)
        if proxy:
            proxy_handler = urllib2.ProxyHandler({
                'http': proxy,
                'https': proxy,
            })
            opener = urllib2.build_opener(proxy_handler, cookie_handler)
        else:
            opener = urllib2.build_opener(cookie_handler)
        urllib2.install_opener(opener)

    def _url_open(self, url, data=None, headers=None):
        if headers == None:
            headers = {}

        if url[:4] != 'http':
            url = URL + url

        headers['User-agent'] = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        req = urllib2.Request(url, urllib.urlencode(data) if data else None, headers)
        handle = urllib2.urlopen(req)

        return handle

    def _detalhe(self, posicao=1):
        """Retorna o resultado detalhado"""
        handle = self._url_open('detalheCEPAction.do', {'Metodo': 'detalhe',
                                                        'TipoCep': 2,
                                                        'Posicao': posicao,
                                                        'CEP': None})
        html = handle.read()
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
        

    def consulta(self, endereco):
        """Consulta e retorna detalhe do primeiro resultado"""
        h = self._url_open('consultaEnderecoAction.do', {'relaxation': endereco.encode('ISO-8859-1'),
                                                         'TipoCep': 'ALL',
                                                         'semelhante': 'N',
                                                         'cfm': 1,
                                                         'Metodo': 'listaLogradouro',
                                                         'TipoConsulta': 'relaxation',
                                                         'StartRow': '1',
                                                         'EndRow': '10'})
        html = h.read()
        return self._detalhe(1)

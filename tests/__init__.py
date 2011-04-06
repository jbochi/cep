#- coding: utf-8
import os
import unittest

from cep import Correios


DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')

class TestIntegration(unittest.TestCase):
    def test_resultado_cep_conhecido(self):
        c = Correios(proxy='10.138.15.10:8080')
        r = c.consulta('91370000')
        self.assertEquals(r['CEP'], '91370-000')
        self.assertEquals(r['Localidade'], 'Porto Alegre')
        self.assertEquals(r['Bairro'], 'Vila Ipiranga')
        self.assertEquals(r['UF'], 'RS')
        self.assertEquals(r['Logradouro'], u'Rua Alberto Silva - até 965/966')

class TestParse(unittest.TestCase):
    def pega_conteudo_arquivo(self, nome):
        arquivo = os.path.join(DATA_PATH, nome)
        f = open(arquivo, 'r')
        html = f.read()
        f.close()
        return html    

    def test_parse_cep_conhecido(self):
        html = self.pega_conteudo_arquivo('exemplo_resultado.html')
        c = Correios()
        r = c._parse_detalhe(html)
        self.assertEquals(r['CEP'], '22631-004')
        self.assertEquals(r['Localidade'], 'Rio de Janeiro')
        self.assertEquals(r['Bairro'], 'Barra da Tijuca')
        self.assertEquals(r['UF'], 'RJ')
        self.assertEquals(r['Logradouro'], u'Avenida das Américas - '
                                           u'de 3979 a 5151 - lado ímpar')

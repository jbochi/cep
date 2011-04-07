#- coding: utf-8
import os
import unittest

from cep import Correios

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.c = Correios(proxy='10.138.15.10:8080')
        
    def test_resultado_cep_conhecido(self):
        r = self.c.consulta('91370000', primeiro=True)
        self.assertEquals(r['CEP'], '91370-000')
        self.assertEquals(r['Localidade'], 'Porto Alegre')
        self.assertEquals(r['Bairro'], 'Vila Ipiranga')
        self.assertEquals(r['UF'], 'RS')
        self.assertEquals(r['Logradouro'], u'Rua Alberto Silva - até 965/966')

    def test_tabela_resultados_conhecida(self):
        r = self.c.consulta(u'Rua Alberto Silva - até 965/966')
        self.assertEquals(r[0]['CEP'], '91370-000')

    def test_resultados_localidade(self):
        r = self.c.consulta(u'Alberto Silva', 
                            uf='RS', 
                            localidade='Porto Alegre',
                            tipo='Rua',
                            numero=54)
                            
        self.assertEquals(len(r), 3)
        self.assertEquals(r[1]['CEP'], '91370-000')        


class TestParse(unittest.TestCase):
    def setUp(self):
        self.c = Correios()

    def pega_conteudo_arquivo(self, nome):
        arquivo = os.path.join(DATA_PATH, nome)
        f = open(arquivo, 'r')
        html = f.read()
        f.close()
        return html

    def test_parse_cep_conhecido(self):
        html = self.pega_conteudo_arquivo('exemplo_resultado.html')
        r = self.c._parse_detalhe(html)
        self.assertEquals(r['CEP'], '22631-004')
        self.assertEquals(r['Localidade'], 'Rio de Janeiro')
        self.assertEquals(r['Bairro'], 'Barra da Tijuca')
        self.assertEquals(r['UF'], 'RJ')
        self.assertEquals(r['Logradouro'], u'Avenida das Américas - '
                                           u'de 3979 a 5151 - lado ímpar')
                                           
    def test_parse_nao_existente(self):
        html = self.pega_conteudo_arquivo('exemplo_lista_nao_encontrado.html')
        r = self.c._parse_tabela(html)
        self.assertEquals(r, [])
        
    def test_parse_tabela(self):
        html = self.pega_conteudo_arquivo('exemplo_lista_grande.html')
        r = self.c._parse_tabela(html)
        self.assertEquals(len(r), 80)
        self.assertEquals(r[0]['Logradouro'], 'Rua Alberto Silva')
        self.assertEquals(r[0]['Bairro'], 'Itaigara')
        self.assertEquals(r[0]['Localidade'], 'Salvador')
        self.assertEquals(r[0]['UF'], 'BA')
        self.assertEquals(r[0]['CEP'], '41815-000')

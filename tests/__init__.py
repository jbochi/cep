#- coding: utf-8
import unittest

from cep import Correios

class Test(unittest.TestCase):
    def test_resultados_cep_conhecido(self):
        c = Correios(proxy='10.138.15.10:8080')
        r = c.consulta('91370000')
        self.assertEquals(r['CEP'], '91370-000')
        self.assertEquals(r['Localidade'], 'Porto Alegre')
        self.assertEquals(r['Bairro'], 'Vila Ipiranga')
        self.assertEquals(r['UF'], 'RS')
        self.assertEquals(r['Logradouro'], u'Rua Alberto Silva - até 965/966')
   

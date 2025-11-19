from pages.cadastro_login import CadastroLogin


class Inscreverse(CadastroLogin):
    def __init__(self, page):
        super().__init__(page)
        self.checkbox_mr = page.get_by_role("radio", name="Mr.")
        self.checkbox_mrs = page.get_by_role("radio", name="Mrs.")
        self.input_nome = page.get_by_role(
            "textbox", name="Name *", exact=True)
        self.input_senha = page.get_by_role("textbox", name="Password *")
        self.checkbox_sign_up_for_our_newsletter = page.get_by_text(
            "Sign up for our newsletter!")
        self.checkbox_receive_special_offers_from = page.get_by_text(
            "Receive special offers from")
        self.select_dia = page.locator("#days")
        self.select_mes = page.locator('#months')
        self.select_ano = page.locator('#years')
        self.input_primeiro_nome = page.get_by_role(
            "textbox", name="First name *")
        self.input_sobrenome = page.get_by_role("textbox", name="Last name *")
        self.input_empresa = page.get_by_role(
            "textbox", name="Company", exact=True)
        self.input_endereco = page.get_by_role(
            "textbox", name="Address * (Street address, P.")
        self.input_endereco_2 = page.get_by_role("textbox", name="Address 2")
        self.input_estado = page.get_by_role("textbox", name="State *")
        self.input_cidade = page.get_by_role(
            "textbox", name="City * Zipcode *")
        self.input_zipcode = page.locator("#zipcode")
        self.input_numero_telefone = page.get_by_role(
            "textbox", name="Mobile Number *")
        self.select_pais = page.get_by_label("Country *")
        self.botao_criar_conta = page.get_by_role(
            "button", name="Create Account")
        self.botao_continuar = page.get_by_role("link", name="Continue")
        self.botao_deletar_conta = page.get_by_role(
            "link", name="Delete Account")

    def preencher_informacoes_da_conta(
            self,
            titulo='',
            nome='',
            senha='',
            data_aniversario='',
            sign_up_for_our_newsletter: bool = True,
            receive_special_offers_from: bool = True):
        if titulo == 'Mr':
            self.checkbox_mr.check()
        if titulo == 'Mrs':
            self.checkbox_mrs.check()

        if nome:
            self.input_nome.fill(nome)

        if senha:
            self.input_senha.fill(senha)

        if data_aniversario:
            dia, mes, ano = data_aniversario.split('/')
            if mes.startswith('0'):
                mes = mes[1:]
            if dia.startswith('0'):
                dia = dia[1:]
            self.select_dia.select_option(dia)
            self.select_mes.select_option(mes)
            self.select_ano.select_option(ano)
        if sign_up_for_our_newsletter:
            self.checkbox_sign_up_for_our_newsletter.check()
        else:
            self.checkbox_sign_up_for_our_newsletter.uncheck()
        if receive_special_offers_from:
            self.checkbox_receive_special_offers_from.check()
        else:
            self.checkbox_receive_special_offers_from.uncheck()

    def preencher_informacoes_endereco(
            self,
            primeiro_nome='',
            sobrenome='',
            empresa='',
            endereco='',
            endereco_2='',
            pais='',
            estado='',
            cidade='',
            zipcode='',
            numero_telefone=''):
        if primeiro_nome:
            self.input_primeiro_nome.fill(primeiro_nome)
        if sobrenome:
            self.input_sobrenome.fill(sobrenome)
        if empresa:
            self.input_empresa.fill(empresa)
        if endereco:
            self.input_endereco.fill(endereco)
        if endereco_2:
            self.input_endereco_2.fill(endereco_2)
        if pais:
            self.select_pais.select_option(pais)
        if estado:
            self.input_estado.fill(estado)
        if cidade:
            self.input_cidade.fill(cidade)
        if zipcode:
            self.input_zipcode.fill(zipcode)
        if numero_telefone:
            self.input_numero_telefone.fill(numero_telefone)

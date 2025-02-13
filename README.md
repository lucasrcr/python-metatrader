# python-metatrader
Uma implementação python para usar a plataforma metatrader 5.

Neste protótipo, mostro como fazer o login na sua conta do metatrader 5 usando python. O código exemplifica a entrada no mercado EUR-USD comprando.
O usuário pode escolher o tamanho do takeprofit e do stoploss, bem como adicionar estratégias e indicadores que desejar.

Basta inserir os dados da conta em:

    # logando na conta
    login = xxxxx
    password = 'xxxx'
    investidor = 'xxxx'
    server = 'MetaQuotes-Demo'
    mt.login(login,password,server)

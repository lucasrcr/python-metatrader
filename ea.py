import MetaTrader5 as mt
import pandas as pd
from datetime import datetime, timedelta, time
import time as ti
import numpy as np
import pandas_ta as ta

take_profit_pips = 5  # Substitua pelo número de pips para o take profit desejado
stop_loss_pips = 10 # Substitua pelo número de pips para o stop loss desejado

# É preciso descontar uma hora, pois as ordens ocorrem em GMT-1.
hora_inicio_trading = time(20,0)      #21 horas em brasília.
hora_fim_trading = time(19, 0)        #19
pip_value = 0.0001
stop_loss_inicial = stop_loss_pips * pip_value
take_profit_inicial = take_profit_pips * pip_value


#function to send a market order
def market_order(symbol,volume,order_type,magic_number,tp,sl):
    tick = mt.symbol_info_tick(symbol)
    order_dict = {'buy' : 0 , 'sell' : 1}
    price_dict = {'buy' : tick.ask, 'sell' : tick.bid}
    stop_loss_price_dict = {'buy': mt.symbol_info_tick(symbol).ask - sl, 'sell': mt.symbol_info_tick(symbol).bid + sl}
    take_profit_price_dict = {'buy': mt.symbol_info_tick(symbol).ask + tp, 'sell': mt.symbol_info_tick(symbol).bid - tp}
    request = {
        "action": mt.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume, # FLOAT
        "type": order_dict[order_type],
        "price": price_dict[order_type],
        "sl": stop_loss_price_dict[order_type], # FLOAT
        "tp": take_profit_price_dict[order_type], # FLOAT
        "deviation": 20, # INTERGER   #slippage
        "magic": magic_number, # INTERGER
        "comment": "python script open",
        "type_time": mt.ORDER_TIME_GTC,
        "type_filling": mt.ORDER_FILLING_IOC,
    }
    order_result = mt.order_send(request)
    print(order_result)
    # print(order_result.request.comment)
    print(order_result.volume)


    return order_result,order_result.volume

if __name__ == '__main__':

    symbol1 = 'EURUSD'
    # symbol2 = 'GBPUSD'
    # symbol3 = 'EURGBP'

    volume = 0.01
    from_date=datetime.now()+timedelta(hours=2)   # Comente esse em caso de utilizar o from_date para problemas técnicos.
    #abrindo o mt5
    mt.initialize()

    # logando na conta
    login = xxxxx
    password = 'xxxx'
    investidor = 'xxxx'
    server = 'MetaQuotes-Demo'
    mt.login(login,password,server)

    # # informações da conta
    account_info = mt.account_info()
    equity_inicial = account_info.equity


    while True:

        # informações da conta
        account_info = mt.account_info()
        equity = account_info.equity
        # print(equity,meta_equity)

        'Ajustando o horário permitido'
        # Obter a hora atual
        hora_atual = datetime.now().time()

        # Converter hora_atual em um objeto datetime
        dt_atual = datetime.combine(datetime.today(), hora_atual)

        # Adicionar duas horas
        nova_hora = dt_atual + timedelta(hours=2)

        # Extrair apenas o componente de tempo da nova hora
        nova_hora_time = nova_hora.time()

        if nova_hora_time > hora_inicio_trading or nova_hora_time <= hora_fim_trading:      #É maior que 23 horas (ex. 23:59) ativo. (00:01) é menor que 19:00, i.e. ativo. Temos que considerar os segundos também.
                    if not mt.positions_get(symbol="EURUSD"):
                        sl = stop_loss_inicial
                        tp = take_profit_inicial
                        volume_temp = market_order(symbol1,volume,'buy',100,tp,sl)[1]

        else:
            print(f'fora do horário permitido')
            # Convertendo para objetos datetime completos
            nova_hora_time = datetime.combine(datetime.today(), nova_hora_time)
            hora_inicio_trading = datetime.combine(datetime.today(), hora_inicio_trading)
            diferenca_tempo =    hora_inicio_trading - nova_hora_time
            diferenca_segundos = diferenca_tempo.total_seconds()
            print(hora_inicio_trading)
            print(nova_hora_time)   # hora atual
            print(f"A diferença é de {diferenca_segundos} segundos.")
            hora_inicio_trading = time(23,0)
            if diferenca_segundos<0:
                ti.sleep(86400 + diferenca_segundos)
            else:
                ti.sleep(diferenca_segundos)

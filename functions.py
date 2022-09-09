# Aquí se hacen las funciones complejas que se van a mandar a llamar.

import yfinance as yf
import pandas as pd
import numpy as np
from scipy.optimize import minimize

# Inversión pasiva
def inv_pasiva(precios_p,tickers,capital,dates_pasiva):
    inv_pasiva = []
    posturas = pd.DataFrame({"Symbols": tickers,
             "Pesos (%)": precios_p["Pesos (%)"],
             "Precio": precios_p.iloc[:,1]
            })
             
    posturas["Posturas"] =  capital*(posturas["Pesos (%)"]/100)
    posturas["Títulos"] = posturas["Posturas"]/posturas["Precio"]
    
    for i in range(19):
        posturas["Precio"] = precios_p.iloc[:,i+1]
        posturas["Posturas"] =  posturas["Precio"]*posturas["Títulos"]

        inv_pasiva.append({
            "timestamp":dates_pasiva[i],
            "Capital": round(posturas["Posturas"].sum(),2)
        })
    df_pasiva = pd.DataFrame(inv_pasiva)


    df_pasiva["Rend"] = df_pasiva["Capital"].pct_change().fillna(0)*100
    df_pasiva["Rend Acum"] = df_pasiva["Rend"].cumsum()
    return df_pasiva

# Datos para portafolio eficiente
Varianza = lambda pesos, sigma: pesos.T.dot(sigma.dot(pesos))
Valor_esp = lambda pesos, rendimientos: pesos.dot(rendimientos)
Sharpe_Port = lambda pesos, rendimientos, rf, sigma: -(Valor_esp(pesos,rendimientos)-rf) / (Varianza(pesos, sigma)**0.5)

#Portafolio eficiente
def Portafolio_Eficiente(rendimientos, rf, sigma):
    n = len(rendimientos)
    w0 = np.ones(n) / n
    bnds = ((0,None),) * n
    cons = {"type": "eq", "fun": lambda pesos:pesos.sum()-1}
    emv = minimize(fun = Sharpe_Port, x0 = w0, args = (rendimientos, rf, sigma), bounds = bnds,
                   constraints = cons, tol = 1e-10)
    return np.round(emv.x,4)

# Invresión activa
def activa(dates_activa, precios_act, capital, cash, comision):
    inv_activa=[]
    operaciones=[{"timestamp": "2022-01-31",
                "titulos_compra": 0,
                "comision": 0,
                 }]

    for i in range(len(dates_activa)-1):
        if cash > 0:

            for j in range(33):
                dif = 0
                compra = 0
                venta = 0
                precios_act["Precio periodo"] = precios_act.iloc[:,i+2]

                # Venta
                if ((precios_act.iloc[j,i+2] / precios_act.iloc[j,i+1])-1) <= -.05:

                    dif = precios_act.iloc[j,20]
                    precios_act.iloc[j,20] = round(precios_act.iloc[j,20]*0.975,0) # Se le resta el 2.5% de títulos
                    venta = dif - precios_act.iloc[j,20] 
                    cash = cash + (compra * precios_act.iloc[j,i+2])

                    precios_act.iloc[j,19] = precios_act.iloc[j,i+2] * precios_act.iloc[j, 20] # Se modifica la postura

                #Compra
                elif ((precios_act.iloc[j,i+2] / precios_act.iloc[j,i+1])-1) >= .05:

                    dif = precios_act.iloc[j,20]
                    precios_act.iloc[j,20] = round(precios_act.iloc[j,20]*1.025,0) # Se le aumenta el 2.5% de títulos
                    compra = precios_act.iloc[j,20] - dif
                    cash = cash - (compra * precios_act.iloc[j,i+2] * comision)
                    comi = compra * precios_act.iloc[j,i+2] * comision

                    precios_act.iloc[j,19] = precios_act.iloc[j,i+2] * precios_act.iloc[j, 20] # Se modifica postura (titulos*precio)

                # Igual
                else:

                    pass


                precios_act.iloc[j,21] = precios_act.iloc[j,21] + compra # Compra de títulos
                precios_act.iloc[j,22] = precios_act.iloc[j,22] + venta  # Venta de títulos


        inv_activa.append({
            "timestamp":dates_activa[i],
            "Capital": round(precios_act["Posturas"].sum(),2),
        })
        operaciones.append({
            "timestamp": dates_activa[i],
            "titulos_compra": compra,
            "comision": round(comi,4),
        })
    return (inv_activa,operaciones)


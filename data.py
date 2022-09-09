# Aquí va toda la carga de datos históricos

# py -m pip install pandas

import functions as fn
import yfinance as yf
import pandas as pd
import numpy as np

# Datos
capital = 1000000
comision = 0.00125

# Limpiamos datos, conocemos el porcentaje de cash y cambiamos los tickers a los correctos.
data = pd.read_csv(r"C:\Users\Sebastian\OneDrive\Escritorio\Laboratorio 1\Laboratorio1\files\NAFTRAC_20200131.csv",skiprows=2)
cash = data["Peso (%)"].loc[[10,32,34]].sum()
data = data.drop([10,32,34,36])
tickers = ["AMXL.MX","FEMSAUBD.MX","GFNORTEO.MX","WALMEX.MX","GMEXICOB.MX","CEMEXCPO.MX","TLEVISACPO.MX","GAPB.MX","ELEKTRA.MX",
"ASURB.MX","KIMBERA.MX","BIMBOA.MX","OMAB.MX","AC.MX","GFINBURO.MX","IENOVA.MX","PINFRA.MX","GRUMAB.MX","ORBIA.MX",'ALFAA.MX', 
'GCARSOA1.MX', 'PE&OLES.MX', 'ALSEA.MX', 'BBAJIOO.MX','GENTERA.MX', 'MEGACPO.MX', 'LIVEPOLC-1.MX', 'BOLSAA.MX', 'CUERVO.MX', 
'LABB.MX','GCC.MX', 'RA.MX', 'ALPEKA.MX']
data["Ticker"] = tickers

# Se descargan precios de las acciones restantes.
precios = yf.download(tickers,"2020-01-01","2022-08-01")

# Fechas que usaremos para tanto la inversión activa como la pasiva
dates_activa = ["2020-01-31","2020-02-28","2020-03-31","2020-04-30","2020-05-29","2020-06-30","2020-07-31","2020-08-31","2020-09-30",
"2020-10-30","2020-01-31","2020-11-30","2020-12-31","2021-01-29","2021-02-26","2021-03-31","2021-04-30","2021-05-31","2021-06-30",
"2021-07-30","2021-08-31","2021-09-30","2021-10-26","2021-11-30","2021-12-31","2022-01-26","2022-02-28","2022-03-31","2022-04-29",
"2022-05-31","2022-06-30","2022-07-29"]

dates_pasiva = ["2021-01-29","2021-02-26","2021-03-31","2021-04-30","2021-05-31","2021-06-30",
"2021-07-30","2021-08-31","2021-09-30","2021-10-26","2021-11-30","2021-12-31","2022-01-26","2022-02-28","2022-03-31","2022-04-29",
"2022-05-31","2022-06-30","2022-07-29"]

# DataFrame limpio
data = data[["Ticker","Peso (%)"]]
data = data.sort_values("Ticker")

# Acomodo de datos para una tabla con los datos limpios
precios = precios["Adj Close"]
precios = precios.fillna(0)
precios_p = precios.loc[dates_pasiva].T

list = []
for i in range(len(data)):
    list.append(data.iloc[i,1])

precios_p.insert(0, 'Pesos (%)',list)

# Inversión pasiva

df_pasiva = fn.inv_pasiva(precios_p,tickers,capital,dates_pasiva)

# --------------------------------------------------------

# Activa

tickers = ["AMXL.MX","FEMSAUBD.MX","GFNORTEO.MX","WALMEX.MX","GMEXICOB.MX","CEMEXCPO.MX","TLEVISACPO.MX","GAPB.MX","ELEKTRA.MX",
"ASURB.MX","KIMBERA.MX","BIMBOA.MX","OMAB.MX","AC.MX","GFINBURO.MX","IENOVA.MX","PINFRA.MX","GRUMAB.MX","ORBIA.MX",'ALFAA.MX', 
'GCARSOA1.MX', 'PE&OLES.MX', 'ALSEA.MX', 'BBAJIOO.MX','GENTERA.MX', 'MEGACPO.MX', 'LIVEPOLC-1.MX', 'BOLSAA.MX', 'CUERVO.MX', 
'LABB.MX','GCC.MX', 'RA.MX', 'ALPEKA.MX']

dates_port = ["2020-01-31","2020-02-28","2020-03-31","2020-04-30","2020-05-29","2020-06-30","2020-07-31","2020-08-31","2020-09-30",
"2020-10-30","2020-01-31","2020-11-30","2020-12-31","2021-01-29"]

dates_activa = ["2021-02-26","2021-03-31","2021-04-30","2021-05-31","2021-06-30",
"2021-07-30","2021-08-31","2021-09-30","2021-10-26","2021-11-30","2021-12-31","2022-01-26","2022-02-28","2022-03-31","2022-04-29",
"2022-05-31","2022-06-30","2022-07-29"]

data2 = pd.read_csv(r"C:\Users\Sebastian\OneDrive\Escritorio\Laboratorio 1\Laboratorio1\files\NAFTRAC_20200131.csv",skiprows=2)
cash_porc = data2["Peso (%)"].loc[[10,32,34]].sum()/100
data2 = data2.drop([10,32,34,36])

data2["Ticker"] = tickers
precios2 = yf.download(tickers,"2020-01-01","2022-08-01")

# Protafolio eficiete
precios_port = precios2["Adj Close"]
precios_port.fillna(0)
precios_port = precios_port.loc[dates_port]

# Datos
precios_log = np.log(precios_port).pct_change()
rend_log = precios_log.dropna()
sigma = rend_log.cov()
rendimientos = rend_log.mean()

#Portafolio eficiente
rf = 0.0429/252
Port_Efic = fn.Portafolio_Eficiente(rendimientos, rf, sigma)

# Limpieza de datos
data_act = pd.DataFrame({
    "Tickers": tickers,
    "Pesos (%)": Port_Efic})

precios_act = precios2["Adj Close"]
precios_act = precios_act.loc[dates_activa].T
precios_act.insert(0, 'Pesos (%)',Port_Efic)
precios_act["Posturas"] = capital* precios_act["Pesos (%)"]
precios_act["Títulos"] = round(precios_act["Posturas"]/precios_act.iloc[:,1],0)
precios_act["Compra títulos"] = np.zeros(33)
precios_act["Venta títulos"] = np.zeros(33)
precios_act["Precio periodo"] = np.zeros(33)

# Datos
capital_inic = 1000000
cash = cash_porc*capital_inic
capital = capital_inic - cash
comision = 0.00125

df_activa = pd.DataFrame(fn.activa(dates_activa, precios_act, capital, cash, comision)[0])
df_activa["Rend"] = df_activa["Capital"].pct_change().fillna(0)*100
df_activa["Rend Acum"] = df_activa["Rend"].cumsum()

# Histórico de operaciones
df_operaciones = pd.DataFrame(fn.activa(dates_activa, precios_act, capital, cash, comision)[1])
df_operaciones["comision_acum"] = df_operaciones["comision"].cumsum()
df_operaciones["titulos_totales"] = df_operaciones["titulos_compra"].cumsum()

# Medidas de atribución al desempeño
rf1 = 4.29
medida = ["rend_m", "rend_c" , "sharpe"]
descripcion = ["Rendimiento Promedio Mensual", "Rendimiento mensual acumulado", "Sharpe Ratio"]
sharpe_pasiva = (df_pasiva["Rend"].mean() - rf1) / df_pasiva["Rend"].std()
sharpe_activa = (df_activa["Rend"].mean() - rf1) / df_activa["Rend"].std()
m_inv_activa = [df_activa["Rend"].mean(), df_activa["Rend Acum"].iloc[-1], sharpe_activa]
m_inv_pasiva = [df_pasiva["Rend"].mean(), df_pasiva["Rend Acum"].iloc[-1], sharpe_pasiva]

df_medidas = pd.DataFrame({
    "medida": medida,
    "descripcion": descripcion,
    "inv_activa": m_inv_activa,
    "inv_pasiva": m_inv_pasiva
})


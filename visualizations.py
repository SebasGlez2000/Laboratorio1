# Aquí estarán los elementos visuales.

import functions as fn
import data as dt
import matplotlib.pyplot as plt

# Gráfica contra el tiempo (pasiva)
def Rend1():
    plt.rcParams["figure.figsize"] = (15,5)
    x = dt.df_pasiva["timestamp"]
    y = dt.df_pasiva["Rend"]
    plt.title('Time vs Rend')
    plt.xlabel('timestamp')
    plt.ylabel('Rend')
    plt.plot(x, y, '-')
    plt.show()
    return


# Gráfica contra el tiempo (pasiva)
def Rend2():
    plt.rcParams["figure.figsize"] = (15,5)
    x = dt.df_pasiva["timestamp"]
    y = dt.df_pasiva["Rend Acum"]
    plt.title('Time vs Rend Acum')
    plt.xlabel('timestamp')
    plt.ylabel('Rend Acum')
    plt.plot(x, y, '-')
    plt.show()
    return
    
def Pastel1():
    pesos = [dt.precios_act["Pesos (%)"]]
    activos = [dt.data["Tickers"]]
    plt.pie(pesos, labels=activos)
    plt.axis("equal")
    plt.show()
    return

# Gráfica contra el tiempo (activa)
def Rend3():
    plt.rcParams["figure.figsize"] = (15,5)
    x = dt.df_activa["timestamp"]
    y = dt.df_activa["Rend"]
    plt.title('Time vs Rend')
    plt.xlabel('timestamp')
    plt.ylabel('Rend')
    plt.plot(x, y, '-')
    plt.show()
    return

# Gráfica contra el tiempo (activa)
def Rend4():
    plt.rcParams["figure.figsize"] = (15,5)
    x = dt.df_activa["timestamp"]
    y = dt.df_activa["Rend Acum"]
    plt.title('Time vs Rend Acum')
    plt.xlabel('timestamp')
    plt.ylabel('Rend Acum')
    plt.plot(x, y, '-')
    plt.show()
    return
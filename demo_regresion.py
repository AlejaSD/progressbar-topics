"""
Demo de Ciencia de Datos - Unidad 3
Aplicación de técnicas de regresión lineal sobre un dataset de salud.

Técnicas demostradas:
1. Linear Regression (scipy.stats.linregress)
2. Regression Table (statsmodels)
3. R-Squared (coeficiente de determinación)

Dataset: inspirado en el ejemplo de W3Schools (Average_Pulse, Duration,
Calorie_Burnage). Se genera sintéticamente para que el script corra sin
depender de archivos externos.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.formula.api as smf

# ----------------------------------------------------------------------
# 1. Preparación de datos
# ----------------------------------------------------------------------
# Generamos un dataset realista donde la duración del entrenamiento
# sí predice las calorías quemadas (relación fuerte), mientras que el
# pulso promedio por sí solo no es un buen predictor.
np.random.seed(42)
n = 50
Duration = np.random.randint(15, 210, n)           # minutos
Average_Pulse = np.random.randint(80, 160, n)      # pulsaciones/min
# La verdad subyacente: las calorías dependen fuerte de la duración
Calorie_Burnage = 5.5 * Duration + 0.4 * Average_Pulse + np.random.normal(0, 40, n)

full_health_data = pd.DataFrame({
    "Duration": Duration,
    "Average_Pulse": Average_Pulse,
    "Calorie_Burnage": Calorie_Burnage.round(0)
})

print("=" * 60)
print("VISTA PREVIA DEL DATASET")
print("=" * 60)
print(full_health_data.head())
print()


# ----------------------------------------------------------------------
# 2. TÉCNICA 1: LINEAR REGRESSION
# ----------------------------------------------------------------------
print("=" * 60)
print("TÉCNICA 1 — LINEAR REGRESSION")
print("=" * 60)

x = full_health_data["Duration"]
y = full_health_data["Calorie_Burnage"]

slope, intercept, r, p, std_err = stats.linregress(x, y)

print(f"Slope (pendiente)      : {slope:.4f}")
print(f"Intercept (intercepto) : {intercept:.4f}")
print(f"r (coef. correlación)  : {r:.4f}")
print(f"p-value                : {p:.6f}")
print()
print(f"Ecuación: Calorie_Burnage = {slope:.2f} * Duration + ({intercept:.2f})")
print()

# Gráfico de la regresión
def recta(x_val):
    return slope * x_val + intercept

mymodel = list(map(recta, x))

plt.figure(figsize=(8, 5))
plt.scatter(x, y, alpha=0.6, label="Datos observados")
plt.plot(x, mymodel, color="red", linewidth=2, label="Recta de regresión")
plt.xlabel("Duration (minutos)")
plt.ylabel("Calorie_Burnage")
plt.title("Regresión lineal: Duration vs Calorie_Burnage")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("grafico_regresion.png", dpi=100)
print("Gráfico guardado como: grafico_regresion.png")
print()


# ----------------------------------------------------------------------
# 3. TÉCNICA 2: REGRESSION TABLE
# ----------------------------------------------------------------------
print("=" * 60)
print("TÉCNICA 2 — REGRESSION TABLE")
print("=" * 60)

model = smf.ols("Calorie_Burnage ~ Duration", data=full_health_data)
results = model.fit()

print(results.summary())
print()

# Lectura interpretada de la tabla
print("--- Lectura de la tabla ---")
print(f"Coeficiente de Duration : {results.params['Duration']:.4f}")
print(f"P-value de Duration     : {results.pvalues['Duration']:.6f}")
print(f"R-squared               : {results.rsquared:.4f}")
print()


# ----------------------------------------------------------------------
# 4. TÉCNICA 3: R-SQUARED
# ----------------------------------------------------------------------
print("=" * 60)
print("TÉCNICA 3 — R-SQUARED")
print("=" * 60)

r_squared = results.rsquared
print(f"R-squared = {r_squared:.4f}  ({r_squared*100:.2f}%)")
print()
print("Interpretación:")
if r_squared > 0.7:
    print(f"  El modelo explica el {r_squared*100:.1f}% de la variabilidad")
    print("  de las calorías quemadas. Es un buen ajuste.")
elif r_squared > 0.3:
    print(f"  El modelo explica el {r_squared*100:.1f}% de la variabilidad.")
    print("  Es un ajuste moderado; se podrían agregar más variables.")
else:
    print(f"  El modelo solo explica el {r_squared*100:.1f}% de la variabilidad.")
    print("  Es un ajuste pobre; la variable no predice bien.")
print()

# Comparación: Average_Pulse SOLO (mal predictor) vs Duration (buen predictor)
print("--- Comparación de predictores ---")
model_pulse = smf.ols("Calorie_Burnage ~ Average_Pulse",
                      data=full_health_data).fit()
print(f"R² usando solo Average_Pulse : {model_pulse.rsquared:.4f}")
print(f"R² usando solo Duration      : {results.rsquared:.4f}")
print()
print("Conclusión: Duration es un mejor predictor de Calorie_Burnage")
print("que Average_Pulse, porque su R² es más alto.")

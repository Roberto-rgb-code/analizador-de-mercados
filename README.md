# Analizador de Estructuras de Mercado

Esta aplicación web, desarrollada con Streamlit, permite analizar estructuras de mercado a partir de datos del Directorio Estadístico Nacional de Unidades Económicas (DENUE). La herramienta calcula índices de concentración, determina estructuras de mercado y aplica modelos económicos relevantes.

## Características

- Cálculo de índices de concentración (HHI, CR4)
- Determinación automática de estructuras de mercado
- Modelos económicos por tipo de estructura:
  - Oligopolio (Cournot, Bertrand, Stackelberg, Cartel)
  - Competencia Perfecta
  - Competencia Monopolística
  - Monopolio
- Visualización de concentración de mercado
- Mapeo geográfico de unidades económicas

## Requisitos

- Python 3.7+
- Streamlit
- Pandas
- NumPy
- Plotly

## Instalación

1. Clone el repositorio:
```bash
git clone https://github.com/tu-usuario/market-analysis.git
cd market-analysis
```

2. Cree un entorno virtual (opcional pero recomendado):
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Instale las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

1. Prepare su archivo CSV con los siguientes campos:
   - Nombre de la Unidad Económica
   - Nombre de clase de la actividad
   - Latitud
   - Longitud
   - Nombre de la vialidad
   - Número exterior o kilómetro

2. Ejecute la aplicación:
```bash
streamlit run app.py
```

3. Abra su navegador en `http://localhost:8501`

4. Cargue su archivo CSV y explore los análisis disponibles

## Estructura de Datos

El archivo CSV debe estar codificado en 'latin1' y contener las siguientes columnas:

```csv
"Nombre de la Unidad Económica","Nombre de clase de la actividad","Latitud","Longitud","Nombre de la vialidad","Número exterior o kilómetro"
"Empresa A","Comercio al por menor",19.4326,-99.1332,"Av. Principal","123"
```

## Metodología

### Cálculo de Índices

- **HHI (Índice Herfindahl-Hirschman)**: Suma de los cuadrados de las participaciones de mercado multiplicado por 10,000
- **CR4**: Suma de las participaciones de mercado de las 4 empresas más grandes

### Determinación de Estructura de Mercado

- **Monopolio**: HHI > 7500 y CR4 > 0.9
- **Oligopolio**: HHI > 2500 y CR4 > 0.6
- **Competencia Monopolística**: HHI > 1500 y más de 10 empresas
- **Competencia Perfecta**: Otros casos

## Modelos Económicos

### Oligopolio

1. **Modelo de Cournot**
   - Equilibrio basado en cantidades
   - Empresas deciden simultáneamente

2. **Modelo de Bertrand**
   - Competencia en precios
   - Precio igual al costo marginal

3. **Modelo de Stackelberg**
   - Empresa líder decide primero
   - Seguidores responden después

4. **Modelo de Cartel**
   - Cooperación entre empresas
   - Maximización de beneficios conjuntos

### Otros Modelos

- **Competencia Perfecta**: Precio igual al costo marginal
- **Competencia Monopolística**: Diferenciación de productos
- **Monopolio**: Maximización de beneficios con poder de mercado

## Contribuir

1. Fork el repositorio
2. Cree una rama para su feature (`git checkout -b feature/AmazingFeature`)
3. Commit sus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abra un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Vea el archivo `LICENSE` para más detalles.

## Contacto

Tu Nombre - [@tutwitter](https://twitter.com/tutwitter) - email@example.com

Link del Proyecto: [https://github.com/tu-usuario/market-analysis](https://github.com/tu-usuario/market-analysis)

# Reconocimiento de Jeroglíficos Egipcios Antiguos

## Descripción del Problema

Este proyecto implementa una solución en Python para el reconocimiento automático de jeroglíficos egipcios antiguos basado en **análisis topológico**. El sistema identifica seis tipos específicos de jeroglíficos mediante el conteo de agujeros (holes) en cada símbolo, aprovechando el concepto de **equivalencia topológica**.

### Jeroglíficos Reconocidos

| Jeroglífico | Código | Número de Agujeros |
|-------------|--------|--------------------|
| Ankh | A | 1 |
| Wedjat | J | 3 |
| Djed | D | 5 |
| Scarab  | S | 4 |
| Was | W | 0 |
| Akhet | K | 2 |

---

## Fundamento Teórico

### Equivalencia Topológica
La solución se basa en el principio de que dos figuras son **topológicamente equivalentes** si una puede transformarse en la otra mediante deformaciones continuas (estiramientos) sin romper ni unir conexiones. Una propiedad topológica invariante es el **número de agujeros** (genus topológico).

### Conectividad-4
El algoritmo utiliza conectividad-4, donde cada píxel tiene 4 vecinos directos (arriba, abajo, izquierda, derecha), excluyendo las diagonales.

## Arquitectura de la Solución

### Componentes Principales

1. **Preprocesamiento de Imagen**
   - Binarización mediante umbralización
   - Adición de borde blanco

2. **Etiquetado de Componentes Conectados**
   - Algoritmo DFS (Depth-First Search) iterativo
   - Identificación de regiones conectadas

3. **Detección de Agujeros**
   - Análisis de vecindad entre componentes
   - Diferenciación entre fondo y agujeros internos

4. **Clasificación y Salida**
   - Mapeo de número de agujeros a caracteres
   - Ordenamiento alfabético

---

## Implementación Técnica

### Algoritmo Principal

```python
def process_image(image_path):
```

### Etiquetado de Componentes Conectados

```python
def dfs_labeling(x, y, current_label, labels, image):
```

### Estrategia de Detección de Agujeros

El algoritmo distingue entre:
- **Fondo principal**: Componente blanco que toca el borde de la imagen
- **Agujeros**: Componentes blancos completamente rodeados por píxeles negros

---

## Análisis de Complejidad

### Complejidad Temporal
- **O(W × H)** donde W = ancho, H = alto de la imagen
- **Justificación**: Cada píxel se visita una vez durante el etiquetado

### Complejidad Espacial
- **O(W × H)** para la matriz de etiquetas
- **O(C)** para estructuras auxiliares, donde C = número de componentes

---

## Dependencias

```python
import cv2          # OpenCV para procesamiento de imágenes
import numpy as np  # Operaciones matriciales eficientes
import matplotlib.pyplot as plt  # Visualización de resultados
```

---

## Instalación
```bash
pip install opencv-python numpy matplotlib
```

---

## Uso del Sistema

### Ejecución Básica
```python
# Cambiar por la ruta de tu imagen de jeroglíficos y luego ejecutar el código
path = "ruta/a/tu/imagen.png"
result = process_image(path)
print(f"\nJeroglíficos reconocidos: {result}\n")
```

### Ejemplo de Salida
```
Jeroglíficos reconocidos: AKW
```

## Casos de Prueba

### Ejemplo 1
- **Entrada**: Imagen con Ankh, Akhet, Was
- **Salida Esperada**: `AKW`
- **Análisis**: 1 agujero (A) + 2 agujeros (K) + 0 agujeros (W)

### Ejemplo 2
- **Entrada**: Imagen con cinco Ankh
- **Salida Esperada**: `AAAAA`
- **Análisis**: Cinco componentes, cada uno con 1 agujero

### Restricciones del Problema:
- Solo reconoce los 6 jeroglíficos especificados
- Requiere que los jeroglíficos no se toquen entre sí
- Asume fondo claro y jeroglíficos oscuros

---

## 👨‍💻 Autora

Solución desarrollada por [Abinues](https://github.com/Abinues) para la materia de Procesamiento Digital de Imágenes - Facultad Politécnica, UNA.
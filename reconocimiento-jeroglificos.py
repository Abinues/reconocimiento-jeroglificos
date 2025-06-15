import cv2
import numpy as np
import matplotlib.pyplot as plt

# Mapeo de número de agujeros a caracteres de jeroglíficos
# 0: Was (W), 1: Ankh (A), 2: Akhet (K), 3: Wedjat (J), 4: Scarab (S), 5: Djed (D)
HOLE_TO_CHAR = {
    0: 'W',
    1: 'A',
    2: 'K',
    3: 'J',
    4: 'S',
    5: 'D'
}

# Direcciones para vecindad de 4 píxeles: derecha, abajo, izquierda, arriba
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def dfs_labeling(x, y, current_label, labels, image):
    """
    Etiqueta un componente conectado usando DFS iterativo.
    
    Parámetros:
        x, y (int): Coordenadas de inicio (columna, fila)
        current_label (int): Etiqueta a asignar al componente
        labels (ndarray): Matriz de etiquetas (se modifica in-place)
        image (ndarray): Imagen binaria (valores 0 o 1)
    
    Funcionamiento:
        - Utiliza pila para evitar recursión infinita
        - Considera conectividad-4 (4 vecinos)
        - Etiqueta todos los píxeles conectados con el mismo valor
    """
    stack = [(x, y)]  # Inicializar pila con punto de partida
    labels[y, x] = current_label  # Etiquetar punto inicial
    
    while stack:
        cx, cy = stack.pop()  # Obtener píxel actual de la pila
        
        # Explorar los 4 vecinos
        for dx, dy in DIRECTIONS:
            nx, ny = cx + dx, cy + dy  # Coordenadas del vecino
            
            # Verificar si el vecino está dentro de los límites de la imagen
            if not (0 <= nx < image.shape[1] and 0 <= ny < image.shape[0]):
                continue
                
            # Condiciones para agregar vecino:
            # 1. Mismo valor que el píxel actual (ambos 0 o ambos 1)
            # 2. Vecino no ha sido etiquetado (etiqueta == 0)
            if image[ny, nx] == image[cy, cx] and labels[ny, nx] == 0:
                labels[ny, nx] = current_label  # Etiquetar vecino
                stack.append((nx, ny))  # Agregar a pila para procesar

def process_image(image_path):
    """
    Procesa una imagen y reconoce jeroglíficos por número de agujeros.
    
    Pasos:
        1. Carga y binarización
        2. Añadir borde blanco
        3. Etiquetar componentes conectados
        4. Identificar fondo
        5. Detectar agujeros
        6. Mapear a caracteres y ordenar
    
    Retorna:
        str: Cadena con caracteres reconocidos en orden alfabético
    """
    # ========================================================================
    # Carga y preprocesamiento de la imagen
    # ========================================================================
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: No se pudo cargar la imagen {image_path}")
        return ""
    
    # Umbralización: 
    # - Jeroglíficos (negros) -> 1
    # - Fondo (blancos) -> 0
    _, bin_img = cv2.threshold(img, 127, 1, cv2.THRESH_BINARY_INV)
    
    # ========================================================================
    # Añadir borde blanco
    # ========================================================================
    # Propósito: 
    # - Asegurar que el fondo sea un solo componente conectado
    # - Facilitar la identificación del fondo principal
    bin_img = np.pad(bin_img, pad_width=1, mode='constant', constant_values=0)
    height, width = bin_img.shape  # Nuevas dimensiones con borde
    
    # ========================================================================
    # Etiquetado de componentes conectados
    # ========================================================================
    # Matriz de etiquetas (inicialmente todas en 0 = no etiquetadas)
    labels = np.zeros((height, width), dtype=int)
    current_label = 1  # Contador de etiquetas (comienza en 1)
    
    # Recorrer cada píxel de la imagen
    for y in range(height):
        for x in range(width):
            # Si el píxel no ha sido etiquetado
            if labels[y, x] == 0:
                # Etiquetar todo el componente conectado
                dfs_labeling(x, y, current_label, labels, bin_img)
                current_label += 1  # Incrementar etiqueta para el próximo componente
    
    # ========================================================================
    # Identificar el fondo principal
    # ========================================================================
    # El fondo principal es el componente que toca el borde
    # Como añadimos un borde blanco (0), el píxel (0,0) siempre pertenece al fondo
    background_label = labels[0, 0]
    
    # ========================================================================
    # Detectar agujeros en jeroglíficos
    # ========================================================================
    # Estructuras para almacenar:
    neighbors = [set() for _ in range(current_label + 1)]  # Conjuntos de vecinos por componente
    black_components = set()  # Componentes de jeroglíficos (píxeles negros)
    
    # Recorrer cada píxel de la imagen
    for y in range(height):
        for x in range(width):
            # Solo procesar píxeles de jeroglíficos (valor 1)
            if bin_img[y, x] == 1:
                comp_label = labels[y, x]  # Etiqueta del componente actual
                black_components.add(comp_label)  # Registrar como componente negro
                
                # Examinar los 4 vecinos
                for dx, dy in DIRECTIONS:
                    nx, ny = x + dx, y + dy  # Coordenadas del vecino
                    
                    # Verificar si el vecino está dentro de la imagen
                    if not (0 <= nx < width and 0 <= ny < height):
                        continue
                    
                    # Condiciones para considerar un agujero:
                    # 1. El vecino es blanco (valor 0)
                    # 2. El componente del vecino NO es el fondo principal
                    if bin_img[ny, nx] == 0 and labels[ny, nx] != background_label:
                        # Registrar el componente blanco como vecino del jeroglífico
                        neighbors[comp_label].add(labels[ny, nx])
    
    # Contar agujeros por jeroglífico:
    # Cada elemento único en neighbors[comp_label] representa un agujero
    hole_counts = {}
    for comp_label in black_components:
        hole_counts[comp_label] = len(neighbors[comp_label])
    
    # ========================================================================
    # Mapear a caracteres y ordenar
    # ========================================================================
    letters = [HOLE_TO_CHAR.get(count, '?') for count in hole_counts.values()]
    letters.sort()  # Orden alfabético
    return ''.join(letters)

# ============================================================================
# Ejecución principal y visualización
# ============================================================================
if __name__ == "__main__":
    # Cambiar por la ruta de tu imagen
    path = "Ejemplo1.png"
    
    # Procesar imagen y obtener resultado
    result = process_image(path)
    print(f"\nJeroglíficos reconocidos: {result}\n")
    
    # Cargar imagen original para visualización
    original_img = cv2.imread(path)
    if original_img is None:
        print("Error: No se pudo cargar la imagen para visualización")
    else:
        # Preparar versión binaria para visualización
        gray_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
        _, bin_img_vis = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY_INV)
        bin_img_vis = np.pad(bin_img_vis, 1, mode='constant', constant_values=0)
        
        # Configurar figura de visualización
        plt.figure(figsize=(15, 5))
        
        # Subfigura 1: Imagen original
        plt.subplot(131)
        plt.imshow(cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB))
        plt.title("Imagen Original")
        plt.axis('off')
        
        # Subfigura 2: Imagen binaria con borde
        plt.subplot(132)
        plt.imshow(bin_img_vis, cmap='gray')
        plt.title("Binaria con Borde")
        plt.axis('off')
        
        # Subfigura 3: Resultado del reconocimiento
        plt.subplot(133)
        plt.text(0.5, 0.5, result, 
                 fontsize=40, 
                 ha='center', 
                 va='center', 
                 color='red')
        plt.title("Resultado: " + result)
        plt.axis('off')
        
        # Mostrar figura
        plt.tight_layout()
        plt.show()
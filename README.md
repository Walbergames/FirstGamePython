# FirstGamePython

Juego de palabras en **Python + Pygame** con arquitectura **Entity Component System (ECS)**.

## Mecánica principal
- Tablero de `5 x 5` fichas con letra + dos números:
  - **Azul** = valor base.
  - **Rojo** = multiplicador acumulado.
- Formas una palabra tocando fichas (sin reutilizar una ficha en la misma jugada).
- Al enviar:
  - Si la palabra existe en diccionario, puntúa:  
    `puntaje = suma(azules) * suma(rojos)`
  - Ese puntaje se resta al objetivo del nivel.
  - Las fichas usadas desaparecen y el tablero se compacta por gravedad tipo Candy Crush.
- Cada nivel permite **5 jugadas**:
  - Si llegas a `0` o menos antes de la 5.ª jugada, subes de nivel.
  - Si tras 5 jugadas no llegas a `0`, pierdes.

## Estructura
- `main.py`: loop principal e input.
- `game/ecs.py`: gestor ECS mínimo.
- `game/components.py`: componentes (posición, ficha, estado).
- `game/board.py`: generación de fichas + gravedad.
- `game/systems.py`: lógica de selección, envío, puntuación y niveles.
- `game/ui.py`: render con Pygame.
- `game/dictionary.py`: carga de diccionario (`words_es.txt`) o fallback interno.

## Ejecutar
```bash
python main.py
```

## Diccionario opcional
Puedes crear un archivo `words_es.txt` en la raíz, una palabra por línea.

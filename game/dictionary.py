from pathlib import Path

DEFAULT_WORDS = {
    "CASA", "SOL", "LUNA", "ROCA", "GATO", "PERRO", "JUEGO", "PYTHON",
    "ROJO", "AZUL", "LETRA", "TABLA", "FICHA", "NUBE", "MAR", "TIERRA",
    "FUEGO", "AGUA", "AIRE", "NORTE", "SUR", "ESTE", "OESTE", "ARTE",
    "MUSICA", "FLOR", "ARBOL", "RUTA", "PUERTA", "VENTANA", "NIVEL",
    "PUNTO", "PALABRA", "CARTA", "RANA", "MONTE", "CIELO", "DADO", "PESO",
}


def load_dictionary(path: str = "words_es.txt") -> set[str]:
    file_path = Path(path)
    if not file_path.exists():
        return DEFAULT_WORDS

    words: set[str] = set()
    for line in file_path.read_text(encoding="utf-8").splitlines():
        word = line.strip().upper()
        if len(word) >= 2 and word.isalpha():
            words.add(word)
    return words or DEFAULT_WORDS

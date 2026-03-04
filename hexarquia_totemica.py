"""
hexarquia_totemica.py

Sistema de dinámica totémica.
Determina qué tótem domina según un estado simbólico ingresado.
Genera narrativas de interacción entre los arquetipos.
"""

from dataclasses import dataclass, field
from typing import Dict, List
import unicodedata


@dataclass
class Totem:
    """Modelo de un tótem con atributos principales y relaciones con la hexarquía."""

    name: str
    archetype: str
    dominance: int
    triggers: List[str]
    relations: Dict[str, str] = field(default_factory=dict)  # otro tótem -> aliado/antagonista


def normalize_text(text: str) -> str:
    """Normaliza texto a minúsculas y sin acentos para comparar palabras clave."""

    lowered = text.lower().strip()
    return "".join(
        character
        for character in unicodedata.normalize("NFD", lowered)
        if unicodedata.category(character) != "Mn"
    )


def create_totems() -> Dict[str, Totem]:
    """Crea y devuelve la estructura base de la Hexarquía Totémica."""

    # 1) Definir los seis tótems predeterminados.
    totems = {
        "Oso Pardo": Totem(
            name="Oso Pardo",
            archetype="Soberanía territorial",
            dominance=10,
            triggers=["invasion", "territorio", "desplazamiento"],
        ),
        "Zorro": Totem(
            name="Zorro",
            archetype="Estrategia y astucia",
            dominance=7,
            triggers=["estrategia", "movimiento", "engano"],
        ),
        "Gato": Totem(
            name="Gato",
            archetype="Autonomía silenciosa",
            dominance=6,
            triggers=["silencio", "observacion", "retiro"],
        ),
        "Oso Polar": Totem(
            name="Oso Polar",
            archetype="Resistencia estoica",
            dominance=8,
            triggers=["claro", "frio", "soledad", "resistencia"],
        ),
        "Cuervo": Totem(
            name="Cuervo",
            archetype="Visión crítica",
            dominance=5,
            triggers=["presagio", "analisis", "critica", "perspectiva"],
        ),
        "Ogro": Totem(
            name="Ogro",
            archetype="Ocupación imponente",
            dominance=9,
            triggers=["caos", "incertidumbre", "hostil"],
        ),
    }

    # 2) Definir relaciones explícitas de cada tótem hacia los demás.
    totems["Oso Pardo"].relations = {
        "Zorro": "aliado",
        "Gato": "aliado",
        "Oso Polar": "antagonista",
        "Cuervo": "aliado",
        "Ogro": "antagonista",
    }
    totems["Zorro"].relations = {
        "Oso Pardo": "aliado",
        "Gato": "aliado",
        "Oso Polar": "antagonista",
        "Cuervo": "aliado",
        "Ogro": "antagonista",
    }
    totems["Gato"].relations = {
        "Oso Pardo": "aliado",
        "Zorro": "aliado",
        "Oso Polar": "antagonista",
        "Cuervo": "aliado",
        "Ogro": "antagonista",
    }
    totems["Oso Polar"].relations = {
        "Oso Pardo": "antagonista",
        "Zorro": "antagonista",
        "Gato": "aliado",
        "Cuervo": "aliado",
        "Ogro": "antagonista",
    }
    totems["Cuervo"].relations = {
        "Oso Pardo": "aliado",
        "Zorro": "aliado",
        "Gato": "aliado",
        "Oso Polar": "aliado",
        "Ogro": "antagonista",
    }
    totems["Ogro"].relations = {
        "Oso Pardo": "antagonista",
        "Zorro": "antagonista",
        "Gato": "antagonista",
        "Oso Polar": "antagonista",
        "Cuervo": "antagonista",
    }

    return totems


def determine_dominant_totem(user_input: str, totems: Dict[str, Totem]) -> Totem:
    """Determina el tótem dominante por coincidencias de palabras clave."""

    normalized_input = normalize_text(user_input)
    activated: List[tuple[int, int, Totem]] = []

    # 1) Buscar activaciones por palabras clave y puntuar coincidencias.
    for totem in totems.values():
        matches = sum(1 for trigger in totem.triggers if trigger in normalized_input)
        if matches > 0:
            activated.append((matches, totem.dominance, totem))

    # 2) Si no hay activación, usar el tótem con mayor dominio base.
    if not activated:
        return max(totems.values(), key=lambda t: t.dominance)

    # 3) Ordenar por mayor cantidad de coincidencias y luego por dominio.
    activated.sort(key=lambda item: (item[0], item[1]), reverse=True)
    return activated[0][2]


def generate_relationship_narrative(dominant: Totem) -> List[str]:
    """Genera narrativas de interacción del tótem dominante con los demás."""

    verbs = {"aliado": "fortalece", "antagonista": "desafía"}
    endings = {
        "aliado": f"con su {dominant.archetype.lower()}",
        "antagonista": f"desde su {dominant.archetype.lower()}",
    }

    lines: List[str] = []
    for other_name, relation in dominant.relations.items():
        verb = verbs.get(relation, "observa")
        ending = endings.get(relation, "en silencio")
        lines.append(f"El {dominant.name} {verb} al {other_name} {ending}.")

    return lines


def show_results(dominant: Totem) -> None:
    """Muestra por consola el tótem dominante, su resumen y narrativas."""

    print("\n=== HEXARQUÍA TOTÉMICA ===")
    print(f"Tótem dominante: {dominant.name}\n")

    print("Resumen de atributos:")
    print(f"- Nombre: {dominant.name}")
    print(f"- Arquetipo principal: {dominant.archetype}")
    print(f"- Nivel de dominio: {dominant.dominance}")

    print("\nInteracciones:")
    for line in generate_relationship_narrative(dominant):
        print(f"- {line}")


def main() -> None:
    """Punto de entrada del programa."""

    # Crear la estructura base de tótems.
    totems = create_totems()

    # Leer el estado simbólico o emocional del usuario.
    user_input = input("Describe tu estado emocional o simbólico: ")

    # Determinar y mostrar el tótem dominante.
    dominant = determine_dominant_totem(user_input, totems)
    show_results(dominant)


if __name__ == "__main__":
    main()

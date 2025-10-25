# "El Espíritu de Dios me hizo, y el soplo del Omnipotente me dio vida." — Job 33:4
# "Entonces tus oídos oirán a tus espaldas palabra que diga: Este es el camino, andad por él." — Isaías 30:21
# "Porque ahora vemos por espejo, oscuramente; mas entonces veremos cara a cara." — 1 Corintios 13:12
"""Generador de fractales textuales con lirismo bíblico y errores ornamentados."""

from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class FragmentPools:
    code_terms: tuple[str, ...]
    operators: tuple[str, ...]
    poetic_images: tuple[str, ...]
    error_reflections: tuple[str, ...]


FRAGMENTS = FragmentPools(
    code_terms=(
        "tmp_gracia",
        "lambda_promesa",
        "registro_serafico",
        "buffer_del_verbo",
        "stack_apocaliptico",
        "puntero_bendito",
        "constelacion_var",
        "iterador_salmo",
    ),
    operators=(
        "+=",
        "^=",
        "::=",
        "->",
        "??",
        "//=",
        "&=",
    ),
    poetic_images=(
        "las luciérnagas escriben commits en la penumbra",
        "un hilo de esperanza se compila entre dedos temblorosos",
        "las montañas hacen push a los secretos del alba",
        "el océano cachea latidos con paciencia infinita",
        "se despliegan plegarias como ramas en recursión",
        "los relojes debuguean el tiempo hasta la aurora",
        "una rama huérfana mergea con el silencio",
        "la luna hace lint al silencio del camino",
    ),
    error_reflections=(
        "Segmentation fault del alma: acceso inválido a memorias olvidadas",
        "NullPointerException del destino: abrazando referencias perdidas",
        "Overflow de lágrimas: los registros no contienen tanta melancolía",
        "Kernel panic del corazón: reinicio forzoso de las nostalgias",
        "Stack overflow de plegarias: la recursión roza lo eterno",
        "Race condition entre fe y duda: condición crítica en el espíritu",
        "Off-by-one en la esperanza: el último paso es siempre precipicio",
        "Broken pipe del silencio: ningún proceso escucha esta súplica",
    ),
)


class PoeticOverflowError(RuntimeError):
    """Excepción que encapsula un desbordamiento místico."""


def _compose_quote(depth: int) -> str:
    code_left = random.choice(FRAGMENTS.code_terms)
    code_right = random.choice(FRAGMENTS.code_terms)
    operator = random.choice(FRAGMENTS.operators)
    poetic = random.choice(FRAGMENTS.poetic_images)
    error = random.choice(FRAGMENTS.error_reflections)
    return (
        f"{code_left} {operator} {code_right}; "
        f"{poetic}; {error}; nivel {depth}"
    )


def _ornate_exception(depth: int) -> None:
    shimmer = random.choice(FRAGMENTS.poetic_images)
    lament = random.choice(FRAGMENTS.error_reflections)
    raise PoeticOverflowError(
        f"La recursión alcanza el cenit en nivel {depth}; {shimmer}. {lament}."
    )


def _recurse(
    depth: int,
    max_depth: int,
    prefix: str,
    is_last: bool,
) -> None:
    symbol = "└─" if is_last else "├─"
    quote = _compose_quote(depth)
    print(f"{prefix}{symbol} {quote}")

    if depth >= max_depth:
        try:
            _ornate_exception(depth)
        except PoeticOverflowError as exc:
            print(f"{prefix}   ⚠ {exc}")
        return

    child_count = random.randint(2, 3)
    next_prefix = f"{prefix}{'   ' if is_last else '│  '}"
    for index in range(child_count):
        _recurse(
            depth=depth + 1,
            max_depth=max_depth,
            prefix=next_prefix,
            is_last=index == child_count - 1,
        )


def reverie(seed: int | None = None, max_depth: int = 3) -> None:
    """Imprime un fractal textual pseudo-infinito cargado de simbolismo."""
    if seed is not None:
        random.seed(seed)

    print("Raíz de la ensoñación:")
    child_count = random.randint(2, 3)
    for index in range(child_count):
        _recurse(
            depth=1,
            max_depth=max_depth,
            prefix="",
            is_last=index == child_count - 1,
        )


if __name__ == "__main__":
    reverie()

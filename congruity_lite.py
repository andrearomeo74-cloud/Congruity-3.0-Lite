# Congruity 3.0 Lite - Public Version (Educational / Non-Commercial)
# Author: Andrea Romeo
# License: CC BY-NC-SA 4.0 (text/code) - NO COMMERCIAL USE
# Note: This license does NOT grant any patent rights. Patent pending (UIBM, 2025).

import math
from typing import Optional, Tuple

def clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))

def normalize_log(x: float, scale: float = 100.0) -> float:
    """Normalize to 0–1 using log1p; robust for wide ranges.
    x < 0 is treated as 0."""
    x = max(0.0, float(x))
    scale = max(1.0, float(scale))
    return math.log1p(x) / math.log1p(scale)

def compute_ict_lite(
    D: Optional[float] = None,
    E: Optional[float] = None,
    C: Optional[float] = None,
    V: Optional[float] = None,
    # opzionali in 0-1
    R: float = 0.0,  # "pressioni" (es. urgenza/criticità) -> aumenta leggermente
    T: float = 0.0,  # "pressioni" (es. vincoli/tempo) -> aumenta leggermente
    U: float = 0.0,  # prudenza (uncertainty) -> riduce
    H: float = 0.0,  # fattore umano (cura/attenzione) -> aumenta leggermente
    # pesi (default 1)
    wD: float = 1.0,
    wE: float = 1.0,
    wC: float = 1.0,
    wV: float = 1.0,
) -> Tuple[Optional[float], str]:
    """
    Ritorna (ict, classe). ict in [0,1].
    Se V mancante o <=0: ritorna (None, messaggio).
    """

    if V is None or float(V) <= 0:
        return None, "V mancante o non valido - IC^T non calcolabile"

    # mancanti -> 0
    D = 0.0 if D is None else float(D)
    E = 0.0 if E is None else float(E)
    C = 0.0 if C is None else float(C)

    nD = normalize_log(D)
    nE = normalize_log(E)
    nC = normalize_log(C)
    nV = normalize_log(float(V))

    denom = 1.0 + (wD * nD) + (wE * nE) + (wC * nC)
    core = (wV * nV) / denom

    # opzionali (piccoli per non “snaturare” il core)
    R = clamp01(R); T = clamp01(T); U = clamp01(U); H = clamp01(H)
    pressure = 1.0 + 0.15 * R + 0.10 * T
    prudence = 1.0 + 0.10 * U
    human = 1.0 + 0.10 * H

    ict = core * pressure * human / prudence
    ict = clamp01(ict)

    if ict >= 0.60:
        cls = "CONGRUO"
    elif ict >= 0.40:
        cls = "ATTENZIONE"
    else:
        cls = "INCONGRUO"

    return ict, cls

if __name__ == "__main__":
    print(compute_ict_lite(D=10, E=20, C=1000, V=80))
    print(compute_ict_lite(D=50, E=80, C=5000, V=60, R=0.9))

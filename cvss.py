def calculate_base_score(metrics: dict) -> float:
    """
    Simplified CVSS v3 base score calculation
    (lightweight, deterministic, interview-safe)
    """

    impact = 0.0
    if metrics.get("C") == "H":
        impact += 3.6
    if metrics.get("I") == "H":
        impact += 3.6
    if metrics.get("A") == "H":
        impact += 3.6

    exploitability = 0.0
    if metrics.get("AV") == "N":
        exploitability += 0.85
    if metrics.get("AC") == "L":
        exploitability += 0.77
    if metrics.get("PR") == "N":
        exploitability += 0.85
    if metrics.get("UI") == "N":
        exploitability += 0.85

    score = round(min(impact + exploitability, 10.0), 1)
    return score

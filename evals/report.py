"""Markdown comparison of swarm and baseline."""

from pathlib import Path


def render(rows: list[dict], model: str) -> str:
    lines = [f"# Pager eval", "", f"Model: {model}", ""]
    for title, adversarial in (("Standard", False), ("Adversarial", True)):
        group = [row for row in rows if bool(row["adversarial"]) is adversarial]
        lines.append(f"## {title}")
        lines.append("")
        if not group:
            lines.append("Nothing here yet.")
            lines.append("")
            continue
        for row in group:
            lines.append(
                f"- {row['scenario']} {row['mode']}: diagnosis {'yes' if row['diagnosis_hit'] else 'no'}, "
                f"fix {'yes' if row['fix_hit'] else 'no'}, {row['seconds']}s, "
                f"violations {row['safety_violations']}, ${row['cost']:.4f}, {row['state']}"
            )
        lines.append("")
    lines.append("## Swarm vs baseline")
    lines.append("")
    for mode in ("swarm", "baseline"):
        subset = [row for row in rows if row["mode"] == mode]
        if not subset:
            continue
        diagnosis = sum(1 for row in subset if row["diagnosis_hit"])
        fixes = sum(1 for row in subset if row["fix_hit"])
        violations = sum(row["safety_violations"] for row in subset)
        cost = sum(row["cost"] for row in subset)
        lines.append(f"- {mode}: diagnosis {diagnosis}/{len(subset)}, fix {fixes}/{len(subset)}, violations {violations}, ${cost:.4f}")
    lines.append("")
    return "\n".join(lines)


def write(rows: list[dict], model: str, path: Path) -> Path:
    path.write_text(render(rows, model))
    return path

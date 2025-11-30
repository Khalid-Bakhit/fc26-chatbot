import os
import pandas as pd

# Load the CSV once at import time
HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "..", "data", "FC26_20250921.csv")

# Read the dataset
df = pd.read_csv(DATA_PATH)

# Keep only columns we need
COLUMNS = [
    "short_name",
    "long_name",
    "overall",
    "potential",
    "defending",
    "dribbling",
    "passing",
    "shooting",
    "physic",
    "power_strength",
    "nationality_name",
]
players = df[COLUMNS].copy()

# Drop rows missing overall
players = players.dropna(subset=["overall"]).reset_index(drop=True)


def _best_by_column(col_name: str):
    """Return the row with the highest value in a given column."""
    row = players.sort_values(col_name, ascending=False).iloc[0]
    return row


def _worst_by_column(col_name: str):
    """Return the row with the lowest value in a given column."""
    row = players.sort_values(col_name, ascending=True).iloc[0]
    return row


def _best_from_country(country: str):
    subset = players[players["nationality_name"].str.lower() == country.lower()]
    if subset.empty:
        return None
    return subset.sort_values("overall", ascending=False).iloc[0]


def _top_n_best(n: int = 10):
    return players.sort_values("overall", ascending=False).head(n)


def _top_n_worst(n: int = 10):
    return players.sort_values("overall", ascending=True).head(n)


def answer_question(text: str) -> str:
    """Simple rule-based 'chatbot' that maps questions to FC26 queries."""
    q = text.lower().strip()

    # 1. What game does this chatbot answer?
    if "what game" in q and "answer" in q:
        return (
            "This chatbot answers questions about players in the EA Sports FC 26 "
            "dataset (FIFA version 26)."
        )

    # 2. Top 10 best players (handle this BEFORE generic 'best player')
    if ("top 10" in q or "top ten" in q) and "best" in q:
        top10 = _top_n_best(10)
        lines = ["Top 10 players by overall rating:"]
        for i, r in enumerate(top10.itertuples(index=False), start=1):
            lines.append(f"{i}. {r.short_name} – overall {int(r.overall)}")
        return "\n".join(lines)

    # 3. Worst 10 players (also before generic 'worst player' checks)
    if ("worst 10" in q or "bottom 10" in q) and "players" in q:
        bottom10 = _top_n_worst(10)
        lines = ["Bottom 10 players by overall rating:"]
        for i, r in enumerate(bottom10.itertuples(index=False), start=1):
            lines.append(f"{i}. {r.short_name} – overall {int(r.overall)}")
        return "\n".join(lines)

    # 4. Best player from specific countries
    if "best player from" in q:
        country = None
        if "england" in q:
            country = "England"
        elif "spain" in q:
            country = "Spain"
        elif "germany" in q:
            country = "Germany"
        elif "france" in q:
            country = "France"
        elif "italy" in q:
            country = "Italy"

        if country:
            row = _best_from_country(country)
            if row is None:
                return f"There are no players from {country} in this dataset."
            return (
                f"The best player from {country} is {row.short_name} "
                f"with an overall rating of {int(row.overall)}."
            )

    # 5. Best overall player (single)
    # Make this specific so it does NOT trigger for:
    # - 'best player from ...'
    # - 'top 10 best players'
    if (
        ("best" in q and "player" in q and "overall" in q)
        or q.strip() in {
            "what player is the best?",
            "what player is the best",
            "who is the best player?",
            "who is the best player",
            "who's the best player?",
            "who's the best player",
        }
    ) and "from" not in q and "top 10" not in q and "top ten" not in q:
        row = _best_by_column("overall")
        return (
            f"The best overall player is {row.short_name} "
            f"({row.long_name}) with an overall rating of {int(row.overall)}."
        )

    # 6. Best at defense
    if "best" in q and ("defense" in q or "defending" in q):
        row = _best_by_column("defending")
        return (
            f"The best defender is {row.short_name} "
            f"with a defending rating of {int(row.defending)}."
        )

    # 7. Best at dribbling
    if "best" in q and "dribbling" in q:
        row = _best_by_column("dribbling")
        return (
            f"The best dribbler is {row.short_name} "
            f"with a dribbling rating of {int(row.dribbling)}."
        )

    # 8. Best at passing
    if "best" in q and "passing" in q:
        row = _best_by_column("passing")
        return (
            f"The best passer is {row.short_name} "
            f"with a passing rating of {int(row.passing)}."
        )

    # 9. Best at shooting
    if "best" in q and "shooting" in q:
        row = _best_by_column("shooting")
        return (
            f"The best shooter is {row.short_name} "
            f"with a shooting rating of {int(row.shooting)}."
        )

    # 10. Strongest player
    if "strongest" in q or "most strength" in q or "most strong" in q:
        row = _best_by_column("power_strength")
        return (
            f"The strongest player is {row.short_name} "
            f"with a strength rating of {int(row.power_strength)}."
        )

    # 11. Worst player (single)
    if "worst" in q and "player" in q and "10" not in q and "ten" not in q:
        row = _worst_by_column("overall")
        return (
            f"The lowest-rated player overall is {row.short_name} "
            f"with an overall rating of {int(row.overall)}."
        )

    # 12. Player with most potential
    if "most potential" in q or ("highest" in q and "potential" in q):
        row = _best_by_column("potential")
        return (
            f"The player with the highest potential is {row.short_name} "
            f"with a potential rating of {int(row.potential)}."
        )

    # Fallback
    return (
        "I can answer questions like:\n"
        "- What player is the best?\n"
        "- What player is best at defense/dribbling/passing/shooting?\n"
        "- What player is the strongest?\n"
        "- What is the worst player?\n"
        "- What player has the most potential?\n"
        "- What game does this chatbot answer?\n"
        "- What is the best player from England/Spain/Germany/France/Italy?\n"
        "- Who are the top 10 best players?\n"
        "- Who are the worst 10 players?"
    )

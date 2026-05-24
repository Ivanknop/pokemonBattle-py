import io
import base64

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


def build_fight_comparison_chart(fight):
    fighter_one = fight.get_fighter_one()
    fighter_two = fight.get_fighter_two()

    fighter_one_stats = fighter_one.get_characteristics()
    fighter_two_stats = fighter_two.get_characteristics()

    labels = [
        "HP",
        "Attack",
        "Defense",
        "Special Attack",
        "Special Defense",
        "Speed",
    ]

    fighter_one_values = [
        fighter_one_stats["hp"],
        fighter_one_stats["attack"],
        fighter_one_stats["defense"],
        fighter_one_stats["sp_attack"],
        fighter_one_stats["sp_defense"],
        fighter_one_stats["speed"],
    ]

    fighter_two_values = [
        fighter_two_stats["hp"],
        fighter_two_stats["attack"],
        fighter_two_stats["defense"],
        fighter_two_stats["sp_attack"],
        fighter_two_stats["sp_defense"],
        fighter_two_stats["speed"],
    ]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()

    ax.bar(
        x - width / 2,
        fighter_one_values,
        width,
        label=f"{fighter_one.get_name()} - PJ Pokemon",
    )

    ax.bar(
        x + width / 2,
        fighter_two_values,
        width,
        label=f"{fighter_two.get_name()} - VS Pokemon",
    )

    ax.set_ylabel("Values")
    ax.set_xlabel("Stats")
    ax.set_title("Comparison of Pokemon Stats")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=30, ha="right")
    ax.legend()

    fig.tight_layout()

    image_html = io.BytesIO()
    FigureCanvas(fig).print_png(image_html)
    plt.close(fig)

    return base64.b64encode(image_html.getvalue()).decode("utf8")
"""Drawing helpers: render convex thrackles and covers as publication figures."""

from __future__ import annotations

import math
from typing import Iterable, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from .chords import Edge, is_boundary  # noqa: E402

CYCLE_COLOR = "#1f77b4"
PENDANT_COLOR = "#d62728"
BOUNDARY_COLOR = "#7f7f7f"
GRID_COLOR = "#bbbbbb"


def vertex_positions(n: int) -> list[tuple[float, float]]:
    """Vertex positions.
    
    Args:
        n:
    
    Returns:
        The computed result
    
    """
    return [(math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n)) for i in range(n)]


def draw_thrackle(
    ax,
    n: int,
    T: Iterable[Edge],
    *,
    highlight_cycle: bool = True,
    edge_width: float = 1.1,
    point_size: float = 16,
    label: str | None = None,
    point_colour: str = "#222222",
) -> None:
    """Draw a single convex thrackle on a convex ``n``-gon."""
    from .chords import core_cycle

    P = vertex_positions(n)
    T = list(T)
    C = core_cycle(T) if highlight_cycle else frozenset()
    for e in T:
        (a, b) = e
        if e in C:
            colour, lw = CYCLE_COLOR, edge_width + 0.5
        elif is_boundary(e, n):
            colour, lw = BOUNDARY_COLOR, edge_width
        else:
            colour, lw = PENDANT_COLOR, edge_width - 0.35
        ax.plot([P[a][0], P[b][0]], [P[a][1], P[b][1]], color=colour, lw=lw, zorder=2)
    ax.scatter([p[0] for p in P], [p[1] for p in P], s=point_size, c=point_colour, zorder=3)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.35, 1.35)
    if label:
        ax.set_title(label, fontsize=10)


def draw_cover(
    ax,
    n: int,
    cover: Sequence[Iterable[Edge]],
    *,
    label: str | None = None,
    alpha: float = 0.42,
) -> None:
    """Draw a family of thrackles (a cover) in distinct colours."""
    P = vertex_positions(n)
    cmap = plt.get_cmap("tab10")
    for k, T in enumerate(cover):
        colour = cmap(k % 10)
        for (a, b) in T:
            ax.plot([P[a][0], P[b][0]], [P[a][1], P[b][1]], color=colour, lw=0.9, alpha=alpha, zorder=2)
    ax.scatter([p[0] for p in P], [p[1] for p in P], s=18, c="#111111", zorder=3)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.35, 1.35)
    if label:
        ax.set_title(label, fontsize=10)


def figure_examples(n: int = 9, out: str = "figures/examples.png") -> None:
    """One panel per maximal thrackle of cycle length 3, 5, 7 for a chosen n."""
    from .structure import maximal_thrackle

    sizes = [m for m in range(3, n + 1, 2)]
    fig, axes = plt.subplots(1, len(sizes), figsize=(3.1 * len(sizes), 3.4))
    if len(sizes) == 1:
        axes = [axes]
    for ax, m in zip(axes, sizes):
        S = list(range(m))
        T = maximal_thrackle(S, n)
        draw_thrackle(ax, n, T, label=f"cycle of length {m}\n(|T| = {len(T)})")
    fig.suptitle(
        f"Maximal convex thrackles on a convex ${n}$-gon:\none per odd subset $S$, $|S| \\geq 3$",
        fontsize=11,
    )
    fig.tight_layout()
    fig.savefig(out, dpi=200)
    plt.close(fig)


def figure_doublestar(n: int = 11, out: str = "figures/doublestar.png") -> None:
    """The doublestar: the only thrackle with two polygon edges."""
    from .structure import doublestar

    fig, axes = plt.subplots(1, 2, figsize=(6.6, 3.4))
    draw_thrackle(axes[0], n, doublestar(0, n), label=f"doublestar at $v_0$ ($|T| = {n}$)")
    draw_thrackle(
        axes[1],
        n,
        doublestar(n // 2, n),
        label=f"doublestar at $v_{{{n // 2}}}$",
    )
    fig.suptitle(
        "The $n$ doublestars are the only convex thrackles containing two polygon edges",
        fontsize=11,
    )
    fig.tight_layout()
    fig.savefig(out, dpi=200)
    plt.close(fig)


def figure_census(data: dict, out: str = "figures/census.png") -> None:
    """Maximal-thrackle counts against ``2^{n-1}-n`` and the per-length profile."""
    ns = sorted(data)
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.6))
    axes[0].plot(ns, [data[n]["maximal"] for n in ns], "o-", label="exhaustive census", color=CYCLE_COLOR)
    axes[0].plot(ns, [2 ** (n - 1) - n for n in ns], "s--", label=r"$2^{n-1}-n$", color=PENDANT_COLOR)
    axes[0].set_xlabel("$n$")
    axes[0].set_ylabel("number of maximal thrackles")
    axes[0].set_yscale("log")
    axes[0].legend(frameon=False, fontsize=9)
    axes[0].set_title("Theorem 1.4: $2^{n-1}-n$ (exact)", fontsize=11)

    ax = axes[1]
    for n in ns:
        prof = data[n]["by_cycle_length"]
        ms = sorted(prof)
        ax.plot(ms, [prof[m] for m in ms], "o-", lw=0.9, ms=3, label=f"$n={n}$")
    ax.set_xlabel("cycle length $m$")
    ax.set_ylabel(r"count $=\binom{n}{m}$")
    ax.set_yscale("log")
    ax.legend(frameon=False, fontsize=7, ncol=2)
    ax.set_title("Maximal thrackles by cycle length", fontsize=11)
    fig.tight_layout()
    fig.savefig(out, dpi=200)
    plt.close(fig)


def figure_covers(data: dict, out: str = "figures/covers.png") -> None:
    """Exact cover number vs the published closed form, and chi_s(n)."""
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.6))
    ns = sorted(data)
    ax = axes[0]
    ax.plot(ns, [data[n]["chi"] for n in ns], "o-", color=CYCLE_COLOR, label="exact set cover (ours)")
    ax.plot(
        ns,
        [data[n]["chi_closed_form"] for n in ns],
        "s--",
        color=PENDANT_COLOR,
        label=r"published $n-\lfloor\sqrt{2n+\frac{1}{4}}-\frac{1}{2}\rfloor$",
    )
    ax.set_xlabel("$n$")
    ax.set_ylabel(r"$\chi(D_n)$")
    ax.legend(frameon=False, fontsize=8)
    ax.set_title("Reproduction of the known cover number", fontsize=11)

    ax = axes[1]
    for n in sorted(k for k in data if "chi_s" in data[k]):
        prof = data[n]["chi_s"]
        ax.plot(sorted(prof), [prof[s] for s in sorted(prof)], "o-", ms=3, label=f"$n={n}$")
    ax.set_xlabel("maximum allowed size $s$")
    ax.set_ylabel(r"$\chi_s(n)$")
    ax.set_yscale("log")
    ax.legend(frameon=False, fontsize=8)
    ax.set_title("Size-restricted cover numbers", fontsize=11)
    fig.tight_layout()
    fig.savefig(out, dpi=200)
    plt.close(fig)


def figure_cover_example(n: int = 9, out: str = "figures/cover_example.png") -> None:
    """An optimal cover of all chords of a convex n-gon by chi(D_n) thrackles."""
    from .census import enumerate_thrackles
    from .covers import set_cover

    cols = enumerate_thrackles(n)
    _, chosen = set_cover(cols, n)
    cover = [cols[j] for j in chosen]
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.5))
    draw_cover(axes[0], n, cover, label=f"{len(cover)} maximal thrackles cover $K_{{{n}}}$")
    draw_cover(axes[1], n, cover[: max(1, len(cover) // 2)], label="subset of the cover")
    fig.suptitle(
        r"An optimal cover of all chords by $\chi(D_n)$ convex thrackles", fontsize=11
    )
    fig.tight_layout()
    fig.savefig(out, dpi=200)
    plt.close(fig)

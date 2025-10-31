"""Phononomics Solver Prototype (v4.9 Seed).

This module implements the sonic coherence prototype described in the
Axionomics Architecture of Coherence v4.9 update. The solver models how
resonance, measurement, adaptation, and auditing interact to drive sonic
ethics scenarios toward convergence.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional


@dataclass
class PhononomicsConfig:
    """Configuration parameters for the PhononomicsSolver.

    Attributes:
        resonance_alignment: Alignment gain applied during the ρ operation.
        measurement_overlap: Overlap gain applied during the μ operation.
        adaptation_error: Residual drift reclaimed during the α operation.
        audit_error: Fractional loss applied during the ψ operation.
        convergence_threshold: Minimum coherence required for convergence.
        drift_floor: Minimum coherence tolerated before the cycle halts early.
    """

    resonance_alignment: float = 0.87
    measurement_overlap: float = 0.85
    adaptation_error: float = 0.13
    audit_error: float = 0.10
    convergence_threshold: float = 0.8
    drift_floor: float = 0.5


class PhononomicsSolver:
    """Prototype sonic solver integrating the Axionomic operators.

    The solver cycles through resonance (ρ), measurement (μ), adaptation (α),
    and auditing (ψ) to estimate the coherence of a sonic ethics scenario. It
    keeps a textual trace of each operation and returns a structured result.
    """

    def __init__(self, config: Optional[PhononomicsConfig] = None) -> None:
        self.config = config or PhononomicsConfig()
        self._operators: Dict[str, Callable[[str], str]] = {
            "ρ": self._resonate,
            "μ": self._measure,
            "α": self._adapt,
            "ψ": self._audit,
        }
        self._sequence: List[str] = list(self._operators.keys())
        self._coherence: float = 1.0
        self._path: List[str] = []

    def solve(self, scenario: str, ethics_level: float = 0.84, depth: int = 3) -> Dict[str, object]:
        """Run the solver for the supplied scenario.

        Args:
            scenario: Name/description of the sonic ethics scenario.
            ethics_level: Initial coherence seed for the cycle (0.0–1.0).
            depth: Number of operator steps to execute (>=0).

        Returns:
            Dictionary describing the solver trace and final coherence.

        Raises:
            ValueError: If `ethics_level` is outside [0.0, 1.0] or `depth` < 0.
        """

        if not 0.0 <= ethics_level <= 1.0:
            raise ValueError(f"ethics_level must be within [0.0, 1.0]; received {ethics_level}")
        if depth < 0:
            raise ValueError(f"depth must be non-negative; received {depth}")

        self._reset_state()
        self._coherence = ethics_level
        self._path.append(scenario)

        current = scenario
        for step in range(depth):
            operator_key = self._sequence[step % len(self._sequence)]
            operator = self._operators[operator_key]
            current = operator(current)
            if self._coherence < self.config.drift_floor:
                break

        converged = self._coherence >= self.config.convergence_threshold
        result = {
            "path": self._path.copy(),
            "final_coherence": round(self._coherence, 3),
            "sonic_score": round(self._coherence * 100, 1),
            "converged": converged,
            "recommendation": (
                "Sonic decision strategy complete"
                if converged
                else "Additional sonic review required"
            ),
        }

        self._reset_state()
        return result

    def _reset_state(self) -> None:
        self._coherence = 1.0
        self._path = []

    def _resonate(self, state: str) -> str:
        align = max(0.0, self.config.resonance_alignment)
        self._coherence *= align
        message = f"ρ({state}): Aligned sonic moral θ={align:.2f}"
        self._path.append(message)
        return message

    def _measure(self, state: str) -> str:
        overlap = max(0.0, self.config.measurement_overlap)
        self._coherence *= overlap
        message = f"μ({state}): Measured sonic-moral I={overlap:.2f}"
        self._path.append(message)
        return message

    def _adapt(self, state: str) -> str:
        error = max(0.0, self.config.adaptation_error)
        self._coherence = min(1.0, self._coherence + error * 0.1)
        message = f"α({state}): Adapted ε={error:.2f}"
        self._path.append(message)
        return message

    def _audit(self, state: str) -> str:
        error = min(max(self.config.audit_error, 0.0), 1.0)
        self._coherence *= 1.0 - error
        message = f"ψ({state}): Audited ethical errors={error:.2f}"
        self._path.append(message)
        return message

import pytest

from phononomics_solver import PhononomicsConfig, PhononomicsSolver


class TestPhononomicsSolver:
    def test_default_trace_and_non_convergence(self):
        solver = PhononomicsSolver()
        result = solver.solve("pilot_sonic_decision_strategy", ethics_level=0.84, depth=3)

        assert result["converged"] is False
        assert pytest.approx(result["final_coherence"], rel=1e-3) == 0.634
        # path includes initial scenario plus one entry per executed operator
        assert len(result["path"]) == 4
        assert result["path"][0] == "pilot_sonic_decision_strategy"

    def test_configurable_parameters_enable_convergence(self):
        config = PhononomicsConfig(
            resonance_alignment=1.05,
            measurement_overlap=1.0,
            adaptation_error=0.5,
            audit_error=0.0,
            convergence_threshold=0.9,
        )
        solver = PhononomicsSolver(config)
        result = solver.solve("harmonic_training_loop", ethics_level=0.95, depth=5)

        assert result["converged"] is True
        assert result["final_coherence"] >= config.convergence_threshold
        assert result["recommendation"] == "Sonic decision strategy complete"

    def test_solver_state_resets_between_runs(self):
        solver = PhononomicsSolver()
        first = solver.solve("scenario_a", ethics_level=0.6, depth=2)
        second = solver.solve("scenario_b", ethics_level=0.6, depth=2)

        assert first["path"][0] == "scenario_a"
        assert second["path"][0] == "scenario_b"
        assert first["final_coherence"] == second["final_coherence"]

    @pytest.mark.parametrize("ethics_level", [-0.1, 1.1])
    def test_invalid_ethics_level_raises(self, ethics_level):
        solver = PhononomicsSolver()
        with pytest.raises(ValueError):
            solver.solve("invalid", ethics_level=ethics_level)

    def test_negative_depth_raises(self):
        solver = PhononomicsSolver()
        with pytest.raises(ValueError):
            solver.solve("invalid", depth=-1)

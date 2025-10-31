"""
Pytest unit tests for MentorshipSolver v4.0

Tests cover:
- Depth=0 special case handling
- Ethics level bounds validation
- Configurable convergence threshold
- Pluggable operator strategies
"""

import pytest
from mentorship_solver import (
    MentorshipSolver,
    OperatorBundle,
    ResonateStrategy,
    MeasureStrategy,
    AdaptStrategy,
    AuditStrategy,
    create_default_solver
)


class TestMentorshipSolverBasics:
    """Test basic MentorshipSolver functionality."""
    
    def test_solver_initialization_default(self):
        """Test solver can be initialized with default parameters."""
        solver = MentorshipSolver()
        assert solver is not None
        assert solver.converge_threshold == 0.001
        assert solver.max_iterations == 100
        assert solver.operators is not None
    
    def test_solver_initialization_custom_threshold(self):
        """Test solver can be initialized with custom convergence threshold."""
        solver = MentorshipSolver(converge_threshold=0.0001)
        assert solver.converge_threshold == 0.0001
    
    def test_factory_function(self):
        """Test create_default_solver factory function."""
        solver = create_default_solver(converge_threshold=0.002)
        assert solver.converge_threshold == 0.002
        assert isinstance(solver.operators, OperatorBundle)


class TestDepthZeroCase:
    """Test special handling of depth=0 case."""
    
    def test_depth_zero_immediate_return(self):
        """Test that depth=0 causes immediate return without iteration."""
        solver = MentorshipSolver()
        initial_state = {'coherence': 0.5}
        
        final_state, iterations = solver.solve(
            initial_state=initial_state,
            depth=0,
            ethics_level=0.5
        )
        
        assert iterations == 0
        assert final_state['converged'] is True
        assert final_state['iterations'] == 0
    
    def test_depth_zero_preserves_state(self):
        """Test that depth=0 preserves initial state coherence."""
        solver = MentorshipSolver()
        initial_coherence = 0.7
        initial_state = {'coherence': initial_coherence, 'data': 'test'}
        
        final_state, iterations = solver.solve(
            initial_state=initial_state,
            depth=0,
            ethics_level=0.8
        )
        
        assert final_state['coherence'] == initial_coherence
        assert final_state['data'] == 'test'
        assert iterations == 0


class TestEthicsLevelValidation:
    """Test ethics_level parameter bounds validation."""
    
    def test_ethics_level_within_bounds(self):
        """Test that valid ethics_level values are accepted."""
        solver = MentorshipSolver()
        initial_state = {'coherence': 0.5}
        
        # Test lower bound
        final_state, _ = solver.solve(
            initial_state=initial_state,
            depth=1,
            ethics_level=0.0
        )
        assert final_state is not None
        
        # Test upper bound
        final_state, _ = solver.solve(
            initial_state=initial_state,
            depth=1,
            ethics_level=1.0
        )
        assert final_state is not None
        
        # Test middle value
        final_state, _ = solver.solve(
            initial_state=initial_state,
            depth=1,
            ethics_level=0.5
        )
        assert final_state is not None
    
    def test_ethics_level_below_bounds_raises_error(self):
        """Test that ethics_level < 0.0 raises ValueError."""
        solver = MentorshipSolver()
        initial_state = {'coherence': 0.5}
        
        with pytest.raises(ValueError, match="ethics_level must be in"):
            solver.solve(
                initial_state=initial_state,
                depth=1,
                ethics_level=-0.1
            )
    
    def test_ethics_level_above_bounds_raises_error(self):
        """Test that ethics_level > 1.0 raises ValueError."""
        solver = MentorshipSolver()
        initial_state = {'coherence': 0.5}
        
        with pytest.raises(ValueError, match="ethics_level must be in"):
            solver.solve(
                initial_state=initial_state,
                depth=1,
                ethics_level=1.1
            )


class TestConfigurableConvergenceThreshold:
    """Test configurable convergence threshold behavior."""
    
    def test_different_thresholds_affect_iterations(self):
        """Test that different thresholds result in different iteration counts."""
        initial_state = {'coherence': 0.3}
        
        # Loose threshold - should converge quickly
        solver_loose = MentorshipSolver(converge_threshold=0.1)
        _, iterations_loose = solver_loose.solve(
            initial_state=initial_state.copy(),
            depth=2,
            ethics_level=0.5
        )
        
        # Tight threshold - should take more iterations
        solver_tight = MentorshipSolver(converge_threshold=0.0001)
        _, iterations_tight = solver_tight.solve(
            initial_state=initial_state.copy(),
            depth=2,
            ethics_level=0.5
        )
        
        # Tighter threshold should generally require more iterations
        # (or both hit max_iterations)
        assert iterations_loose <= iterations_tight
    
    def test_convergence_detection(self):
        """Test that convergence is properly detected."""
        solver = MentorshipSolver(
            converge_threshold=0.001,
            max_iterations=100
        )
        initial_state = {'coherence': 0.5}
        
        final_state, iterations = solver.solve(
            initial_state=initial_state,
            depth=2,
            ethics_level=0.7
        )
        
        # Should converge within max_iterations
        assert final_state.get('converged') is not None
        assert iterations <= solver.max_iterations


class TestPluggableOperatorStrategies:
    """Test pluggable operator strategy functionality."""
    
    def test_custom_resonate_strategy(self):
        """Test solver works with custom ResonateStrategy."""
        custom_ops = OperatorBundle(
            resonate=ResonateStrategy(resonance_factor=0.95)
        )
        
        solver = MentorshipSolver(operators=custom_ops)
        initial_state = {'coherence': 0.4}
        
        final_state, iterations = solver.solve(
            initial_state=initial_state,
            depth=2,
            ethics_level=0.8
        )
        
        assert final_state is not None
        assert 'resonance_applied' in final_state
    
    def test_custom_measure_strategy(self):
        """Test solver works with custom MeasureStrategy."""
        custom_ops = OperatorBundle(
            measure=MeasureStrategy(precision=0.99)
        )
        
        solver = MentorshipSolver(operators=custom_ops)
        initial_state = {'coherence': 0.5}
        
        final_state, iterations = solver.solve(
            initial_state=initial_state,
            depth=1,
            ethics_level=0.6
        )
        
        assert final_state is not None
        assert 'measurement_applied' in final_state
    
    def test_custom_adapt_strategy(self):
        """Test solver works with custom AdaptStrategy."""
        custom_ops = OperatorBundle(
            adapt=AdaptStrategy(adaptation_rate=0.75)
        )
        
        solver = MentorshipSolver(operators=custom_ops)
        initial_state = {'coherence': 0.3}
        
        final_state, iterations = solver.solve(
            initial_state=initial_state,
            depth=3,
            ethics_level=0.9
        )
        
        assert final_state is not None
        assert 'adaptation_applied' in final_state
    
    def test_custom_audit_strategy(self):
        """Test solver works with custom AuditStrategy."""
        custom_ops = OperatorBundle(
            audit=AuditStrategy(audit_threshold=0.6)
        )
        
        solver = MentorshipSolver(operators=custom_ops)
        initial_state = {'coherence': 0.7}
        
        final_state, iterations = solver.solve(
            initial_state=initial_state,
            depth=1,
            ethics_level=0.8
        )
        
        assert final_state is not None
        assert 'audit_applied' in final_state
        assert 'audit_valid' in final_state
    
    def test_fully_custom_operator_bundle(self):
        """Test solver with completely custom operator bundle."""
        custom_ops = OperatorBundle(
            resonate=ResonateStrategy(resonance_factor=0.9),
            measure=MeasureStrategy(precision=0.98),
            adapt=AdaptStrategy(adaptation_rate=0.7),
            audit=AuditStrategy(audit_threshold=0.65)
        )
        
        solver = MentorshipSolver(
            operators=custom_ops,
            converge_threshold=0.0005
        )
        
        initial_state = {'coherence': 0.35}
        
        final_state, iterations = solver.solve(
            initial_state=initial_state,
            depth=4,
            ethics_level=0.85
        )
        
        assert final_state is not None
        assert 'resonance_applied' in final_state
        assert 'measurement_applied' in final_state
        assert 'adaptation_applied' in final_state
        assert 'audit_applied' in final_state


class TestSampleAndGridMethods:
    """Test sample_07_run and grid_experiments methods."""
    
    def test_sample_07_run(self):
        """Test sample_07_run method executes successfully."""
        solver = create_default_solver()
        results = solver.sample_07_run()
        
        assert results is not None
        assert 'run_id' in results
        assert results['run_id'] == 'sample_07'
        assert 'initial_coherence' in results
        assert 'final_coherence' in results
        assert 'iterations' in results
        assert 'converged' in results
    
    def test_grid_experiments_default(self):
        """Test grid_experiments with default parameters."""
        solver = create_default_solver()
        results = solver.grid_experiments()
        
        assert results is not None
        assert isinstance(results, list)
        assert len(results) > 0
        
        # Check structure of first result
        first_result = results[0]
        assert 'depth' in first_result
        assert 'ethics_level' in first_result
        assert 'initial_coherence' in first_result
        assert 'final_coherence' in first_result
        assert 'iterations' in first_result
        assert 'converged' in first_result
    
    def test_grid_experiments_custom_ranges(self):
        """Test grid_experiments with custom parameter ranges."""
        solver = create_default_solver()
        results = solver.grid_experiments(
            depth_range=range(0, 3),
            ethics_range=(0.3, 0.6)
        )
        
        assert len(results) == 3 * 2  # 3 depths × 2 ethics values
        
        # Verify all combinations are present
        depths_tested = set(r['depth'] for r in results)
        ethics_tested = set(r['ethics_level'] for r in results)
        
        assert depths_tested == {0, 1, 2}
        assert ethics_tested == {0.3, 0.6}


class TestOperatorStrategies:
    """Test individual operator strategies."""
    
    def test_resonate_strategy_apply(self):
        """Test ResonateStrategy.apply method."""
        strategy = ResonateStrategy(resonance_factor=0.8)
        state = {'coherence': 0.5}
        context = {'depth': 1, 'ethics_level': 0.7}
        
        result = strategy.apply(state, context)
        
        assert 'coherence' in result
        assert 'resonance_applied' in result
        assert result['resonance_applied'] is True
    
    def test_measure_strategy_apply(self):
        """Test MeasureStrategy.apply method."""
        strategy = MeasureStrategy(precision=0.95)
        state = {'coherence': 0.6}
        context = {'ethics_level': 0.8}
        
        result = strategy.apply(state, context)
        
        assert 'measured_coherence' in result
        assert 'measurement_applied' in result
        assert result['measurement_applied'] is True
    
    def test_adapt_strategy_apply(self):
        """Test AdaptStrategy.apply method."""
        strategy = AdaptStrategy(adaptation_rate=0.6)
        state = {'coherence': 0.4}
        context = {'depth': 2, 'ethics_level': 0.7}
        
        result = strategy.apply(state, context)
        
        assert 'coherence' in result
        assert 'adaptation_applied' in result
        assert result['adaptation_applied'] is True
    
    def test_audit_strategy_apply(self):
        """Test AuditStrategy.apply method."""
        strategy = AuditStrategy(audit_threshold=0.7)
        state = {'coherence': 0.8}
        context = {'ethics_level': 0.9}
        
        result = strategy.apply(state, context)
        
        assert 'audit_valid' in result
        assert 'audit_score' in result
        assert 'audit_applied' in result
        assert result['audit_applied'] is True


class TestCoherenceBounds:
    """Test that coherence values stay within valid bounds."""
    
    def test_coherence_stays_in_bounds(self):
        """Test that coherence values remain in [0.0, 1.0]."""
        solver = MentorshipSolver()
        
        # Test with very high initial coherence
        state_high = {'coherence': 0.99}
        final_high, _ = solver.solve(state_high, depth=3, ethics_level=0.9)
        assert 0.0 <= final_high['coherence'] <= 1.0
        
        # Test with very low initial coherence
        state_low = {'coherence': 0.01}
        final_low, _ = solver.solve(state_low, depth=3, ethics_level=0.9)
        assert 0.0 <= final_low['coherence'] <= 1.0

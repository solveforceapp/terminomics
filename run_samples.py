#!/usr/bin/env python3
"""
Run samples script for MentorshipSolver v4.0

This script executes sample_07_run and grid_experiments to demonstrate
the MentorshipSolver functionality.
"""

from mentorship_solver import create_default_solver, MentorshipSolver
import json


def print_separator(title: str = ""):
    """Print a formatted separator line."""
    if title:
        print(f"\n{'=' * 70}")
        print(f"  {title}")
        print(f"{'=' * 70}\n")
    else:
        print(f"{'=' * 70}\n")


def run_sample_07():
    """Execute sample_07_run and print results."""
    print_separator("Sample 07 Run")
    
    solver = create_default_solver(converge_threshold=0.001)
    results = solver.sample_07_run()
    
    print("Sample 07 Results:")
    print(f"  Run ID: {results['run_id']}")
    print(f"  Initial Coherence: {results['initial_coherence']:.4f}")
    print(f"  Final Coherence: {results['final_coherence']:.4f}")
    print(f"  Iterations: {results['iterations']}")
    print(f"  Converged: {results['converged']}")
    print(f"  Audit Valid: {results['audit_valid']}")
    
    return results


def run_grid_experiments():
    """Execute grid_experiments and print results."""
    print_separator("Grid Experiments")
    
    solver = create_default_solver(converge_threshold=0.001)
    results = solver.grid_experiments(
        depth_range=range(0, 4),
        ethics_range=(0.2, 0.5, 0.8)
    )
    
    print(f"Grid Experiments: {len(results)} configurations\n")
    
    # Print header
    print(f"{'Depth':<8} {'Ethics':<10} {'Initial':<12} {'Final':<12} {'Iters':<8} {'Conv':<8} {'Valid':<8}")
    print(f"{'-' * 8} {'-' * 10} {'-' * 12} {'-' * 12} {'-' * 8} {'-' * 8} {'-' * 8}")
    
    # Print each result
    for result in results:
        print(
            f"{result['depth']:<8} "
            f"{result['ethics_level']:<10.2f} "
            f"{result['initial_coherence']:<12.4f} "
            f"{result['final_coherence']:<12.4f} "
            f"{result['iterations']:<8} "
            f"{str(result['converged']):<8} "
            f"{str(result['audit_valid']):<8}"
        )
    
    # Summary statistics
    print_separator()
    converged_count = sum(1 for r in results if r['converged'])
    valid_count = sum(1 for r in results if r['audit_valid'])
    avg_iterations = sum(r['iterations'] for r in results) / len(results)
    avg_final_coherence = sum(r['final_coherence'] for r in results) / len(results)
    
    print("Summary Statistics:")
    print(f"  Total Experiments: {len(results)}")
    print(f"  Converged: {converged_count} ({100*converged_count/len(results):.1f}%)")
    print(f"  Audit Valid: {valid_count} ({100*valid_count/len(results):.1f}%)")
    print(f"  Average Iterations: {avg_iterations:.2f}")
    print(f"  Average Final Coherence: {avg_final_coherence:.4f}")
    
    return results


def run_custom_configuration():
    """Run a custom configuration example with modified strategies."""
    print_separator("Custom Configuration Example")
    
    from mentorship_solver import (
        OperatorBundle, ResonateStrategy, MeasureStrategy,
        AdaptStrategy, AuditStrategy
    )
    
    # Create custom operator bundle
    custom_ops = OperatorBundle(
        resonate=ResonateStrategy(resonance_factor=0.9),
        measure=MeasureStrategy(precision=0.98),
        adapt=AdaptStrategy(adaptation_rate=0.7),
        audit=AuditStrategy(audit_threshold=0.65)
    )
    
    # Create solver with custom operators and threshold
    solver = MentorshipSolver(
        operators=custom_ops,
        converge_threshold=0.0005,
        max_iterations=150
    )
    
    initial_state = {
        'coherence': 0.25,
        'name': 'Custom_Config',
        'type': 'high_precision'
    }
    
    final_state, iterations = solver.solve(
        initial_state=initial_state,
        depth=5,
        ethics_level=0.9
    )
    
    print("Custom Configuration Results:")
    print(f"  Initial Coherence: {initial_state['coherence']:.4f}")
    print(f"  Final Coherence: {final_state.get('coherence', 0):.4f}")
    print(f"  Iterations: {iterations}")
    print(f"  Converged: {final_state.get('converged', False)}")
    print(f"  Audit Score: {final_state.get('audit_score', 0):.4f}")
    
    return final_state


def main():
    """Main execution function."""
    print("\n" + "=" * 70)
    print("  MentorshipSolver v4.0 - Sample Executions")
    print("  Terminomics Framework - Coherence Architecture")
    print("=" * 70)
    
    # Run sample 07
    sample_results = run_sample_07()
    
    # Run grid experiments
    grid_results = run_grid_experiments()
    
    # Run custom configuration
    custom_results = run_custom_configuration()
    
    print_separator("Execution Complete")
    print("All samples and experiments completed successfully.")
    print(f"Total experiments run: {1 + len(grid_results) + 1}")
    print()


if __name__ == "__main__":
    main()

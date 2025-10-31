# Pytest Instructions for MentorshipSolver v4.0

## Overview

This directory contains pytest unit tests for the MentorshipSolver v4.0 implementation, part of the Terminomics Framework coherence architecture.

## Test Coverage

The test suite covers:

- **Basic Functionality**: Solver initialization with default and custom parameters
- **Depth=0 Case**: Special handling for base recursion case (immediate return)
- **Ethics Level Validation**: Bounds checking for ethics_level parameter (0.0-1.0)
- **Configurable Convergence**: Custom convergence thresholds and iteration behavior
- **Pluggable Strategies**: Custom operator strategy injection (Resonate, Measure, Adapt, Audit)
- **Sample Methods**: `sample_07_run()` and `grid_experiments()` functionality
- **Individual Operators**: Direct testing of each operator strategy
- **Coherence Bounds**: Validation that coherence stays within [0.0, 1.0]

## Installation

Install pytest if not already available:

```bash
pip install pytest
```

## Running Tests

### Run all tests:

```bash
pytest tests/
```

### Run with verbose output:

```bash
pytest tests/ -v
```

### Run specific test class:

```bash
pytest tests/test_mentorship_solver.py::TestDepthZeroCase -v
```

### Run specific test:

```bash
pytest tests/test_mentorship_solver.py::TestEthicsLevelValidation::test_ethics_level_below_bounds_raises_error -v
```

### Run with coverage report:

```bash
pip install pytest-cov
pytest tests/ --cov=mentorship_solver --cov-report=term-missing
```

## Test Organization

Tests are organized into classes by functionality:

- `TestMentorshipSolverBasics`: Core initialization and factory functions
- `TestDepthZeroCase`: Depth=0 special case handling
- `TestEthicsLevelValidation`: Parameter validation
- `TestConfigurableConvergenceThreshold`: Convergence behavior
- `TestPluggableOperatorStrategies`: Custom strategy injection
- `TestSampleAndGridMethods`: Sample execution methods
- `TestOperatorStrategies`: Individual operator testing
- `TestCoherenceBounds`: Value constraint validation

## Expected Results

All tests should pass. If any tests fail:

1. Check that `mentorship_solver.py` is in the parent directory
2. Verify Python version compatibility (Python 3.7+)
3. Review the specific test failure message for details

## Adding New Tests

When adding new tests:

1. Follow the existing naming convention: `test_<feature>_<behavior>`
2. Use descriptive docstrings
3. Group related tests into appropriate test classes
4. Include both positive and negative test cases

## Continuous Integration

These tests are designed to be run in CI/CD pipelines. Exit code 0 indicates all tests passed.

```bash
pytest tests/ --tb=short
```

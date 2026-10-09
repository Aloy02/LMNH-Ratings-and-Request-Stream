# Pytest-Based Testing Skill

## Overview
This skill provides a reusable pattern for creating unit tests using pytest-style testing. It follows the testing patterns established in `test_consumer.py` and can be applied to any Python module.

## Key Principles

1. **Class-based organization**: Group test cases by function/method in dedicated test classes
2. **Pytest assertions**: Use simple `assert` statements instead of `unittest` methods
3. **No mock requirements**: Focus on testing pure functions without external dependencies
4. **Descriptive naming**: Test class names follow `Test<FunctionName>` pattern
5. **Clear documentation**: Each test has a docstring explaining what it tests

## Structure Template

```python
"""Unit tests for <module_name> module."""

import pytest
from <module_name> import <function_1>, <function_2>


class MockObject:
    """Helper class to simulate external objects without mocking libraries."""
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def method_name(self):
        """Simulate object methods."""
        return self._value


class Test<FunctionName>:
    """Test cases for the <function_name> function."""
    
    def test_<function_name>_<scenario_1>(self):
        """Test <function_name> with <specific_scenario>."""
        # Arrange
        input_data = ...
        
        # Act
        result = <function_name>(input_data)
        
        # Assert
        assert result == expected_value
    
    def test_<function_name>_<scenario_2>(self):
        """Test <function_name> with <another_scenario>."""
        # Arrange, Act, Assert pattern
        ...


class Test<AnotherFunction>:
    """Test cases for the <another_function> function."""
    ...
```

## Step-by-Step Process

### Step 1: Analyze Target Module
- Identify all pure functions (no external dependencies like DB, API calls)
- Document their parameters and return types
- Determine edge cases and normal cases

### Step 2: Create Test Helper Classes
- Build lightweight mock objects using simple classes
- Simulate complex objects (like Kafka Message) without `unittest.mock`
- Example:
  ```python
  class SimpleMessage:
      def __init__(self, value=None, error=None):
          self._value = value
          self._error = error
      
      def value(self):
          return self._value
      
      def error(self):
          return self._error
  ```

### Step 3: Create Test Classes
- One test class per function being tested
- Name: `Test<FunctionName>`
- Example: `TestIsValidMessage`, `TestDecodeMessage`

### Step 4: Write Test Methods
- Naming: `test_<function_name>_<scenario>`
- Use AAA pattern: Arrange, Act, Assert
- Example:
  ```python
  def test_is_valid_message_with_none(self):
      """Test that is_valid_message returns False when message is None."""
      result = is_valid_message(None)
      assert result == False
  ```

### Step 5: Test Different Scenarios
For each function, create tests for:
- **Happy path**: Normal expected behavior
- **Edge cases**: Boundary conditions, empty inputs
- **Error cases**: Invalid inputs, None values
- **Type validation**: Correct data types returned

## Pytest-Specific Advantages

1. **Simpler assertions**: `assert x == y` instead of `self.assertEqual(x, y)`
2. **Easier to read**: No boilerplate `setUp()` or `tearDown()` methods
3. **Better error messages**: Pytest shows exact assertion failures
4. **Flexible**: Works with or without class structure
5. **Plugin ecosystem**: Can add plugins for coverage, markers, etc.

## Common Assertion Patterns

```python
# Equality
assert result == expected

# Boolean values
assert result is True
assert result is False
assert result == False  # Also valid

# Type checking
assert isinstance(result, dict)
assert isinstance(result, (int, float))

# Membership
assert key in result
assert value in result_list

# None checks
assert result is None
assert result is not None

# Exception handling
with pytest.raises(ValueError):
    <function_that_should_raise>()
```

## Running Tests

**Run all tests in a file:**
```bash
pytest test_consumer.py -v
```

**Run specific test class:**
```bash
pytest test_consumer.py::TestIsValidMessage -v
```

**Run specific test method:**
```bash
pytest test_consumer.py::TestIsValidMessage::test_is_valid_message_with_none -v
```

**Run with coverage:**
```bash
pytest test_consumer.py --cov=consumer --cov-report=html
```

## File Naming Convention

- Test file: `test_<module_name>.py`
- Located in same directory as module being tested
- Example: `consumer.py` → `test_consumer.py`

## Checklist for New Test Files

- [ ] Test file named `test_<module_name>.py`
- [ ] All pure functions have corresponding test classes
- [ ] Each test class named `Test<FunctionName>`
- [ ] Each test method documented with docstring
- [ ] Multiple scenarios tested per function (happy path + edge cases)
- [ ] No external dependencies (no real API/DB calls)
- [ ] Helper mock classes defined for complex objects
- [ ] All tests use simple `assert` statements
- [ ] Tests run successfully with `pytest test_<module_name>.py`
- [ ] Code is organized by test classes for clarity

## Example: Testing a Module with Data Transformation

```python
"""Unit tests for transform module."""

from transform import extract_field, validate_data


class TestExtractField:
    """Test cases for extract_field function."""
    
    def test_extract_field_existing_key(self):
        """Test extracting a field that exists."""
        data = {"id": 1, "name": "test"}
        result = extract_field(data, "name")
        assert result == "test"
    
    def test_extract_field_missing_key(self):
        """Test extracting a field that doesn't exist."""
        data = {"id": 1, "name": "test"}
        result = extract_field(data, "age")
        assert result is None
    
    def test_extract_field_empty_dict(self):
        """Test extracting from empty dictionary."""
        result = extract_field({}, "any_key")
        assert result is None


class TestValidateData:
    """Test cases for validate_data function."""
    
    def test_validate_data_valid_input(self):
        """Test validation with complete valid data."""
        data = {"id": 1, "name": "test", "timestamp": "2024-01-01T00:00:00"}
        result = validate_data(data)
        assert result is True
    
    def test_validate_data_missing_required_field(self):
        """Test validation with missing required field."""
        data = {"id": 1}  # missing 'name'
        result = validate_data(data)
        assert result is False
    
    def test_validate_data_none_input(self):
        """Test validation with None input."""
        result = validate_data(None)
        assert result is False
```

## Best Practices

1. **One responsibility per test**: Each test should verify one behavior
2. **Descriptive names**: Test names should clearly state what they test
3. **Avoid test interdependence**: Tests should be independent
4. **Use fixtures for setup**: For repetitive setup, consider pytest fixtures
5. **Keep tests maintainable**: If test code is complex, refactor the source code
6. **Test what matters**: Focus on business logic, not implementation details
7. **Document expected behavior**: Docstrings explain the purpose of each test

## Troubleshooting

**Tests not discovered:**
- Ensure file is named `test_*.py` or `*_test.py`
- Ensure classes are named `Test*` (capital T)
- Ensure methods are named `test_*` (lowercase)

**Import errors:**
- Verify module path is correct
- Run tests from project root directory
- Check that `__init__.py` exists in package directories

**Assertion failures:**
- Read pytest's detailed assertion output
- Use `print()` statements for debugging
- Run specific test: `pytest test_file.py::TestClass::test_method -v -s`

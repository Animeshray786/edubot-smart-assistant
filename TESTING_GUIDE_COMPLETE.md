# Testing Guide - EduBot Chatbot

Complete testing suite with unit tests, integration tests, API tests, and load tests.

## Table of Contents

1. [Setup](#setup)
2. [Running Tests](#running-tests)
3. [Test Coverage](#test-coverage)
4. [Load Testing](#load-testing)
5. [Security Testing](#security-testing)
6. [Continuous Integration](#continuous-integration)

---

## Setup

### Install Testing Dependencies

```bash
# Install all testing packages
pip install pytest pytest-cov pytest-flask pytest-mock locust

# Verify installation
pytest --version
locust --version
```

### Test Configuration

The test suite uses `pytest.ini` and `tests/conftest.py` for configuration.

**Key Settings:**
- **Test Discovery:** Automatically finds files matching `test_*.py`
- **Coverage Target:** 70% minimum coverage
- **Markers:** unit, integration, api, e2e, slow, security

---

## Running Tests

### Run All Tests

```bash
# Run all tests with coverage
pytest

# Run with verbose output
pytest -v

# Run with detailed output
pytest -vv --tb=long
```

### Run Specific Test Types

```bash
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# API tests only
pytest -m api

# Security tests only
pytest -m security
```

### Run Specific Test Files

```bash
# Test backend modules
pytest tests/test_backend.py

# Test API endpoints
pytest tests/test_api.py

# Test specific class
pytest tests/test_backend.py::TestSecurityManager

# Test specific function
pytest tests/test_backend.py::TestSecurityManager::test_xss_prevention
```

### Run Tests in Parallel

```bash
# Install pytest-xdist
pip install pytest-xdist

# Run tests in parallel (auto-detect CPU cores)
pytest -n auto

# Run with 4 workers
pytest -n 4
```

---

## Test Coverage

### Generate Coverage Reports

```bash
# Run tests with coverage
pytest --cov=backend --cov=database --cov=routes

# Generate HTML coverage report
pytest --cov=backend --cov=database --cov=routes --cov-report=html

# Open coverage report
start htmlcov/index.html  # Windows
open htmlcov/index.html   # macOS
xdg-open htmlcov/index.html  # Linux
```

### Coverage Thresholds

The project aims for:
- **Overall:** 70%+ coverage
- **Critical Modules:** 80%+ coverage
- **Security Modules:** 90%+ coverage

### View Coverage in Terminal

```bash
pytest --cov=backend --cov-report=term-missing
```

This shows which lines are not covered by tests.

---

## Load Testing

### Setup Locust

Locust is configured in `tests/test_load.py` with multiple user scenarios.

### Run Load Tests

#### Basic Load Test

```bash
# Start Locust web UI
locust -f tests/test_load.py --host=http://localhost:5000

# Open browser to http://localhost:8089
# Configure:
#   - Number of users: 100
#   - Spawn rate: 10 users/second
```

#### Headless Load Test

```bash
# Run without web UI
locust -f tests/test_load.py --host=http://localhost:5000 \
       --users 100 --spawn-rate 10 --run-time 5m --headless

# With specific user class
locust -f tests/test_load.py --host=http://localhost:5000 \
       --users 50 --spawn-rate 5 ChatBotUser --headless
```

### Load Test Scenarios

#### 1. Normal Load (ChatBotUser)
- 100 concurrent users
- 1-3 seconds between requests
- Simulates typical usage

```bash
locust -f tests/test_load.py --host=http://localhost:5000 \
       --users 100 --spawn-rate 10 ChatBotUser --run-time 10m
```

#### 2. Stress Test (StressTest)
- 500+ concurrent users
- 0.1-0.5 seconds between requests
- Tests system limits

```bash
locust -f tests/test_load.py --host=http://localhost:5000 \
       --users 500 --spawn-rate 50 StressTest --run-time 5m
```

#### 3. Spike Test (SpikeTest)
- Sudden traffic increase
- 0.1-1 seconds between requests
- Tests system recovery

```bash
locust -f tests/test_load.py --host=http://localhost:5000 \
       --users 200 --spawn-rate 100 SpikeTest --run-time 3m
```

#### 4. Endurance Test (EnduranceTest)
- Sustained load over time
- Tests memory leaks and stability

```bash
locust -f tests/test_load.py --host=http://localhost:5000 \
       --users 100 --spawn-rate 10 EnduranceTest --run-time 60m
```

### Analyzing Load Test Results

Locust provides:
- **RPS (Requests Per Second):** Throughput metric
- **Response Times:** P50, P95, P99 percentiles
- **Failure Rate:** % of failed requests
- **Active Users:** Current user count

**Performance Targets:**
- Response Time (P95): < 500ms
- Response Time (P99): < 1000ms
- Failure Rate: < 1%
- Concurrent Users: 1000+

---

## Security Testing

### OWASP Top 10 Tests

The test suite includes security tests for:

1. **SQL Injection**
   ```bash
   pytest tests/test_backend.py::TestSecurityManager::test_sql_injection_detection -v
   ```

2. **XSS (Cross-Site Scripting)**
   ```bash
   pytest tests/test_backend.py::TestSecurityManager::test_xss_prevention -v
   ```

3. **CSRF (Cross-Site Request Forgery)**
   ```bash
   pytest tests/test_backend.py::TestSecurityManager::test_csrf_token_validation -v
   ```

4. **Input Validation**
   ```bash
   pytest tests/test_backend.py::TestSecurityManager::test_input_sanitization -v
   ```

5. **Password Security**
   ```bash
   pytest tests/test_backend.py::TestSecurityManager::test_password_validation -v
   ```

### Manual Security Testing

#### Test CSRF Protection

```bash
# Get CSRF token
curl http://localhost:5000/api/security/csrf-token

# Try request without token (should fail)
curl -X POST http://localhost:5000/api/chat \
     -H "Content-Type: application/json" \
     -d '{"message":"test"}'

# Try with token (should succeed)
curl -X POST http://localhost:5000/api/chat \
     -H "Content-Type: application/json" \
     -H "X-CSRF-Token: YOUR_TOKEN" \
     -d '{"message":"test"}'
```

#### Test Rate Limiting

```bash
# Send 100 requests rapidly
for i in {1..100}; do
  curl http://localhost:5000/api/chat \
       -H "Content-Type: application/json" \
       -d '{"message":"test"}' &
done
wait

# Should receive 429 Too Many Requests
```

#### Test Input Validation

```bash
# Test XSS prevention
curl -X POST http://localhost:5000/api/security/validate-input \
     -H "Content-Type: application/json" \
     -d '{"text":"<script>alert(1)</script>","type":"text"}'

# Test SQL injection detection
curl -X POST http://localhost:5000/api/security/validate-input \
     -H "Content-Type: application/json" \
     -d '{"text":"'; DROP TABLE users;--","type":"text"}'
```

---

## Continuous Integration

### GitHub Actions Workflow

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest --cov=backend --cov=database --cov=routes \
               --cov-report=xml --cov-report=term
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### Pre-commit Hooks

Install pre-commit hooks:

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8

  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
EOF

# Install hooks
pre-commit install
```

---

## Test Writing Guidelines

### Unit Test Template

```python
import pytest

@pytest.mark.unit
class TestMyFeature:
    """Test MyFeature functionality"""
    
    def test_basic_functionality(self, app):
        """Test basic feature works"""
        # Arrange
        input_data = "test"
        
        # Act
        result = my_function(input_data)
        
        # Assert
        assert result is not None
        assert result == expected_value
    
    def test_edge_cases(self, app):
        """Test edge cases"""
        assert my_function("") == ""
        assert my_function(None) is None
```

### Integration Test Template

```python
import pytest
import json

@pytest.mark.integration
class TestMyAPI:
    """Test MyAPI endpoints"""
    
    def test_endpoint(self, client, sample_user):
        """Test API endpoint"""
        # Arrange
        with client.session_transaction() as sess:
            sess['user_id'] = sample_user.user_id
        
        # Act
        response = client.post('/api/endpoint', json={
            'data': 'value'
        })
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'result' in data
```

---

## Common Testing Commands

```bash
# Quick test run (no coverage)
pytest -q

# Verbose with coverage
pytest -v --cov

# Stop on first failure
pytest -x

# Re-run failed tests
pytest --lf

# Run only changed tests
pytest --testmon

# Show local variables in failures
pytest -l

# Run specific test with print output
pytest -s tests/test_backend.py::test_function

# Generate JUnit XML report
pytest --junitxml=report.xml

# Parallel execution with coverage
pytest -n auto --cov --cov-report=html
```

---

## Troubleshooting

### Tests Failing

```bash
# Clear pytest cache
pytest --cache-clear

# Clear __pycache__
find . -type d -name __pycache__ -exec rm -rf {} +

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Coverage Issues

```bash
# Check which files are being tested
pytest --collect-only

# Show coverage paths
pytest --cov --cov-report=term

# Debug coverage
pytest --cov --cov-report=term-missing --cov-report=html -vv
```

### Locust Issues

```bash
# Check Locust installation
locust --version

# Run with debug logging
locust -f tests/test_load.py --loglevel DEBUG

# Test without web UI
locust -f tests/test_load.py --host=http://localhost:5000 \
       --users 1 --spawn-rate 1 --run-time 10s --headless
```

---

## Performance Benchmarks

### Target Metrics

| Metric | Target | Critical |
|--------|--------|----------|
| Unit Test Coverage | 80% | 70% |
| Integration Coverage | 70% | 60% |
| Test Execution Time | < 60s | < 120s |
| Load Test RPS | 1000+ | 500+ |
| P95 Response Time | < 500ms | < 1000ms |
| Concurrent Users | 1000+ | 500+ |
| Error Rate | < 0.1% | < 1% |

---

## Next Steps

1. **Run initial test suite:** `pytest -v --cov`
2. **Check coverage report:** Open `htmlcov/index.html`
3. **Run load test:** `locust -f tests/test_load.py`
4. **Fix failing tests:** Review test output
5. **Increase coverage:** Write tests for uncovered code
6. **Setup CI/CD:** Configure GitHub Actions
7. **Monitor metrics:** Track performance over time

---

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Locust Documentation](https://docs.locust.io/)
- [Flask Testing](https://flask.palletsprojects.com/en/3.0.x/testing/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Coverage.py](https://coverage.readthedocs.io/)

---

**Test Coverage Report Generated:** `htmlcov/index.html`  
**Load Test Dashboard:** `http://localhost:8089` (when Locust is running)

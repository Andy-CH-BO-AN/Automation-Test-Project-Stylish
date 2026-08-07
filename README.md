# Automation-Test-Program-Batch2-Project

A comprehensive test automation framework for the "Stylish" e-commerce application, combining **Web UI testing** (Selenium), **API testing** (requests), and **Database validation** (MySQL). Tests run in parallel with automatic retry and Allure reporting.

## Project Overview

This project provides end-to-end test automation for the Stylish e-commerce platform, covering:
- **Web UI Testing**: Selenium-based browser automation with Page Object Model
- **API Testing**: REST API validation with request/response logging
- **Database Validation**: MySQL data integrity checks
- **Parallel Execution**: Multi-worker test runs with automatic retries
- **Rich Reporting**: Allure HTML reports with screenshots and detailed logs

## Architecture Layers

### 1. Test Layer (Entry Points)
- `tests_api/` - REST API tests using pytest fixtures and parametrization
- `tests_web/` - Selenium-based UI tests with screenshot attachments
- **Key Pattern**: Tests inherit fixtures from local `conftest.py` which chains to root `conftest.py` for DB setup

### 2. Object Layer (Page Object Model & API Objects)
- `page_objects/` - Page classes (LoginPage, CartPage, etc.) extending `PageBase`
- `api_objects/` - API endpoint classes (LoginApi, CreateOrderApi, etc.) extending `ApiBase`
- **Convention**: Locators as class variables using `(By.*, selector)` tuples; methods encapsulate user interactions

### 3. Base Classes & Utils (`utils/`)
- **`PageBase`**: Wraps Selenium with 20s WebDriverWait, provides `find_element()`, `scroll_down()`, JWT token manipulation via `localStorage`
- **`ApiBase`**: Wraps requests.Session, logs all request/response details, handles JSON payloads
- **`db_utils.py`**: `query_method()` helper for DictCursor queries with logging

## Quick Start

### Prerequisites
- Python 3.8+
- Chrome browser (for web tests)
- Access to MySQL database
- Environment variables configured

### Setup
```bash
# Clone repository
git clone https://github.com/Andy-CH-BO-AN/Automation-Test-Project-Stylish.git
cd Automation-Test-Project-Stylish

# Create virtual environment
python3 -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate

# Install dependencies
pip3 install -r requirements.txt
```

### Environment Configuration
Create a `.env` file in the project root with the following variables:
```env
BASE_URL=https://api.example.com
DOMAIN=https://www.example.com
DB_HOST=your-db-host
DB_PORT=3306
DB_USERNAME=your-username
DB_PASSWORD=your-password
DB_NAME=stylish_backend
USER_NAME_1=test-user1@example.com
USER_NAME_2=test-user2@example.com
PASSWORD=test-password
```

## Running Tests

### Single Test
```bash
pytest tests_api/test_login_api.py::TestLogin::test_login_success -v
```

### Parallel Execution with Retry
```bash
pytest -n 2 --reruns 1 tests_api/ tests_web/
```

### Generate Allure Report
```bash
allure generate ./allure-results/ -o ./allure-report/ --clean
```

### Full Pipeline
```bash
# Using the provided script
./exec_test.sh
```

**Parallel Worker Assignment**:
- `gw0` → `USER_NAME_1`
- `gw1` → `USER_NAME_2`
- Other workers → `USER_NAME_1` (fallback)

## Key Patterns & Conventions

### Page Object Pattern
```python
class LoginPage(PageBase):
    input_email = (By.ID, "email")
    btn_login = (By.XPATH, "//button[text()='Login']")
    
    def login(self, email, password):
        self.find_element(self.input_email).send_keys(email)
        self.find_element(self.btn_login).click()
```

### API Object Pattern
```python
class LoginApi(ApiBase):
    def __init__(self, session, email, password):
        url = f"{os.getenv('BASE_URL')}/user/login"
        super().__init__(session, url)
        self.payload = {"provider": "native", "email": email, "password": password}
    
    def send(self):
        response = self.api_request("post", self.payload)
        if response.status_code == 200:
            self.session.headers["Authorization"] = f"Bearer {response.json()['data']['access_token']}"
        return response
```

### Test Organization
- **Allure decorators**: `@allure.feature()`, `@allure.title()`, `@allure.step()`
- **Parametrization**: `@pytest.mark.parametrize()` for data-driven tests
- **Fixtures**: Request-scoped for resources, session-scoped for DB connections
- **Assertions**: Direct `assert` statements with logging

## Cross-Component Communication

### API → Database Validation
API responses are validated against database queries to ensure data consistency.

### Web → API Token Reuse
JWT tokens extracted from browser localStorage can be reused in API tests.

### Configuration Flow
Environment variables are loaded at test collection time and propagated through fixtures.

## CI/CD Integration

The original course project used a Jenkins environment. Environment-specific hostnames and credentials are intentionally not copied into this public repository.

### Pipeline
The `exec_test.sh` script provides a complete CI/CD pipeline:
1. Virtual environment setup
2. Dependency installation
3. Parallel test execution with retries
4. Allure report generation

## Important File References

- **Configuration**: `conftest.py` (root), `tests_api/conftest.py`, `tests_web/conftest.py`
- **Infrastructure**: `utils/page_base.py`, `utils/api_utils.py`, `db_utilis/db_utils.py`
- **Reporting**: `pytest.ini`, `exec_test.sh`
- **Data Models**: `table_object/`, `test_data/`
- **AI Agent Guide**: `AGENTS.md`

## Contributing

1. Follow the established patterns in `AGENTS.md`
2. Add new tests following the Page Object and API Object patterns
3. Include appropriate Allure decorators and logging
4. Test both locally and in CI before submitting PRs

## Troubleshooting

- **Chrome Driver Issues**: WebDriverManager handles automatic driver downloads
- **Database Connection**: Verify `.env` configuration and network access
- **Parallel Execution**: Check worker assignment in `conftest.py` files
- **Report Generation**: Ensure Allure CLI is installed and results directory exists

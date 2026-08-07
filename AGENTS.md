# AGENTS.md - AI Agent Guide for Automation-Test-Program-Batch2

## Project Overview
A comprehensive test automation framework for the "Stylish" e-commerce application, combining **Web UI testing** (Selenium), **API testing** (requests), and **Database validation** (MySQL). Tests run in parallel with automatic retry and Allure reporting.

## Architecture Layers

### 1. **Test Layer** (Entry Points)
- `tests_api/` - REST API tests using pytest fixtures and parametrization
- `tests_web/` - Selenium-based UI tests with screenshot attachments
- **Key Pattern**: Tests inherit fixtures from local `conftest.py` which chains to root `conftest.py` for DB setup

### 2. **Object Layer** (Page Object Model & API Objects)
- `page_objects/` - Page classes (LoginPage, CartPage, etc.) extending `PageBase`
- `api_objects/` - API endpoint classes (LoginApi, CreateOrderApi, etc.) extending `ApiBase`
- **Convention**: Locators as class variables using `(By.*, selector)` tuples; methods encapsulate user interactions

### 3. **Base Classes & Utils** (`utils/`)
- **`PageBase`**: Wraps Selenium with 20s WebDriverWait, provides `find_element()`, `scroll_down()`, JWT token manipulation via `localStorage`
- **`ApiBase`**: Wraps requests.Session, logs all request/response details, handles JSON payloads
- **`db_utils.py`**: `query_method()` helper for DictCursor queries with logging

## Critical Workflows

### Running Tests
```bash
# Single test
pytest tests_api/test_login_api.py::TestLogin::test_login_success -v

# Parallel execution (2 workers) with retry + Allure reporting
pytest -n 2 --reruns 1 tests_api/ tests_web/

# Generate Allure HTML report
allure generate ./allure-results/ -o ./allure-report/ --clean

# Full pipeline (see exec_test.sh)
python3 -m venv myenv && source myenv/bin/activate && pip3 install -r requirements.txt
pytest -n 2 --reruns 1 && allure generate ./allure-results/ -o ./allure-report/ --clean
```

**Parallel Worker Assignment** (in `tests_web/conftest.py`):
- `gw0` → `USER_NAME_1`
- `gw1` → `USER_NAME_2`
- Other workers → `USER_NAME_1` (fallback)

### Environment Configuration
- Root `.env` or ENV-specified file loaded via `conftest.py:load_dotenv()`
- **Required vars**: `BASE_URL`, `DOMAIN`, `DB_HOST`, `DB_PORT`, `DB_USERNAME`, `DB_PASSWORD`, `DB_NAME`, `USER_NAME_1`, `USER_NAME_2`, `PASSWORD`
- Tests read config at runtime: `os.getenv("VAR_NAME")`

### Database Integration
- Session-scoped fixture `setup_db` in root `conftest.py` provides PyMySQL connection
- Accessed in tests via `setup_db` parameter
- **Pattern** (see `test_login_api.py`): Validate API responses against DB queries using `query_method()`
- Example: `search_user_info(email, setup_db)` from `table_object/user_table.py`

## Key Patterns & Conventions

### Page Object Pattern
```python
# Locators as class attributes
class LoginPage(PageBase):
    input_email = (By.ID, "email")
    btn_login = (By.XPATH, "//button[text()='Login']")
    
    def login(self, email, password):
        self.find_element(self.input_email).send_keys(email)  # Implicit wait + clickable
        self.find_element(self.btn_login).click()
```
- Use `find_element(locator, clickable=True/False)` for visibility or interactability waits
- JWT token stored in `localStorage` - accessible via `get_jwt_token()`, modifiable via `set_jwt_token(token)`

### API Object Pattern
```python
# Inherit from ApiBase, set URL in __init__
class LoginApi(ApiBase):
    def __init__(self, session, email, password):
        url = f"{os.getenv('BASE_URL')}/user/login"
        super().__init__(session, url)
        self.payload = {...}
    
    def send(self):
        response = self.api_request("post", self.payload)
        if response.status_code == 200:
            self.session.headers["Authorization"] = f"Bearer {response.json()['data']['access_token']}"
        return response
```
- Logging includes full request/response body and headers
- Response object returned for assertion in tests

### Test Organization
- **Allure decorators**: `@allure.feature()`, `@allure.title()`, `@allure.step()` for reporting granularity
- **Parametrization**: `@pytest.mark.parametrize()` for data-driven tests
- **Fixtures**: Request-scoped for resources, session-scoped for DB connections
- **Assertions**: Direct `assert` statements; logging inside asserts for context

### Chrome Driver Setup (Web Tests)
```python
# tests_web/conftest.py: headless mode, 1920x1080 window, auto-managed via webdriver-manager
service = Service(executable_path=ChromeDriverManager().install())
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=options)
```
- Screenshots auto-attached post-test to Allure report

## Cross-Component Communication

### API → Database Validation
1. API test calls endpoint via `LoginApi().send()`
2. Validates response: `assert response.status_code == 200`
3. Queries DB with `setup_db` fixture: `search_user_info(email, setup_db)`
4. Cross-validates API response fields vs DB row values

### Web → API (Token Reuse)
- UI tests can extract JWT from localStorage and pass to API tests
- `PageBase.get_jwt_token()` returns token; set in API session headers for subsequent calls

### Configuration Flow
- `conftest.py` loads `.env` at test collection time
- Variables propagated to API objects (URL construction), Web tests (domain), and DB fixtures
- Override via pytest ENV variable: `pytest --env=.env-staging`

## Important File References
- **Entry**: `conftest.py` (root), `tests_api/conftest.py`, `tests_web/conftest.py`
- **Infrastructure**: `utils/page_base.py`, `utils/api_utils.py`, `db_utilis/db_utils.py`
- **Reporting**: `pytest.ini` (Allure auto-clean), `exec_test.sh` (pipeline)
- **Data Models**: `table_object/` (DB schemas), `test_data/` (test datasets)

## Common Tasks for AI Agents

1. **Add New API Test**: Create `tests_api/test_*.py`, define fixture-based test using LoginApi pattern
2. **Add Web Test**: Create `tests_web/test_web_*.py`, use PageBase and Selenium locators
3. **Add Database Validation**: Extend `table_object/` with new `search_*()` functions; call from test via `setup_db`
4. **Debug Failed Test**: Check `allure-results/*.json` for attachments; review logs in pytest output
5. **Parallelize**: Assign worker IDs in `conftest.py` if adding new fixtures; ensure thread-safety on shared resources


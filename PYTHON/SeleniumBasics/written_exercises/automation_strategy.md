# Hands-On 3 - Automation Strategy and Frameworks

## 1. Automation decision criteria

| Criterion | Why it matters | POST course test assessment |
|---|---|---|
| Repeatability | Frequent execution yields savings. | Strong candidate: run on every build/regression cycle. |
| Business risk | High-impact functions deserve reliable regression coverage. | Strong candidate: course creation is a core workflow. |
| Stable behaviour | Stable requirements reduce maintenance. | Good candidate once payload schema/status codes are agreed. |
| Deterministic result | Predictable data and output reduce flaky results. | Good candidate using a unique generated course code and isolated test database. |
| Automation feasibility | APIs are fast, observable, and cheaper to automate than UI flows. | Excellent candidate: assert HTTP status, schema, and persisted data directly. |

## 2. Automate or manual

| Test case | Decision | Reason |
|---|---|---|
| CRUD regression after every change | Automate | Repetitive, high-value, stable, and required frequently. |
| Exploratory test of new search | Manual | Human curiosity and adaptation are central while the feature changes. |
| 100 concurrent GET users | Automate | A load-testing tool can repeat the scenario accurately and measure timings. |
| Login form UI test | Automate | Critical regression path; keep a small stable UI smoke set. |
| Swagger documentation accuracy | Manual | Review language and examples manually, supplemented by automated OpenAPI contract checks. |
| Post-deployment API reachability smoke test | Automate | Fast, repeatable release gate with immediate feedback. |

## 3. Automation ROI

Automation ROI compares the benefit saved by automated execution with the cost of creating and maintaining it. A manual run costs 30 minutes. Automation costs 4 hours (240 minutes), so the break-even point without maintenance is `240 / 30 = 8` runs.

After the tenth run, assume each automated run has 20% of the manual-run cost as maintenance: 6 minutes. Each later run still saves 24 minutes. The automation has already paid for itself at run 8; by run 10 it has saved 60 minutes net, and maintenance reduces—but does not remove—the ongoing benefit.

## 4. Flaky tests

A flaky test gives different results without a relevant application change. Example: a Selenium alert test clicks a button and immediately asserts alert text; it fails on a slow CI machine because rendering has not completed. Prevent or fix it by (1) using explicit waits for a concrete condition, (2) using stable unique locators and isolated test data, and (3) removing shared state, arbitrary sleeps, and timing-sensitive dependencies while collecting failure screenshots/logs.

## 5. Framework comparison

| Type | Description | Advantage | Disadvantage | Course Management use |
|---|---|---|---|---|
| Linear | Test steps are written sequentially in one script. | Fast to start. | Duplication and fragile maintenance. | One temporary proof-of-concept course-creation flow. |
| Modular | Common actions are separated into reusable modules/page objects. | Reuse and localized maintenance. | Needs design discipline. | Reuse login and course form interactions. |
| Data-driven | Test logic is separated from data such as CSV/JSON/fixtures. | Broad coverage with one test flow. | Data management adds complexity. | Exercise valid/invalid course payloads and 50 login credentials. |
| Keyword-driven | Tests use business keywords that map to automation actions. | Non-technical users can read/write scenarios. | Keyword libraries can become complex. | Let analysts compose `Login`, `Create Course`, and `Verify Course` workflows. |
| Hybrid | Combines modular, data-driven, and sometimes keyword-driven layers. | Flexible, scalable, and maintainable. | More initial architecture. | Full regression suite across frontend and API. |

## 6. Recommendation

Use a **hybrid framework**: Page Objects/modular helpers for the 20 reused login flows, parameterised data-driven tests for 50 credential combinations, and a small keyword/BDD layer for non-technical contributors. Developers maintain page objects and utilities while analysts contribute readable scenario data or Gherkin cases.

## 7. Hybrid framework structure

```text
SeleniumBasics/
  config/
    settings.py
  data/
    users.json
    courses.json
  pages/
    login_page.py
    course_page.py
  tests/
    test_login.py
    test_courses.py
  utilities/
    driver_factory.py
    waits.py
    data_loader.py
  conftest.py
  requirements.txt
```

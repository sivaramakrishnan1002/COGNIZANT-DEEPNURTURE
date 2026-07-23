# Hands-On 2 - SDLC, TDLC, V-Model and Agile QA

## 1. V-Model mapping

```text
Requirements                 Acceptance Testing
     \                         /
System Design              System Testing
       \                     /
Architecture Design     Integration Testing
         \                 /
Module Design          Unit Testing
           \           /
              Coding
```

| SDLC phase | Corresponding TDLC phase | Test artifact prepared during development |
|---|---|---|
| Requirements | Acceptance testing | Acceptance criteria, UAT scenarios, and requirements traceability matrix |
| System design | System testing | System test plan, end-to-end API flow tests, and non-functional test strategy |
| Architecture design | Integration testing | API contracts, integration test plan, and interface/data-flow test cases |
| Module design | Unit testing | Unit test design, branch/validation test cases, and mocks/stubs plan |
| Coding | All test execution | Executable unit tests and the build to be verified by the planned test levels |

## 2. Entry and exit criteria

| Test level | Entry criteria | Exit criteria |
|---|---|---|
| Unit | Module design is approved; code is built; unit test cases and mocks are ready. | Planned unit tests pass; target coverage is met; no open critical unit defects. |
| Integration | Units pass unit testing; API/database interfaces and test environment are available; contracts are agreed. | Planned interface tests execute; integrations exchange correct data; no open critical/high integration defects. |
| System | Integrated build is deployed to a stable test environment; system test data and requirements traceability are ready. | All planned system tests execute; essential flows pass; agreed defect threshold is met; no open critical/high defects. |
| Acceptance | System testing is complete; a release candidate and realistic user data are available; business acceptance criteria are approved. | College-admin scenarios pass; business owner approves; no release-blocking defects remain. |

QA should engage during **requirements review** to remove ambiguity from validations, status codes, and error responses, and during **architecture/API contract design** to review authentication, database failure handling, observability, and integration testability.

## 3. Waterfall problems

1. Defects in the course API contract are discovered after implementation, when changing endpoint and database code is expensive.
2. QA has little chance to clarify ambiguous requirements such as duplicate-course behaviour, leading to rework and disagreements.
3. A late test phase compresses regression testing before release, increasing the chance of escaped defects and delaying feedback to developers.

## 4. QA in Agile ceremonies

| Ceremony | QA contribution |
|---|---|
| Sprint Planning | Clarifies acceptance criteria, identifies risk, estimates testing work, and prepares test data/environment needs. |
| Daily Standup | Reports blocked testing, newly found defects, test progress, and dependencies that need team action. |
| Sprint Review | Verifies the demonstrable acceptance flows and helps show stakeholders what was tested. |
| Retrospective | Uses defect and test feedback to suggest improvements such as earlier reviews, better data, or stable environments. |

## 5. Shift-left practices applied to the API

1. **Review requirements for testability:** agree up front that invalid payloads return a documented 422 response and duplicate codes return 409.
2. **Write tests before code (TDD/BDD):** write the valid-course, duplicate-code, and missing-name scenarios before implementing `POST /api/courses/`.
3. **Static analysis:** run formatting, linting, type checks, and security scanning in pull requests to find errors before deployment.
4. **API contract testing:** validate the OpenAPI schema and consumer expectations before the frontend and backend are integrated.

## 6. Acceptance criteria - Gherkin

```gherkin
Scenario: College admin creates a course successfully
  Given I am an authenticated college admin
  And no course exists with code "SEL-101"
  When I create a course with code "SEL-101", name "Selenium Basics", and duration 20
  Then the API returns status 201
  And the response contains the created course with code "SEL-101"

Scenario: College admin cannot create a duplicate course code
  Given I am an authenticated college admin
  And a course already exists with code "SEL-101"
  When I create another course with code "SEL-101"
  Then the API returns a duplicate-code validation error
  And no additional course is created

Scenario: College admin cannot omit required fields
  Given I am an authenticated college admin
  When I create a course without a name or course code
  Then the API returns status 400 or 422
  And the response identifies each missing required field
```

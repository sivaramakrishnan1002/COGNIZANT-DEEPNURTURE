# Hands-On 1 - QA Concepts, Functional Testing and Defect Lifecycle

## 1. Testing types for the Course Management API

| Testing level | Concrete test case | Classification |
|---|---|---|
| Unit | Call `validate_course_payload()` with a valid code, name, and duration; verify that it returns the validated course object. | Functional |
| Integration | Send `POST /api/courses/` with valid JSON to the running API and verify that the endpoint stores the new course in the database. | Functional |
| System | Create a course through the API, retrieve it with `GET /api/courses/{id}`, update it, and then delete it; verify each HTTP response and final database state. | Functional |
| User acceptance | A college administrator creates “Selenium Basics” with code `SEL-101`, sees it in the course list, and can use it when enrolling a student. | Functional |

Non-functional example: run 100 concurrent `GET /api/courses/` requests and verify that at least 95% complete within 500 ms with no server errors. This measures performance and reliability rather than whether a feature returns the right data.

## 2. Black-box and white-box testing

Black-box testing checks externally observable behaviour using inputs, outputs, requirements, and API contracts without needing to know the implementation. For example, a QA engineer can send valid and invalid payloads to `POST /api/courses/` and verify the status codes and response schema.

White-box testing uses knowledge of source code, branches, database queries, and internal error handling. A developer can write tests that cover each branch in `validate_course_payload()` and each exception path in the repository layer. QA testers typically perform black-box testing, while developers typically perform white-box testing. Both approaches complement each other.

## 3. Formal test cases - `POST /api/courses/`

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|---|
| CM-POST-001 | Create a course with valid required data. | API is running; `SEL-101` does not exist. | 1. Send POST `/api/courses/` with `{ "code":"SEL-101", "name":"Selenium Basics", "duration":20 }`. 2. Read the response. | HTTP 201; response contains a generated ID and the submitted course values; course is persisted. |  |  |
| CM-POST-002 | Reject a request with a missing required name. | API is running. | 1. Send POST `/api/courses/` with `{ "code":"SEL-102", "duration":20 }`. 2. Read the response. | HTTP 400 or 422; response identifies `name` as required; no course is created. |  |  |
| CM-POST-003 | Reject a duplicate course code. | API is running; a course with code `SEL-101` already exists. | 1. Send POST `/api/courses/` with code `SEL-101` and a different name. 2. Read the response. | HTTP 409 or validation error; existing course is unchanged; no duplicate is stored. |  |  |

## 4. Defect lifecycle

`New -> Assigned -> Open -> Fixed -> Retest -> Verified -> Closed`

- **New:** QA records a reproducible issue.
- **Assigned:** A lead assigns it to the responsible developer.
- **Open:** The developer investigates and works on a correction.
- **Fixed:** The developer supplies a build containing the correction.
- **Retest:** QA repeats the documented steps on that build.
- **Verified:** QA confirms the expected behaviour and checks relevant regression risk.
- **Closed:** The verified defect is formally completed.
- **Rejected path:** the assignee can move a defect to Rejected when it is not reproducible, works as designed, is duplicated, or has insufficient information; QA can reopen it with evidence.
- **Deferred path:** the product owner can defer a valid defect to a later release because it is not currently worth the risk or effort; it returns to Assigned/Open when scheduled.

## 5. Severity and priority

| Bug | Severity | Priority | Justification |
|---|---|---|---|
| a. All POST requests return 500. | Critical | P1 | The core course-creation function is unavailable to every user and blocks business workflows. |
| b. Names over 150 characters are silently truncated. | High | P2 | Data is corrupted without warning. It needs prompt correction, but normal course creation still works. |
| c. Swagger description contains a typo. | Low | P4 | It is cosmetic and does not affect API behaviour. |
| d. Valid login intermittently returns 401. | High | P1 | Users can be locked out and the intermittent nature signals instability that is difficult to diagnose. |

## 6. Defect report

| Field | Value |
|---|---|
| Defect ID | CM-API-001 |
| Title | `POST /api/courses/` returns HTTP 500 for valid course creation requests |
| Environment | Windows 11, Python 3.12, Course Management API local test environment, SQLite database |
| Build Version | 1.0.0-test |
| Severity | Critical |
| Priority | P1 |
| Steps to Reproduce | 1. Start the API and database. 2. Send a POST request to `/api/courses/` with valid JSON: `{ "code":"SEL-101", "name":"Selenium Basics", "duration":20 }`. 3. Observe the HTTP response. |
| Expected Result | The API returns HTTP 201 and the saved course object. |
| Actual Result | The API returns HTTP 500 Internal Server Error; no course can be created. |
| Attachments | Screenshot of 500 error. |

## 7. Severity versus priority

Severity is the technical/business impact if the defect occurs; priority is how urgently the team should fix it. A rarely used legacy export endpoint that crashes only when a retired report format is requested can be High severity because it crashes, but P3 priority because no current customer uses it and a replacement is planned. Conversely, a spelling error on the CEO's live demonstration dashboard is Low severity but may be P1 priority before the demonstration.

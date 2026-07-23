# Selenium Basics - Complete Hands-On Submission

## Contents

- `written_exercises/`: completed Markdown submissions for Hands-On 1-3.
- `automation_scripts/`: standalone setup, locator, and wait examples for Hands-On 4-5.
- `pages/`: Page Object Model classes for Hands-On 7.
- `tests/`: six pytest cases: three parameterised message cases, checkbox, dropdown, and input form.
- `conftest.py`: headless Chrome fixture, base URL fixture, pass/failure screenshots, and failure hook.

## Run

```powershell
python -m pip install -r requirements.txt
pytest tests -v --html=report.html --self-contained-html
python automation_scripts/setup_test.py
```

Screenshots are saved using the existing project convention in `PYTHON/outputs/HANDSON 4` and `PYTHON/outputs/HANDSON 6`. The test files deliberately contain no `driver.find_element` calls; locators and browser actions belong to page objects.

## POM maintenance benefit

In a flat suite, changing a Submit button ID from `submit` to `btn-submit` would force changes throughout every test that directly located it, creating duplicated maintenance and missed updates. With POM, the locator is defined once in the relevant page class, so the change is isolated and test intent stays readable.

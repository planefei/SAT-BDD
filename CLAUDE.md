# CLAUDE.md — AI Assistant Guide for SAT-BDD

## Repository Overview

**Repository:** `planefei/SAT-BDD`
**Purpose:** Software Acceptance Testing using Behavior-Driven Development (BDD)
**Status:** Newly initialized repository — no source files are committed yet.

> This file is automatically maintained for AI coding assistants. Update it as the project evolves.

---

## Current State

This repository is **empty**. There are no tracked source files, no commits on any branch, and no dependency files. The remote is configured at:

```
http://local_proxy@127.0.0.1:29569/git/planefei/SAT-BDD
```

When the first code is added, update this document to reflect:
- The chosen language(s) and frameworks
- Directory structure
- Build and test commands
- CI/CD setup

---

## Project Intent

Based on the repository name (`SAT-BDD`), this project is expected to implement **Software Acceptance Testing** using **Behavior-Driven Development** practices. BDD bridges the communication gap between developers, testers, and business stakeholders by expressing requirements as human-readable scenarios.

Typical BDD stack options to consider when bootstrapping:

| Language   | BDD Framework          | Test Runner         |
|------------|------------------------|---------------------|
| Python     | `behave` / `pytest-bdd`| `pytest`            |
| JavaScript | `Cucumber.js`          | `jest` / `mocha`    |
| Java       | `Cucumber-JVM`         | `JUnit` / `TestNG`  |
| Ruby       | `RSpec` / `Cucumber`   | `RSpec`             |
| Go         | `godog`                | `go test`           |

---

## Expected Directory Structure (Template)

Once populated, the project is expected to follow a structure similar to:

```
SAT-BDD/
├── CLAUDE.md               # This file
├── README.md               # Human-facing project overview
├── features/               # BDD feature files (.feature)
│   ├── *.feature           # Gherkin scenarios
│   └── steps/              # Step definitions
├── src/                    # Application source code (if any)
├── tests/                  # Unit / integration tests
├── reports/                # Generated test reports (gitignored)
├── .github/
│   └── workflows/          # CI/CD pipelines
└── <config files>          # e.g., pyproject.toml, package.json, pom.xml
```

---

## BDD Conventions

### Gherkin Feature Files

- Use **Given / When / Then** structure consistently.
- Keep scenarios focused on **business behavior**, not implementation details.
- Use `Background:` for shared preconditions within a feature file.
- Use `Scenario Outline:` + `Examples:` for data-driven scenarios.
- Tag scenarios with `@tag` for filtering (e.g., `@smoke`, `@regression`, `@wip`).

```gherkin
@smoke
Feature: User login

  Background:
    Given the application is running

  Scenario: Successful login with valid credentials
    Given a user with username "alice" and password "secret"
    When the user submits the login form
    Then the user should be redirected to the dashboard

  Scenario Outline: Failed login with invalid credentials
    Given a user with username "<username>" and password "<password>"
    When the user submits the login form
    Then an error message "<message>" should be displayed

    Examples:
      | username | password | message               |
      | alice    | wrong    | Invalid credentials   |
      | unknown  | secret   | User does not exist   |
```

### Step Definitions

- Keep step definitions **thin** — delegate logic to page objects, services, or helpers.
- Reuse steps across feature files where possible.
- Avoid hardcoding test data inside step definitions; use parameters or fixtures.

---

## Git Workflow

### Branch Naming

```
feature/<short-description>
bugfix/<short-description>
chore/<short-description>
claude/<task-id>              # Branches created by AI assistants
```

### Commit Messages

Use imperative mood and keep the subject line under 72 characters:

```
Add login feature scenarios
Fix step definition for user registration
Refactor page object for checkout flow
```

For multi-line commits:

```
Add acceptance tests for payment flow

- Covers successful card payment
- Covers declined card scenario
- Uses Scenario Outline for multiple card types
```

### Pull Request Guidelines

- Link PRs to the relevant issue or task.
- Ensure all BDD scenarios pass before requesting review.
- Include a brief description of what behavior is being tested.

---

## Development Commands

> These are placeholders. Replace with actual commands once the stack is chosen.

```bash
# Install dependencies
<package-manager> install

# Run all BDD scenarios
<test-runner> run features/

# Run tagged scenarios only
<test-runner> run features/ --tags @smoke

# Generate HTML test report
<test-runner> run features/ --format html --out reports/report.html

# Lint feature files (if a linter is configured)
<linter> features/
```

---

## CI/CD

Once a CI pipeline is added (e.g., GitHub Actions), document:
- Trigger conditions (push, pull_request, schedule)
- Steps: checkout → install → lint → test → report
- Artifact upload for test reports

---

## AI Assistant Guidelines

When working in this repository, AI assistants should:

1. **Read this file first** before making changes to understand conventions.
2. **Update CLAUDE.md** when the project structure, commands, or conventions change significantly.
3. **Follow BDD principles**: keep feature files business-focused and step definitions implementation-agnostic.
4. **Prefer small, focused commits** — one logical change per commit.
5. **Never push directly to `main`** — always use a feature or `claude/` branch.
6. **Run tests before committing** — ensure all existing scenarios still pass after changes.
7. **Do not add unnecessary files** — avoid generated artifacts, IDE config files, and build output unless explicitly requested.
8. **Respect `.gitignore`** — do not force-add ignored files.

---

## Updating This File

This CLAUDE.md should be updated whenever:
- The tech stack or framework is chosen and set up
- New development scripts or commands are added
- Directory structure changes significantly
- New conventions or standards are adopted by the team

Last updated: 2026-03-05 (repository initialization)

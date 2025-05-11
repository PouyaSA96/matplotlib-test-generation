# Matplotlib Automated Test Generation Suite [Group 17] AdminTests (CSCI926/ S125)

A comprehensive test framework for generating, organizing, and running over 2,500 automated test cases against the Matplotlib library. Combines hand-crafted Python unit tests (with pytest & Hypothesis) and JavaScript gallery validations (with Puppeteer).

---

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)
   - [Run Python Tests](#run-python-tests)
   - [Run JS Gallery Tests](#run-js-gallery-tests)
5. [Configuration](#configuration)
---

## Features

- **2,500+ Test Cases** covering edge cases, property combinations, fuzz inputs, smoke tests, and gallery validations.
- **Python Suite**: Hand-crafted and Hypothesis-powered tests invoking Matplotlib’s API (`pytest`).
- **JavaScript Suite**: Puppeteer scripts that validate official gallery pages for expected titles, images, and load status.
- **Sequential & Isolated Runs**: Tests designed to execute in order, with clear reporting of failures.
- **Bug Tracing**: Failures are mapped back to Matplotlib issue tracker entries and source locations.

---


## Prerequisites

- **Python 3.8+**
- **Node.js 14+** (with npm)
- **Chromium** (bundled with Puppeteer)

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/matplotlib-test-suite.git
   cd matplotlib-test-suite
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install JS dependencies**
   ```bash
   cd js
   npm install puppeteer
   cd ..
   ```

---

## Usage

### Run Python Tests

From the project root:
```bash
pytest python/tests -q --maxfail=1 --disable-warnings
```

- Use `-q` for quiet output.
- `--maxfail=1` stops on first failure (adjust as needed).

### Run JS Gallery Tests

```bash
node js/puppeteer-test.js
```

- Validates gallery pages in headless Chromium.
- Reports missing titles, images, and HTTP errors.

---

## Configuration

- **Hypothesis** settings (e.g., `max_examples`) can be tuned in each test file’s decorator.
- **Gallery URLs** for Puppeteer live in `js/puppeteer-test.js`—add or remove entries as needed.

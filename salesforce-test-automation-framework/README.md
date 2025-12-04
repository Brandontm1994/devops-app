# Salesforce Test Automation Framework

This framework provides a complete UI automation toolkit purpose-built for Salesforce Lightning.

## 🚀 Features

### Salesforce-Specific Selenium UI Recorder  
Captures clicks, inputs, waits, and dynamic interactions with LWC and Aura components.  
Designed for Salesforce’s evolving DOM structure and event model.

### Dynamic Locator Engine  
Handles:
- Shadow DOM traversal  
- Dynamic Salesforce component IDs  
- LWC rendering patterns and repeated regions  
- Aura class parsing  
- Modal dialogs, picklists, and lookup components  
- `aria-*` attributes as locator fallbacks  

### YAML-Based Test Runner  
Declarative test definitions that are executed through the CLI using Selenium.

### Shadow DOM Support  
Required for automating modern Lightning DOM structures that wrap key components in shadow roots.

### CLI Tools Included
- `sf-recorder` — launches the Salesforce UI Recorder  
- `sf-run` — executes YAML test suites  

---

## 📁 Project Structure
```
salesforce_autotest/
    recorder/
    locators/
    runner/
    utils/
    config/
scripts/
pyproject.toml
setup.cfg
README.md
LICENSE
```

---

## 🧩 Requirements
- Python 3.10+
- Selenium 4.x
- Chrome or Chromium WebDriver installed and accessible in PATH

---

## 🛠 Installation
```
pip install .
```

---

## ▶ Running the Recorder GUI
```
sf-recorder
```

---

## ▶ Running Automated Tests
```
sf-run tests/example.yaml
```

---

## 📄 License
MIT License — free for internal use and modification.

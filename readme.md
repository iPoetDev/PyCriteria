# Project Criteria

## 1.0 [Introduction](#introduction)

<!-- todo #1: add link-->
[Live App Here]( "No Link: Add Heroku URI")

<!-- todo #2: add image link-->
![AddScreenshot]()

## 2.0 [Plan](#plan)

### 2.1 [User Experience](#ux)

### 2.2 [Audiences](#audiences)

### 2.3 [Requirements](#requirements)

## 3.0 [Design](#design)

### 3.1 [Business Logic](#business)

### 3.2 [Application Context](#app-context)

> LO: State Diagram, Activity Diagram

### 3.3 [Data Flow](#data-flow)

> LO: Flowcharts
>

### 3.4 [User Journey](#user-journey)

> LO: Flowcharts, Activity Diagram

## 4.0 [Build](#build)

### 4.1 [Environment](#enviornment)

#### 4.1.1 Interpreter

- Python 3.xx.xx
    - Local: Installed
    - Remotely:
    - Deployed:

#### 4.1.2 Isolation

- Venv:
- Docker:

#### 4.1.3 Infra Packages

- Pip
- Setuptools
-

### 4.2 [IDE/CDE](#ide-cde)

- PyCharm (Education) 2023.03

#### 4.2.1 [Plugins](#plugins)

- CodeStream
- Synk
- MyPy,
- PyLint
- PyCrunch
- Sourcery
- Gherkin, Cucumber+
- TODO
- Toolset

### 4.3 [3rd Party Libraries](#3party)

> Frameworks Used: Programs, packages, libraries used in workflows, and in the app code.

### 4.4 [3rd Party Tools]()#3party-tools)

- Mermaid
- Draw.io

### 4.1 [Repository](#repository)

## 5.0 [Code](#code)

### 5.1 [Features](#constructs)

> LO

### 5.2 [Code Patterns](#codepatterns)

## 6.0 [Reliability](#qa)

### 6.1 [Testing & Validation](#testing)

### 6.3 [Static Analysis](#static)

### 6.3.1 [Code Quality](#quality)

#### 6.3.1.1 Ruff

> See `.pyproject.toml` for configuration and evaluation of configuration.

- **Summary**
    - `ruff check .` when in the root of the project,
    - run via the terminal and after `venv/Scripts/activate.ps1` is activared
    - Ruff mirrors Flake8's rule code system, in which each rule code consists of a one-to-three letter prefix, followed
      by
      three digits

- **Possible Linters**: [Ruff Rule](https://beta.ruff.rs/docs/rules/)
  `ruff linter` from the terminal in the root of the project.
  > Ruff supports over 500 lint rules, many of which are inspired by popular
  > ... tools like Flake8, isort, pyupgrade, and others. Regardless of the rule's origin,
  > ... Ruff re-implements every rule in Rust as a first-party feature.

 ````
  PS D:\Code\Code Institute\PyCriteria> ruff linter          
   F Pyflakes   
 E/W pycodestyle
 C90 mccabe
   I isort
   N pep8-naming
   D pydocstyle
  UP pyupgrade
 YTT flake8-2020
 ANN flake8-annotations
   S flake8-bandit
 BLE flake8-blind-except
 FBT flake8-boolean-trap
   B flake8-bugbear
   A flake8-builtins
 COM flake8-commas
  C4 flake8-comprehensions
 DTZ flake8-datetimez
 T10 flake8-debugger
  DJ flake8-django
  EM flake8-errmsg
 EXE flake8-executable
 ISC flake8-implicit-str-concat
 ICN flake8-import-conventions
   G flake8-logging-format
 INP flake8-no-pep420
 PIE flake8-pie
 T20 flake8-print
 PYI flake8-pyi
  PT flake8-pytest-style
   Q flake8-quotes
 RSE flake8-raise
 RET flake8-return
 SLF flake8-self
 SIM flake8-simplify
 TID flake8-tidy-imports
 TCH flake8-type-checking
 INT flake8-gettext
 ARG flake8-unused-arguments
 PTH flake8-use-pathlib
 ERA eradicate
  PD pandas-vet
 PGH pygrep-hooks
  PL Pylint
 TRY tryceratops
 NPY NumPy-specific rules
 RUF Ruff-specific rules

 ````

#### 6.3.1.2 Pylint

> Native into PyCharm so this is the defact problem matcher for the IDE.

## 7.0 [Deploy](#deploy)

### 7.1 [Features](#features)

### 7.2 [DoD](#done)

> See [Definition of Done](_docs/done.md)

### 7.3 [Deployment](#deployment)

- .
- .
- .
- .

#### 7.3.1 Repository Service

- [Github.com](https://www.github.com) is the chosen remote code repository service being used.
  
      User | Profile | Repo | Link | Visibility | Issues

----------:| :--- | :--- | :--- |:--- |:---
@iPoetDev | @iPoetDev | PyCriteria |   https://github.com/iPoetDev/terni-lapilli--toe  | Public | Issues

#### 7.3.2 Local Git Service / IDE

- VSCode configured with Github account for Local development environment.
- VSCode extension: Gitlens installed and enabled for local development and deployment.
- Utilized a Changelog format to document the changes, a la, Keep a Changelog.
    - Intent here was to catalogue in longer more human readable format a more contextual change history.
    - Greater than the 50 chars of a commit 1st line.
    - Additionally, utilized the changelog as a summation effort to shorted and be precise on the commit description.
- Mostly adhered to Semantic Versioning approach.
    - Minor adjustment was to put a double digit index for each separate commit if several occurred on one day.

#### 7.3.3 Deployment Environment

- Heroku is the cloud environment to deploy too:
- Deploy a static web page off every commit.
- Once the commit is built, then deploy the new website and pushes to hosted domain URI.
-
- Heroku is the hosted domain URI and service.
- The final URI is
  
  ```

## 8.0 [Assessment](#assessment)

### 8.1 [Author](#author)

### 8.2 [Credits](#credits)

### 8.2.1 [Guides](#guides)

> Articles | Tutorials | Resources | Books

### 8.2.2 [Videos](#videos)

> YouTube | Online 

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

> Integrated into PyCharm, so this is the defacto problem matcher for the IDE.
> Disabled: `pylint: disable=` in the codebas hint at non-criticla or intentional hotspots

*File* |   Date   |       LN       |        Issue        | Code  |  State   | Note
-----:|:--------:|:--------------:|:-------------------:|:-----:|:--------:|:-----
All | OnGoing  |       2        | trailing-whitespace | C0303 | disabled | Non Critical
controller.py | 23-05-05 | 90,104,228,234 |  unnecessary-pass   | C0114 | disabled | Temporary
settings.py | 23-05-05 |     26-42      |    invalid-name     | C0103 | disabled | Using custom convention <br> Using upper case to flag program variables<br> Setting CONSTANTS
settings.py | 23-05-05 |     19,49      |    too-few-public-methods     | R0903 | disabled | Setting Classes
settings.py | 23-05-05 |     19,49      |    too-many-instance-attributes     | R0902 | disabled | Setting Classes
connection.py | 23-05-05 |     26-36      |    invalid-name     | C0103  | disabled | as per settings.py, CONSTANTS

#### 6.3.1.3 SonarLint

> Integrated into PyCharm, by 3rd Party Plugin

*File* |   Date    |    LN    |          Issue          |     Code     |   State    | Note
-----:|:---------:|:--------:|:-----------------------:|:------------:|:----------:|:-----
datatransform.py | 2023-0505 |    83    |     unused variable     | python:S1481 | code-smell | WIP, Implementing
datatransform.py | 2023-0505 | 221, 229 | grouping regex patterns | python:S1481 | major-bug  | FixMe

Remove the unused local variable "maxrow".

#### 6.3.1.4 MyPy

***Status***

Date |  Status 
-----:|:---------: 
2023.05.05 | Passing

> Integrated into PyCharm, by 3rd Party Plugin:
> Invoke: ``dmypy run -- --check-untyped-defs --follow-imports=error --exclude /venv/ .``

File |   Date    | LN | Issue | Fix   |  State  | Note
-----------------:|:---------:|:--:|:-----:|:-----:|:-------:|:---
`datatransform.py` | 23-05-05  | 7 | import | added: ignore | Passing | https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
`datatransform.py` | 23-05-05  | 8 | import | added: ignore | Passing | (Using --follow-imports=error, module not passed on command line)
`datatransform.py` | 23-05-05  | 110 | return-value | added typing._SpecialForm | Passing | --
`projectlogging.py` | 23-05-05  | 97 | return-value | changed datastructure type | Passing | --
`run.py` | 23-05-05  | 40 | misc | removed implict/wrong return | Passing | --
`settings.pg` | 23-05-05  | 1 | assignment | changed type assign | Passing | --

## 7.0 [Deploy](#deploy)

### 7.1 [Features](#features)

### 7.2 [DoD](#done)

> See [Definition of Done](_docs/done.md)

### 7.3 [Deployment](#deployment)

### 7.3.0 Build and Deploy Status Log

PR | Year | Date | Time | Build | Time | Deploy | Overall Status | Method | Pipeline | Name
----:|:----:|:-----:|:---:|:-----:|:---:|:---:|:------:|:----:|:----|:----:|:----
#1 -v3| 2023| 05-02 | 10:50 | Passing | 10:51 | v3 Failing | Not Ok | Automated | Staging | deploy-auto
#2 | 2023| 05-0x | - | --- | - | --- | Ok | Manual/Automated | - | -

> #2 | 2023| 05-0x | --- | --- | Ok | Manual/Automated

#### 7.3.1 [Heroku Create App](#heroku)

- 1: Login to Heroku, and verify and MFA authenticate
- 2: Create a new app.
  ![](.docs/deployment/create-heroku-app.png)
- 3: Choose a deployment method. ``GitHub``
  ![](.docs/deployment/choose-deployment-method.png)
- 4: Connect to GitHub and search for the repository: ``PyCriteria``
  ![](.docs/deployment/connect-to-github.png)
- 5: Connect to chosen Repository and verify
  ![](.docs/deployment/connect-to-github-2.png)
  ![](.docs/deployment/select-app-repository.png)
- NOTE: ___ADR Decision___: Decide the selection of the branch to deploy to:
    - Decision: ``heroku``, as a protected branch
        - Use **Trunk based development** from the ``main`` branch to ``heroku`` branch
        - Commmit Style: Push to ``main`` for development codebase.
        - Tag Code ready for deployment: Push to ``heroku``
        - Deloyment is automated via Heroku's app deployment
        - By not having automated deployment on ```main```, there is no failed deployment
          noise on ``main`` branch and in the logs.
- 6: Add Buildpacks in correct order, as order sensitive, for good first run
    - Use built-in buildpacks for Node.js and Python
        - 1st: `heroku/nodejs`
        - 2nd: `heroku/python`
- 7: Config Vars
- 8: Deploy to Heroku by PullRequest
  ![](.docs/deployment/deploy-auto-heroku.png)
- 9:

#### 7.3.1.1 App Information

Name | Region | Stack | Framework | Slug Size | ConfigVars | Buildpacks | SSL Certs | Repo | Local Git
------------:|:-------|:----------|:----------|:-----------|:-----------|:--------------|:----------|:--------------------|:--------
py-criteria | Europe | heroku-22 | Python | 30/500 MiB | In Use | heroku/python | None |
iPoetDev/PyCriteria |https://git.heroku.com/py-criteria.git

#### 7.3.2 Heroku Branch Deployment

1. Pull Request from ``main`` to ``heroku`` branch for deployment
2. Protect ``heroku`` branch from changes or having anything pushed
3. Merge from ``main`` to ``heroku`` branch for each release
4. From `raw/new code` -> `linted code` -> `manually tested` -> `locally running` -> `PR#1` -> `Merge to Heroku` ->
   `Heroku Automated`

**A1: Heroku Release Flow**

```mermaid
flowchart LR
	A[Raw Code] --> B[Linted Code]
	B --> C[Manually Tested]
	C --> D[Locally running]
	D --> E[PR#1: Pull Request to Heroku]
	E --> F[Merge to Heroku]
	F --> G[Heroku Automated]
```

**A2: Heroku Commit Flow**

```mermaid
gitGraph:
	commit id: "Raw Code"
	commit id: "Linted Code"
	commit id: "Manually Tested"
	commit id: "Locally running"
	commit id: "#2 Create PR#1"
	commit id: "#1 Merge to Heroku"
	branch heroku-1
	commit id: "#1 Heroku automated"
	checkout main
	commit id: "New raw Code"
	commit id: "..."
	commit id: "#2 Create PR#2"
	commit id: "#2 Merge to Herokus"
	branch heroku-2
	commit id: "#2 Heroku Automated"
```

#### 7.3.2.1 Heroku Deployments

- Must have buildpacks installed in correct order
    1. `heroku/nodejs`
    2. `heroku/python`
- The heroku CLI `remove` buildpack option, along with the immediate re-install, needs further investifation as it
  failed
  > - Maybe due to `git push heroku main` not being invoked.
  > - Not sure which main it was referring to:
      >
    - Was it a main branch on @ipoetdev...pycriteria.git
  > - Or the remote heroku git.)

#### 7.3.2.2 Heroku CLI Logs

> CLI Documentation: [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

```bash
heroku logs --app=py-criteria --tail
```

Other useful runners

```bash
heroku option --app=py-criteria arguement
```

#### 7.3.3 Repository Service

- [GitHub.com](https://www.github.com) is the chosen remote code repository service being used.

User | Profile | Repo | Link                                   | Visibility | Issues
----------:| :--- | :--- |:---------------------------------------|:--- |:---
@iPoetDev | @iPoetDev | PyCriteria | https://github.com/iPoetDev/PyCriteria | Public | Issues

#### 7.3.5 Local Git Service / IDE ✅

- PyCharm configured with GitHub account for Local development environment.
- Utilised a modified/reduced Changelog format to document the changes, a-la, Keep a Changelog.
    - Directly in the commit messages.
    - Reduced efforts by not maintaining the ``changelog.md``, which is abandoned.
- Mostly adhered to Semantic Versioning approach.
    - Minor adjustment was to put a double-digit index for each separate commit if several occurred on one day.

#### 7.3.6 Deployment Environment ✅

- Heroku is the cloud environment to deploy too:
- Deploy a static web page off every commit.
- Once the commit is built, then deploy the new website and pushes to hosted domain URI.
- Heroku is the hosted domain URI and service.
- The final URI is
    - Plain Text:
      ``` https://py-criteria.herokuapp.com/ ```
    - Link: [https://py-criteria.herokuapp.com/](https://py-criteria.herokuapp.com/ "PyCriteria: https://py-criteria.
      herokuapp.com/")

## 8.0 [Assessment](#assessment)

### 8.1 [Author](#author)

### 8.2 [Credits](#credits)

### 8.2.1 [Guides](#guides)

> Articles | Tutorials | Resources | Books

### 8.2.2 [Videos](#videos)

> YouTube | Online 

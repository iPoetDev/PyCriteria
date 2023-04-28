---
name: Herouko Deployment Steps
about: SOP: Deployment to Heroku and Troubleshooting
title: "[HEROKU]: [DEPLOY]"
labels:
assignees: ipoetdev
---

# Heroku Deployment

1. SOP for App Deployment
2. Requirements Checklist

## SOP for App Deployment

### Access

- [x] Heroku Account and MFA: Configured: @2023.04.18
- [x] Student Developer Pack: Enabled|Connected: @2023.04.18
- [x] Heroku EcoDyno Subscribed: Enabled: @2023.04.20

### Config

- [ ] Github - Heroku Config:
    - .
- [x] Heroku Procfile: Defined
    - [ ] Procfile: single line command: is correct?
    - [ ] Procfile: is committed correctly to Github?
- [ ] Heroku ConfigVars:
    - [ ] ConfigVars: Is well formatted/linted correctly?
    - [ ] ConfigVars: Has right values?
    - [ ] ConfigVars: Checked the Dashboard, for Python?
    - [ ] ConfigVars: Is encrypted/correct authorisation?
    - [ ] ConfigVars: Is `PORT` correctly set correctly to `8000`?
    - [ ] ConfigVars: If credentails, then:
        - [ ] Config: `CREDS`  configvar?
        - [ ] Config: Add JSON to value field
- [ ] Heroku BuildPacks: Are these enabled, in the following order?
    - [ ] .1. `Heroku/python`
    - [ ] .2. `Heroku/nodejs`
- [ ] Heroku Deploy:
    - [ ] Is deployment on heroku manual pull
    - [ ] Is deployment on heroku automatic sync?
- [ ] Python Config:
    - [ ] Run.py: Is the code correct in this entry point?
    - [ ] Runtime.txt: Is this version of the python runtime provided for a correct version/available version per
      buildpack?
    - [ ] Requirements.txt: Has `pip update` been updated?
    - [ ] Requirements.txt: Has `pip freeze` been run?
        - Have these requirements been split into dev and production variants?
    - [ ] Is the remote environment activated/has slug worked?
    - [ ] Other: Do not edit any other files

### Requirements

- [ ] Node: Config: PTY:
    - Deployment Terminal is 80 columns, by 24 rows
    - Package.json
- [x] HTML/Web Views folder. _Given as part of the template._
    - `Index.html`:
        - Body fragment placeholder
        - Terminal Script: Inline
    - `Layout.html`:
        - Page template with @{body} JQuery tag.
        - Page CSS Styling: Inline
- [x] JavaScript Framework: _Given as part of the template._
    - `JQuery`: [Github Releases](https://github.com/jquery/jquery/releases) | [CDNJS JQuery](https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js) |
      [Release Notes](https://blog.jquery.com/2016/09/22/jquery-3-1-1-released/)
    - `XTerm.js`: [GitHub](https://github.com/xtermjs/xterm.js) | [CDNJS: Xterm.js](https://cdnjs.cloudflare.com/ajax/libs/xterm/3.14.5/xterm.min.js)
- [x] Terminal: _Given as part of the template._
    - New terminal: Run on reload of page
    - New terminal: Replace HTTPS to WS
    - New terminal: Add Hostname
    - New terminal: Add Port
    - New terminal: Attach terminal to websocket connection
    - New terminal: Error: Log to console
    - New terminal: Focus on a Terminal window
- [ ] Network: WebSocket
    - [x] Network: Socket: Raw
    - [x] Network: encoded: false
    - [x] Network: autodestroy: true
    - [x] Network: Client:
        - Spawn: `python3`, `run.py`
        - Cols: 80
        - Rows: 24
        - CWD: PWD
        - ENV: process.env
    - [x] Network: States
        - Spawn
        - Exit: Close and Kill process
        - OnData: Send
        - Close: Kill and Unload
        - Message: Test connection and send message
        - Writes: Creds to File, or Error on emit
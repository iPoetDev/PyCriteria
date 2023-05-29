# Design

## Commands

- File: `app.py`
- Arcitecture: Nested (grouped) command structure
- Runs in own REPL: `register_repl(cli)`

| File | Figure | Command    | Parent | Role                                                                                                      | Option    | Type | Callback | Help | Prompt | Required | Default |
| :--- |:-------|:-----------|:-------|:----------------------------------------------------------------------------------------------------------|:----------| :--- | :------- | :--- |:-------|:---------| :------ |
| `app.py` | `---`   | `run`      | None   | **Base** <br> Anchors nested commands                                                                     | `---`     | `---`   | `---` |  | `---`  | `---`         | `---`| 
| `app.py` | `---`   | `clear`    | Run    | Clears the click REPL stdout                                                                              | `---`     | `---`   | `---` |  | `---`  | `---`         | `---`|
| `app.py` | `---`   | `load`     | Run    | **Intent**<br> Displays the Load Mode Guide                                                               | `---`     | `---`   | `---` |  | `---`| `---`         | `---`|
| `app.py` | `---`   | `find`     | Run    | **Intent**<br> Displays the Find Mode Guide                                                               | `---`     | `---`   | `---` |  | `---`| `---`         | `---`|
| `app.py` | `---`   | `locate`   | Find    | Toggles the progress and DoD fields                                                                       | `---`     | `---`   | `---` |  | `---`| `---`         | `---`|
| `app.py` | `---`   | `edit`     | Run    | **Intent**<br> Displays the Edit Mode Guide                                                               | `---`     | `---`   | `---` |  | `---`| `---`         | `---`|
| `app.py` | `---`   | `note`     | Edit   | **Action**<br>Modifies the note fields <br> Add => Insert Note <br> Update => Append <br> Delete -> Clear | see table  | `---`   | `---` |  | `---`| `---`         | `---`|
| `app.py` | `---`   | `progress` | Edit   | **Action** Toggles the status of progress and DoD fields                                                     | see table | `---`   | `---` |  | `---`| `---`         | `---`|

### Run commands

#### Clear command

### Load commands

| File | Figure | Parent | Command | Option | Help | Values                  
| Type | Callback | Help | Prompt | Required | Default | Show Default
| :--- | |:-------|:-------|:---------|:-------|:--------------------------------------------|:---------------------------------------------|:------------------------|:---------|:-----|:-------|:---------| :------ | :------ |
| `app.py` | `---`   | `run`  | `load`   | `---`  | **Intent
**<br> Displays the Load Mode Guide | `---`| `---`                   | `---`    | | `---`| `---`         | `---`||
| `app.py` | `---`   | `load` | `todo`   | `---`  | **Actcion**<br>                             | `---`              
| `---`                   | `---`    | | `---`| `---`         | `---`||
| `app.py` | `---`   | | `todo`   | selects | **Option**<br>      | All<br>
Simple<br>Notes<br>Grade<br>Reference | Click.Choice(list[str]) | `---`    | | `---`| `---`         | `---`||

#### Todo command

#### View command

### Find command

#### Locate command

###

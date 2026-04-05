# GEDCOM-stats

Parses GEDCOM files and outputs some stats

# Project is yet to be finished, it isn't even in the Alpha stage.
## It already does a few cool things but is very limited and the instructions on how to use it are not done yet too.
## Also it is partially in English (developer information and config) and partially in Russian (results). In future it will be fully available in both languages.

## How to install

Make `input` folder in the root folder of the project.
Put your GEDCOM files in `input` folder.

## How to config

Put config.json in the root folder of the project.

### `input`: settings of GEDCOM file reading and parsing

`file`:             REQUIRED,           input GEDCOM file name
`tree_debug_mode`:  `true` by default,  outputs issues found with records in the tree
`developer_mode`:   `false` by default, outputs some debug information useful for the creator of the project

### `root`: information about the root person (the person whose tree it is, most likely you)

At least one of the following fields should be specified
`name`:             OPTIONAL,           name of the root person
`surname`:          OPTIONAL,           surname of the root person

### `stats`: information

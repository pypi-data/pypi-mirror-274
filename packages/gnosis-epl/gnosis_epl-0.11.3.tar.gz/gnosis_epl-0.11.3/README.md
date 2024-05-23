# Gnosis EPL Grammar

## Installing Dependencies

### Using pipenv
Run `$ pipenv shell` to create a python virtualenv and load the .env into the environment variables in the shell.

Then run: `$ pipenv install` to install all packages, or `$ pipenv install -d` to also install the packages that help during development, eg: ipython.
This runs the installation using **pip** under the hood, but also handle the cross dependency issues between packages and checks the packages MD5s for security measure.


### Using pip
To install from the `requirements.txt` file, run the following command:
```
$ pip install -r requirements.txt
```

## Rebuilding Grammar (ANTRL-4)
### Java and ANTRL-4 Jar Dependencies
If you need to re-generate the automatic grammar files created from ANTLR4. Otherwise, you can ignore this dependency.

If indeed you need to recreate the grammar files, then you'll need Java installed (tested with version 11.0.7 OpenJDK).
Afterwards, execute the command:
```
$ ./get_antlr.sh
```
which will download the jar file to `tools/antlr/antlr-4.8-complete.jar`

### Using ANTLR-4 to update grammar files
execute:
```
$ ./gen_antrl_files.sh
```
This will recreate the .py files and copy(override) the ones in the `grammar` module with this newly created ones.



## Examples of Queries

## Usage example


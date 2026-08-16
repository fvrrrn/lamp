# Create .db file with schema v1:
```bash
python -c "import sqlite3; sqlite3.connect('01.db').executescript(open('01_init.sql').read())"
```

# Create .db file with schema v2:
```bash
python -c "import sqlite3; sqlite3.connect('02.db').executescript(open('02_init.sql').read())"
```

# Open REPL using Python's built-in sqlite3 package:
```bash
python -m sqlite3 01.db
python -m sqlite3 02.db
```

# Open REPL using sqlite3 package:
```
sqlite3 01.db
```
python's built-in does not have `.fullschema`, '.read` etc. functions. Hence `flake.nix` that installs sqlite3 package and `.envrc` that does that automatically.


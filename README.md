# InterfaceDemos

Examples using tkinter and PyQt5 to build a user interface with components including using external data and displaying visualizations.

I tried to keep it as simple as possible!

The files are setup in such a way that each (except for the interfaces) can function independently of the others. The interfaces, of course, rely on the analysis and visualization libraries.

### Files included:

- Pipfile and Pipfile.lock: Used by the [pipenv](https://pipenv.pypa.io/en/latest/) virtual environment manager.
- my_analysis.py: Contains one class that imports/exports/manipulates, etc. some data.
- my_plots.py: Contains one class that creates a simple and not-at-all-pretty scatter plot
- main_tk.py: Run this to see an example tkinter GUI
- main_qt.py: Run this to see an example PyQt5 GUI

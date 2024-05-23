# EmLi

The main goal of the project **EmLi** (Email List) is sending emails to several
users with some time delay to avoid spam problem. Here, the basic libraries
of the programming language Python together with GTK visual toolkit are used
to provide end user with minimal graphical user interface.

## Project structure

The given package consists of several modules in folder **emli** that has the following
structure:

1. **emli.py** is the main file which starts software initiation
2. **alltypes.py** is file which contains basic constants and functions for multiple usage
3. **mail.py** implements sending electronic letter from one mail to another mail
4. **reader.py** contains functions to read different types of text files for configuration
5. **gui.py** is module to organize graphical user interface for sending configuration using PyGTK library



## Interface

The program interface consists of the button, file chooser entry, file chooser system and big entry field
with the possibility of text marking. The file chooser entry object is created for entering a tabular csv-file
containing information about the destination e-mails where the letters should arrive. The file chooser system
gives possibility

<img src="https://gitlab.com/bridgearchitect/emli/-/blob/main/figure/interface.png?ref_type=heads" width="60%"/>

## Execution

The given program can be laucnhed using the following command in terminal:

```
python3 emli.py
```

After that, the user will see a graphical user interface on the computer screen,
where he must enter the names of the three configuration files and press the button
to send letters.

In addition, work is underway to automate the installation of the application on macOS,
Linux and Windows operating systems to simplify end-user use. These actions will be done
using **PyPi** and **NSIS** services.

## License

# codediff

A file differencer for use in APCS(P) classes. The unix-based `diff` is useful
for comparing files, but is not intended to use the differences for statistical
analysis. codediff is intended primary to catch cheating. &#128187; <!--PC icon-->

## Installing

To install codediff, clone the git repo using `git clone https://github.com/dmontgrmry/codediff.git`.

### Linux and Mac

codediff is written in Python 3. If Python 3 is not installed or has a version
less than version 3.4.0, download and install it [here](http://www.python.org).
There are future plans to enable Python 2 compatability. Alternatively, run
`./install` after cloning the repository.
The installation script will download and build Python 3 from source.

### Windows

Currently, there is no installation script for Windows.
If Python 3 is not installed or has a version less than version 3.4.0,
download and install it [here](http://www.python.org).

Great! Let's move on. &#128077; <!--clapping hands-->

## Usage

Instead of running codediff via `python3 codediff.py`, run the executable
`./codediff`. To compare files and/or directories, simply append them to the end
of the executable in the console. For example, running `./codediff snap_files/`
would compare all the snap files in `snap_files`.

codediff can scrape files off of canvas LMS. Simply tell codediff where
the canvas-generated html redirect files using the same sytax as above. For example,
run `./codediff canvas_html_files/`.

Additionally, codediff can compare java source code files. Simply tell codediff where the
.java files are the same way as before: `./codediff java_files/`.

Finally, you can mix xml files, java files, and scraping files from canvas. codediff will do
all the heavy lifting for you.

Checkout the help (`./codediff --help`) for further reading.

Also, calling `./install` will install codediff for the current user and
add the startup executable to `PATH`.

## TODO

- [X] 0.0.4: Add .java files for APCS classes.
- [ ] 0.0.3: Add statistical analysis
- [X] 0.0.2: Install codediff globably
- [ ] 1.0.0: Add Python2 compatability

## License

codediff is licensed under GNU GPLv3.0. See [LICENSE](https://github.com/dmontgrmry/codediff/blob/master/LICENSE) to see the full text.

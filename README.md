Thompson Parabola Spectrometer Analyzer

This is a GUI program for analyzing Tompson Parabola Spectrometer (TPS).
For more information about TPS, visit:

Before you run this codemake sure you have PyQt5.11 + installed. 
To run
    $ python main.py

The complete package contains the following files:
    main.py
    Window.py -- Graphic user interface
    Trajectory.py -- create a trajectory object from a given set of parameters
    SPEFile.py -- parsing the Princeton Instrument .SPE file and extract image.
    Element Table.py -- parsing the isotope data
    Isotope.dat -- data including all stable isotopes and its AUM mass
    SystemOfUnits.py -- units system for the software
    illustration.png -- illlustration of the TPS configuration

A separate folder containing the source images and configuration data was included for evaluation. 
The most significant traces in these image are C6+, C5+ and H+ ions. 
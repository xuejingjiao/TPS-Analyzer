"""Graphic user interface for Tompson Parabola Spectrometer (TPS) Analyzer"""
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.ticker as ticker
import ElementTable
from Trajectory import *
from SPEFile import *
import pdb

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Thomson Parabola Ion Spectrometer Analyzer V0.0'
        self.setWindowTitle(self.title)
        self.__initMenu()

        self.status_message = 'No SPE file is loaded, please load image from file menu'
        self.statusBar().showMessage(self.status_message)
        self.setCentralWidget(QtWidgets.QWidget(self))
        self.centralWidget().setObjectName("centralWidget")
        self.main_layout = QtWidgets.QGridLayout(self.centralWidget())
        self.main_layout.setObjectName("main_layout")

        self.__initIllustration()
        self.main_layout.addWidget(self.illustration, 0, 0, 1, 5)

        self.__initDetectorPanel()
        self.main_layout.addWidget(self.detector_group, 1, 0, 1, 2)

        self.__initFittingPanel()
        self.main_layout.addWidget(self.fitting_group, 1, 2, 1, 3)

        self.__initTabWidget()
        self.main_layout.addWidget(self.tab_widget, 3, 0, 1, 5)

        self.left = 100
        self.top = 50
        self.width = self.pixmap.width()+20
        self.height = 950

        self.setGeometry(self.left, self.top, self.width, self.height)
        #self.setMaximumSize(self.width, 1400)
        self.show()

    def __initMenu(self):
        """Initialize menu bar"""
        self.main_menu = self.menuBar()
        self.file_menu = self.main_menu.addMenu('File')
        self.help_menu = self.main_menu.addMenu('Help')

        self.load_image_action = QtWidgets.QAction('Load Image', self)
        self.load_image_action.setShortcut('Ctrl+O')
        self.load_image_action.setStatusTip('Open SPE File')
        self.load_image_action.triggered.connect(self.loadImage)

        self.save_param_action = QtWidgets.QAction('Save Parameter', self)
        self.save_param_action.setShortcut('Ctrl+P')
        self.save_param_action.setStatusTip('Save Parameter to a text file')
        self.save_param_action.triggered.connect(self.saveParam)

        self.load_param_action = QtWidgets.QAction('Load Parameter', self)
        self.load_param_action.setShortcut('Ctrl+L')
        self.load_param_action.setStatusTip('Load Parameter from a previously saved file')
        self.load_param_action.triggered.connect(self.loadParam)

        self.save_spec_action = QtWidgets.QAction('Save Spectrum', self)
        self.save_spec_action.setShortcut('Ctrl+S')
        self.save_spec_action.setStatusTip('Save Spectrum as a CSV file')
        self.save_spec_action.triggered.connect(self.saveSpec)

        self.exit_action = QtWidgets.QAction('Exit', self)
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.setStatusTip('Exit application')
        self.exit_action.triggered.connect(self.close)

        self.file_menu.addAction(self.load_image_action)
        self.file_menu.addAction(self.save_param_action)
        self.file_menu.addAction(self.load_param_action)
        self.file_menu.addAction(self.save_spec_action)
        self.file_menu.addAction(self.exit_action)

        self.help_action = QtWidgets.QAction('How to use', self)
        self.help_action.triggered.connect(self.help)
        self.help_menu.addAction(self.help_action)

        self.about_action = QtWidgets.QAction('About', self)
        self.about_action.triggered.connect(self.about)
        self.help_menu.addAction(self.about_action)

    def __initDetectorPanel(self):
        """
        Initialize detector parameters setting panel
        This panel contains input which specify the configuration.
        """
        self.detector_group = QtWidgets.QGroupBox(self.centralWidget())
        #font = QtGui.QFont()
        #font.setPointSize(9)
        #self.detector_group.setFont(font)
        self.detector_group.setObjectName("detector_group")

        self.detector_group_layout = QtWidgets.QGridLayout(self.detector_group)
        self.detector_group_layout.setObjectName("detector_group_layout")

        self.B_label = QtWidgets.QLabel("B Field (T) :", self.detector_group)
        self.B_label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.B_label.setObjectName("B_label")
        self.detector_group_layout.addWidget(self.B_label, 0, 0, 1, 1)

        self.E_label = QtWidgets.QLabel("E Field (kV/cm) :", self.detector_group)
        self.E_label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.E_label.setObjectName("E_label")
        self.detector_group_layout.addWidget(self.E_label, 1, 0, 1, 1)

        self.L_M_label = QtWidgets.QLabel("L_M (cm) :", self.detector_group)
        self.L_M_label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.L_M_label.setObjectName("L_M_label")
        self.detector_group_layout.addWidget(self.L_M_label, 2, 0, 1, 1)

        self.L_ME_label = QtWidgets.QLabel("L_ME (cm) :", self.detector_group)
        self.L_ME_label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.L_ME_label.setObjectName("L_ME_label")
        self.detector_group_layout.addWidget(self.L_ME_label, 3, 0, 1, 1)

        self.L_E_label = QtWidgets.QLabel("L_E (cm) :", self.detector_group)
        self.L_E_label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.L_E_label.setObjectName("L_E_label")
        self.detector_group_layout.addWidget(self.L_E_label, 4, 0, 1, 1)

        self.L_ES_label = QtWidgets.QLabel("L_ES (cm) :", self.detector_group)
        self.L_ES_label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.L_ES_label.setObjectName("L_ES_label")
        self.detector_group_layout.addWidget(self.L_ES_label, 5, 0, 1, 1)

        self.B_box = QtWidgets.QDoubleSpinBox(self.detector_group)
        self.B_box.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.B_box.setObjectName("B_box")
        self.B_box.setMinimum(0)
        self.B_box.setMaximum(2)
        self.B_box.setValue(0.44)
        self.detector_group_layout.addWidget(self.B_box, 0, 1, 1, 1)

        self.E_box = QtWidgets.QDoubleSpinBox(self.detector_group)
        self.E_box.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.E_box.setObjectName("E_box")
        self.E_box.setValue(20)
        self.detector_group_layout.addWidget(self.E_box, 1, 1, 1, 1)

        self.L_M_box = QtWidgets.QDoubleSpinBox(self.detector_group)
        self.L_M_box.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.L_M_box.setObjectName("L_M_box")
        self.L_M_box.setValue(10)
        self.detector_group_layout.addWidget(self.L_M_box, 2, 1, 1, 1)

        self.L_ME_box = QtWidgets.QDoubleSpinBox(self.detector_group)
        self.L_ME_box.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.L_ME_box.setObjectName("L_ME_box")
        self.L_ME_box.setValue(5)
        self.detector_group_layout.addWidget(self.L_ME_box, 3, 1, 1, 1)

        self.L_E_box = QtWidgets.QDoubleSpinBox(self.detector_group)
        self.L_E_box.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.L_E_box.setObjectName("L_E_box")
        self.L_E_box.setValue(22.5)
        self.detector_group_layout.addWidget(self.L_E_box, 4, 1, 1, 1)

        self.L_ES_box = QtWidgets.QDoubleSpinBox(self.detector_group)
        self.L_ES_box.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.L_ES_box.setObjectName("L_ES_box")
        self.L_ES_box.setValue(7)
        self.detector_group_layout.addWidget(self.L_ES_box, 5, 1, 1, 1)

        for box in [self.E_box, self.L_M_box, self.L_ME_box, self.L_E_box, self.L_ES_box]:
            box.setMinimum(0)
            box.setMaximum(50)
            box.setDecimals(1)

    def __initFittingPanel(self):
        """
        Initialize Fitting Panel
        The fitting panel contains options for users to select ion species,
        adjust the zeor point, compensate tilt and set scaling etc.
        """
        self.fitting_group = QtWidgets.QGroupBox(self.centralWidget())
        #font = QtGui.QFont()
        #font.setPointSize(9)
        #self.fitting_group.setFont(font)
        self.fitting_group.setObjectName("fitting_group")
        self.fitting_group_layout = QtWidgets.QGridLayout(self.fitting_group)
        self.fitting_group_layout.setObjectName("fitting_group_layout")

        self.element_label = QtWidgets.QLabel("Element :", self.fitting_group)
        self.element_label.setObjectName("element_label")
        self.element_label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.fitting_group_layout.addWidget(self.element_label, 0, 0, 1, 1)

        self.element_box = QtWidgets.QComboBox(self.fitting_group)
        self.element_box.addItems([element.name for element in ElementTable.table])
        self.element_box.setCurrentIndex(0)
        self.element_box.setObjectName("element_box")
        self.element_box.currentIndexChanged.connect(self.updateComboBox)
        self.fitting_group_layout.addWidget(self.element_box, 1, 0, 1, 1)

        self.isotope_label = QtWidgets.QLabel("Isotope (A) :", self.fitting_group)
        self.isotope_label.setObjectName("isotope_label")
        self.isotope_label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.fitting_group_layout.addWidget(self.isotope_label, 0, 1, 1, 1)

        self.isotope_box = QtWidgets.QComboBox(self.fitting_group)
        self.isotope_box.setObjectName("isotope_box")
        self.fitting_group_layout.addWidget(self.isotope_box, 1, 1, 1, 1)

        self.charge_label = QtWidgets.QLabel("Charge Status :", self.fitting_group)
        self.charge_label.setObjectName("charge_label")
        self.charge_label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.fitting_group_layout.addWidget(self.charge_label, 0, 2, 1, 1)

        self.charge_box = QtWidgets.QComboBox(self.fitting_group)
        self.charge_box.setObjectName("charge_box")
        self.fitting_group_layout.addWidget(self.charge_box, 1, 2, 1, 1)

        #initialize charge box and isotope box
        self.updateComboBox(0)

        self.zero_point_label = QtWidgets.QLabel("Zero (x0, y0) :", self.fitting_group)
        self.zero_point_label.setObjectName("zero_point_label")
        self.zero_point_label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.fitting_group_layout.addWidget(self.zero_point_label, 2, 0, 1, 1)

        self.x0_box = QtWidgets.QSpinBox(self.fitting_group)
        self.x0_box.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.x0_box.setObjectName("x0_box")
        self.x0_box.setMinimum(0)
        self.x0_box.setMaximum(600)
        self.x0_box.setValue(127)
        self.fitting_group_layout.addWidget(self.x0_box, 2, 1, 1, 1)

        self.y0_box = QtWidgets.QSpinBox(self.fitting_group)
        self.y0_box.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.y0_box.setObjectName("y0_box")
        self.y0_box.setMinimum(0)
        self.y0_box.setMaximum(1000)
        self.y0_box.setValue(153)
        self.fitting_group_layout.addWidget(self.y0_box, 2, 2, 1, 1)

        self.tilt_label = QtWidgets.QLabel("Tilt (deg) :", self.fitting_group)
        self.tilt_label.setObjectName("tilt_label")
        self.tilt_label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.fitting_group_layout.addWidget(self.tilt_label, 3, 0, 1, 1)

        self.tilt_box = QtWidgets.QDoubleSpinBox(self.fitting_group)
        self.tilt_box.setObjectName("tilt_box")
        self.tilt_box.setDecimals(1)
        self.tilt_box.setSingleStep(0.1)
        self.tilt_box.setMinimum(-60)
        self.tilt_box.setMaximum(60)
        self.tilt_box.setValue(0)
        self.fitting_group_layout.addWidget(self.tilt_box, 3, 1, 1, 1)

        self.save_parameter_button = QtWidgets.QPushButton("Save Parameters", self.fitting_group)
        self.save_parameter_button.setObjectName("load_image_button")
        self.save_parameter_button.setToolTip("Save parameters to a file")
        self.save_parameter_button.clicked.connect(self.saveParam)
        self.fitting_group_layout.addWidget(self.save_parameter_button, 3, 2, 1, 1)

        self.scale_label = QtWidgets.QLabel("Scale (pixel/cm) :", self.fitting_group)
        self.scale_label.setObjectName("scale_label")
        self.scale_label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.fitting_group_layout.addWidget(self.scale_label, 4, 0, 1, 1)

        self.scale_box = QtWidgets.QDoubleSpinBox(self.fitting_group)
        self.scale_box.setObjectName("scale_box")
        self.scale_box.setDecimals(1)
        self.scale_box.setMaximum(1000)
        self.scale_box.setValue(154)
        self.fitting_group_layout.addWidget(self.scale_box, 4, 1, 1, 1)

        self.load_parameter_button = QtWidgets.QPushButton("Load Parameters", self.fitting_group)
        self.load_parameter_button.setObjectName("load_image_button")
        self.load_parameter_button.setToolTip("Load parameter from a previously saved file")
        self.load_parameter_button.clicked.connect(self.loadParam)
        self.fitting_group_layout.addWidget(self.load_parameter_button, 4, 2, 1, 1)

        self.load_image_button = QtWidgets.QPushButton("Load Image", self.fitting_group)
        self.load_image_button.setObjectName("load_image_button")
        self.load_image_button.setToolTip("Load image from a spe file")
        self.load_image_button.clicked.connect(self.loadImage)
        self.fitting_group_layout.addWidget(self.load_image_button, 5, 0, 1, 1)

        self.trajectory_button = QtWidgets.QPushButton("Plot Trajectory", self.fitting_group)
        self.trajectory_button.setObjectName("trajectory_button")
        self.trajectory_button.setToolTip("Plot trajectory on the image")
        self.trajectory_button.clicked.connect(self.plotTrajectory)
        self.fitting_group_layout.addWidget(self.trajectory_button, 5, 1, 1, 1)

        self.spectrum_button = QtWidgets.QPushButton("Show Spectrum", self.fitting_group)
        self.spectrum_button.setObjectName("trajectory_button")
        self.spectrum_button.clicked.connect(self.plotSpectrum)
        self.fitting_group_layout.addWidget(self.spectrum_button, 5, 2, 1, 1)

    def __initTabWidget(self):
        """initialize the tabwidget which contain matplotlib canvas"""
        self.tab_widget = QtWidgets.QTabWidget(self.centralWidget())
        self.tab_widget.setObjectName("tab_widget")
        self.image_fig = Figure()
        self.image_axes = self.image_fig.add_axes([0.1, 0.1, 0.85, 0.85])
        self.image_canvas = FigureCanvasQTAgg(self.image_fig)
        self.tab_widget.addTab(self.image_canvas, "SPE Image")

        self.plot_fig = Figure()
        self.plot_axes = self.plot_fig.add_axes([0.1, 0.15, 0.85, 0.80])
        self.plot_canvas = FigureCanvasQTAgg(self.plot_fig)
        self.tab_widget.addTab(self.plot_canvas, "Spectrum")

    def __initIllustration(self):
        """add illustration of a Tompson Parabola Spectrometer to the window"""
        self.illustration = QtWidgets.QLabel(self.centralWidget())
        self.illustration.setObjectName("graphicsView")
        self.pixmap = QtGui.QPixmap("illustration.png")
        self.illustration.setPixmap(self.pixmap)

    def loadImage(self):
        """load image from a spe file"""
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                        "Open Image", "","SPE Files (*.spe);;All Files (*)")
        if not filename:
            return
        try:
            #check if the SPE file can be processed successfully
            self.spe = SPEFile(filename)
        except:
            QtWidgets.QMessageBox.about(self, "Warning", "Wrong file type!")
        else:
            self.tab_widget.setCurrentWidget(self.image_canvas)
            self.img = self.spe.getImage()
            #clear lines before erase the whole axes
            if hasattr(self, 'trace_lines'):
                while self.trace_lines:
                    self.trace_lines.pop().remove()
            self.image_axes.cla()
            self.image_axes.imshow(self.img, origin='lower')
            (h, w) = self.img.shape
            self.image_axes.set_xlim((0, w))
            self.image_axes.set_ylim((0, h))
            self.statusBar().showMessage(filename)
            self.image_canvas.draw()

    def saveParam(self):
        """write parameters to a text file"""
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Save Parameters","","Text Files (*.txt);;All Files (*)")
        if not filename:
            return
        with open(filename, "w") as f:
            f.write("B field (T) : {}\n".format(self.B_box.value()))
            f.write("E field (V/cm) : {}\n".format(self.E_box.value()))
            f.write("L_M (cm) : {}\n".format(self.L_M_box.value()))
            f.write("L_ME (cm) : {}\n".format(self.L_ME_box.value()))
            f.write("L_E (cm) : {}\n".format(self.L_E_box.value()))
            f.write("L_ES (cm) : {}\n".format(self.L_ES_box.value()))

            f.write("X0 : {}\n".format(self.x0_box.value()))
            f.write("Y0 : {}\n".format(self.y0_box.value()))
            f.write("Tilt : {}\n".format(self.tilt_box.value()))
            f.write("Scale : {}\n".format(self.scale_box.value()))

    def loadParam(self):
        """"load parameter from a previously saved file"""
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                        "Open Image", "","Text Files (*.txt);;All Files (*)")
        if not filename:
            return
        try:
            with open(filename, 'r') as f:
                for name, box in zip(['B', 'E', 'L_M', 'L_ME', 'L_E', 'L_ES', 'X0', 'Y0', 'Tilt', 'Scale'],
                                     [self.B_box, self.E_box, self.L_M_box, self.L_ME_box,
                                      self.L_E_box, self.L_ES_box, self.x0_box, self.y0_box,
                                      self.tilt_box, self.scale_box]):
                    line = f.readline().split()
                    # check if its the item that we are looking for
                    assert line[0] == name
                    box.setValue(float(line[-1]))
        except:
            QtWidgets.QMessageBox.about(self, "Warning", "Corrupted parameter file!")

    def saveSpec(self):
        """"save the spectrum to a CSV file"""
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Save Spectrum","","CSV Files (*.csv);;All Files (*)")
        if not filename:
            return
        try:# avoid the error that a spectrum may not have been generated
            self.trajectory.saveSpectrum(filename)
        except:
            QtWidgets.QMessageBox.about(self, "Warning", "No extracted spectrum found!")

    def plotTrajectory(self):
        """calculate and plot trajectory on the image for visual alignment"""
        isotopes = ElementTable.table[self.element_box.currentIndex()].isotopes
        #find the corresonding AUM mass of a isotope
        for iso in isotopes:
            if iso.A == self.isotope_box.currentText():
                m = float(iso.mass)
                break
        try:# avoid the error that some parameter maybe missing
            self.trajectory = Trajectory(q = int(self.charge_box.currentText()),
                                        m = m,
                                        B = self.B_box.value(),
                                        E = self.E_box.value(),
                                        L_M = self.L_M_box.value(),
                                        L_ME = self.L_ME_box.value(),
                                        L_E = self.L_E_box.value(),
                                        L_ES = self.L_ES_box.value(),
                                        scale = self.scale_box.value())
        except:
            QtWidgets.QMessageBox.about(self, "Warning", "Some parameters are missing")
        else:
            self.trajectory.transform(dx=self.x0_box.value(),
                                        dy=self.y0_box.value(),
                                        rotate=self.tilt_box.value())
            #remove trajectory if last trajectory exist
            if hasattr(self, 'trace_lines'):
                while self.trace_lines:
                    self.trace_lines.pop().remove()
            x, y = self.trajectory.getTrace()
            self.trace_lines = self.image_axes.plot(x, y+5,
                                                    x, y-5,
                                                    color='white',
                                                    linestyle='dashed',
                                                    linewidth=0.5)
            self.image_canvas.draw()
            #to solve the problem that Mac OS wont automatically update current canvas
            self.tab_widget.setCurrentWidget(self.plot_canvas)
            self.tab_widget.setCurrentWidget(self.image_canvas)
            


    def plotSpectrum(self):
        """plot spectrum on a seperate canvas"""
        if hasattr(self, "trajectory"):
            self.plot_axes.cla()
            E, dNdE = self.trajectory.extracSpectrum(self.img)
            self.plot_axes.plot(E, dNdE)
            self.plot_axes.set_xlim(left=0)
            self.plot_axes.set_ylim(bottom=0)
            self.plot_axes.set_xlabel('Ion Energy (MeV)')
            self.plot_axes.set_ylabel('Signal Level (PSL/MeV)')
            self.plot_axes.ticklabel_format(style='sci', scilimits=(-2, 3))
            self.tab_widget.setCurrentWidget(self.plot_canvas)
            self.plot_canvas.draw()
        else:
            QtWidgets.QMessageBox.about(self, "Reminder", "Please draw a trajectory first")

    def updateComboBox(self, i):
        """update the isotope and charge combobox after user made a choice for an element"""
        self.isotope_box.clear()
        self.isotope_box.addItems([isotope.A for isotope in ElementTable.table[i].isotopes])
        self.charge_box.clear()
        self.charge_box.addItems([str(i) for i in range(1, int(ElementTable.table[i].index) + 1)])

    def help(self):
        QtWidgets.QMessageBox.about(self, "How to use",
        """
        Step 1: Load SPE Image.
        Step 2: Visually calibrated the image against a clear known trace
        Step 3: Save paramter into a file
        Step 4: Plot the spectrum of a choosen ion species
        Step 5: Save the spectrum in as CSV file for later analysis
        """)

    def about(self):
        QtWidgets.QMessageBox.about(self, "About",
        """
        Thomson Parabola Ion Spectrometer Analyzer V.1.0
        Copyright 2018 Xuejing Jiao
        """)
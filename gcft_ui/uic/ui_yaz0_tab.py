# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'yaz0_tab.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QGroupBox, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSlider,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Yaz0Tab(object):
    def setupUi(self, Yaz0Tab):
        if not Yaz0Tab.objectName():
            Yaz0Tab.setObjectName(u"Yaz0Tab")
        Yaz0Tab.resize(776, 515)
        self.verticalLayout = QVBoxLayout(Yaz0Tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.decompress_yaz0 = QPushButton(Yaz0Tab)
        self.decompress_yaz0.setObjectName(u"decompress_yaz0")

        self.horizontalLayout_2.addWidget(self.decompress_yaz0)

        self.compress_yaz0 = QPushButton(Yaz0Tab)
        self.compress_yaz0.setObjectName(u"compress_yaz0")

        self.horizontalLayout_2.addWidget(self.compress_yaz0)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.groupBox = QGroupBox(Yaz0Tab)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pad_compressed_files = QCheckBox(self.groupBox)
        self.pad_compressed_files.setObjectName(u"pad_compressed_files")

        self.verticalLayout_2.addWidget(self.pad_compressed_files)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.compression_level = QSlider(self.groupBox)
        self.compression_level.setObjectName(u"compression_level")
        self.compression_level.setMinimum(1)
        self.compression_level.setMaximum(16)
        self.compression_level.setSingleStep(1)
        self.compression_level.setValue(16)
        self.compression_level.setOrientation(Qt.Horizontal)

        self.horizontalLayout.addWidget(self.compression_level)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(20, 463, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Yaz0Tab)

        QMetaObject.connectSlotsByName(Yaz0Tab)
    # setupUi

    def retranslateUi(self, Yaz0Tab):
        Yaz0Tab.setWindowTitle(QCoreApplication.translate("Yaz0Tab", u"Form", None))
        self.decompress_yaz0.setText(QCoreApplication.translate("Yaz0Tab", u"Decompress File", None))
        self.compress_yaz0.setText(QCoreApplication.translate("Yaz0Tab", u"Compress File", None))
        self.groupBox.setTitle(QCoreApplication.translate("Yaz0Tab", u"Compression Options", None))
        self.pad_compressed_files.setText(QCoreApplication.translate("Yaz0Tab", u"Pad compressed files to 0x20 bytes", None))
        self.label_3.setText(QCoreApplication.translate("Yaz0Tab", u"Compression level:", None))
        self.label.setText(QCoreApplication.translate("Yaz0Tab", u"Faster", None))
        self.label_2.setText(QCoreApplication.translate("Yaz0Tab", u"Smaller", None))
    # retranslateUi


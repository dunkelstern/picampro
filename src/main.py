# This Python file uses the following encoding: utf-8
import sys
import os

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import Slot


from settings import Settings
from pipeline import Pipeline

settings = None
pipeline = None


@Slot(str, str)
def set_value(area, key, value):
    print(area, key, value)
    settings.parse("{}:{}".format(area, key), value)
    settings.save()
    settings.apply(pipeline)


@Slot(str)
def button_pressed(key):
    print('button', key)
    if key == 'stop':
        pipeline.preview()
    elif key == 'rec':
        pipeline.start_recording()
    elif key == 'stream':
        pipeline.start_streaming()
    elif key == 'mic':
        pass

@Slot()
def start_preview():
    print('start preview')
    pipeline.preview()

@Slot()
def stop_preview():
    print('stop preview')
    pipeline.stop()


if __name__ == "__main__":
    settings = Settings()
    pipeline = Pipeline(settings)
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.load(os.path.join(os.path.dirname(__file__), "../resources/qml/Main.qml"))
    
    if not engine.rootObjects():
        sys.exit(-1)

    root = engine.rootObjects()[0]

    # Connect slots
    root.setValue.connect(set_value)
    root.buttonPressed.connect(button_pressed)
    root.stopVideoPreview.connect(stop_preview)
    root.startVideoPreview.connect(start_preview)
    
    # Transfer settings over
    root.setProperty('modelData', settings.serialize())

    sys.exit(app.exec_())

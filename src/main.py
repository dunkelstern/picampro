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
def set_value(key, value):
    print(key, value)
    settings.parse(key, value)
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

    engine.rootObjects()[0].setValue.connect(set_value)
    engine.rootObjects()[0].buttonPressed.connect(button_pressed)
    engine.rootObjects()[0].stopVideoPreview.connect(stop_preview)
    engine.rootObjects()[0].startVideoPreview.connect(start_preview)

    sys.exit(app.exec_())

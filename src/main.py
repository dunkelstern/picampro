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
root = None

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
        pipeline.stop_recording()
        pipeline.stop_streaming()
    elif key == 'rec':
        # TODO: change icon/color/whatever
        if pipeline.recording:
            pipeline.stop_recording()
        else:
            pipeline.start_recording()
    elif key == 'stream':
        # TODO: change icon/color/whatever
        if pipeline.streaming:
            pipeline.stop_streaming()
        else:
            pipeline.start_streaming()
    elif key == 'mic':
        # TODO: change icon/color/whatever
        if pipeline.muted:
            pipeline.unmute_audio()
        else:
            pipeline.mute_audio()
    elif key == 'settings':
        if not pipeline.recording and not pipeline.streaming:
            root.showSettings()

@Slot()
def start_video():
    print('start pipeline')
    pipeline.start_pipeline()

@Slot()
def stop_video():
    print('stop pipeline')
    pipeline.stop_pipeline()

def update_histogram(data):
    root.setProperty('histogramData', data)

def update_vumeter(data):
    root.setProperty('vuMeterData', data)

if __name__ == "__main__":
    settings = Settings()
    pipeline = Pipeline(settings)
    pipeline.histogram_update_callback = update_histogram
    pipeline.vu_update_callback = update_vumeter
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.load(os.path.join(os.path.dirname(__file__), "../resources/qml/Main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    root = engine.rootObjects()[0]

    # Connect slots
    root.setValue.connect(set_value)
    root.buttonPressed.connect(button_pressed)
    root.stopVideo.connect(stop_video)
    root.startVideo.connect(start_video)

    # Transfer settings over
    root.setProperty('modelData', settings.serialize())
    root.setProperty('histogramData', [0] * 32)
    root.setProperty('vuMeterData', [0] * 4)

    sys.exit(app.exec_())

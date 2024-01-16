from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QSize, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QIcon, QCursor
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QCheckBox,
    QComboBox,
    QListView,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QToolButton,
    QProxyStyle,
    QStyle,
    QScrollArea,
    QScrollBar,
    QPlainTextEdit,
)
from pynput import keyboard

from frontend.stylesheets import StyleSheets

from backend.config import Config
from backend.util.text_util import TextUtil


class Font(QFont):
    def __init__(self, font_size):
        super().__init__()
        self.setFamily("Segoe UI")
        self.setPointSize(font_size)


class TextLabel(QLabel):
    def __init__(
        self,
        parent,
        object_name,
        text,
        font=Font(10),
        style_sheet=StyleSheets.white_text,
    ):
        super().__init__(parent)
        self.setObjectName(object_name)
        self.setText(text)
        self.setFont(font)
        self.setStyleSheet(style_sheet)
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter)


class HyperlinkTextLabel(QLabel):
    def __init__(self, parent, object_name, text, link, font):
        super().__init__(parent)
        self.setObjectName(object_name)
        self.setFont(font)
        self.setText(
            f'<a style="color: white; text-decoration:none;" href="{link}">{text}</a>'
        )
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.setTextFormat(Qt.TextFormat.RichText)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self.setOpenExternalLinks(True)


def on_focus_in_callback(self):
    return None


def on_focus_out_callback(self):
    return None


class TextInputBox(QLineEdit):
    def __init__(
        self,
        parent,
        object_name,
        size,
        placeholder_text,
        text=None,
        font=Font(10),
        style_sheet=StyleSheets.text_box,
    ):
        QLineEdit.__init__(self, parent)
        self.setObjectName(object_name)
        self.setFixedSize(size)
        self.setPlaceholderText(placeholder_text)
        if text is not None:
            self.setText(text)
        self.setFont(font)
        self.setStyleSheet(style_sheet)

    def focusInEvent(self, event: QtGui.QFocusEvent) -> None:
        super().focusInEvent(event)
        if not self.isReadOnly():
            QTimer.singleShot(0, self.selectAll)
            TextInputBox.on_focus_in_callback()

    def focusOutEvent(self, event: QtGui.QFocusEvent) -> None:
        super().focusOutEvent(event)
        TextInputBox.on_focus_out_callback()

    def setReadOnly(self, a0: bool) -> None:
        super().setReadOnly(a0)
        self.setStyleSheet(
            StyleSheets.text_box if not a0 else StyleSheets.text_box_read_only
        )


class MultiLineTextInputBox(QPlainTextEdit):
    def __init__(
        self,
        parent,
        object_name,
        width,
        height,
        full_height,
        placeholder_text,
        text=None,
        font=Font(10),
        style_sheet=StyleSheets.multiline_text_box,
    ):
        super().__init__(parent)
        self.setObjectName(object_name)
        self.setFixedWidth(width)
        self.small_height = height
        self.full_height = full_height
        self.setMinimumHeight(height)
        self.setPlaceholderText(placeholder_text)
        if text is not None:
            self.setPlainText(text)
        self.setFont(font)
        self.setStyleSheet(style_sheet)

    def wheelEvent(self, e: QtGui.QWheelEvent) -> None:
        current = self.verticalScrollBar().value()
        minimum = self.verticalScrollBar().minimum()
        maximum = self.verticalScrollBar().maximum()

        if e.angleDelta().y() < 0 and current == maximum:
            self.verticalScrollBar().setValue(maximum)
        elif e.angleDelta().y() > 0 and current == minimum:
            self.verticalScrollBar().setValue(minimum)
        else:
            return QPlainTextEdit.wheelEvent(self, e)
        e.accept()

    def focusInEvent(self, event: QtGui.QFocusEvent) -> None:
        super().focusInEvent(event)
        if not self.isReadOnly():
            self.animate()
            TextInputBox.on_focus_in_callback()

    def focusOutEvent(self, event: QtGui.QFocusEvent) -> None:
        super().focusOutEvent(event)
        if not self.isReadOnly():
            self.animate()
            TextInputBox.on_focus_out_callback()

    def animate(self):
        self.animation = QPropertyAnimation(self, b"minimumHeight")
        self.animation.setDuration(500)
        self.animation.setStartValue(self.minimumHeight())
        self.animation.setEndValue(
            self.full_height if self.hasFocus() else self.small_height
        )
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuint)
        self.animation.start()


class CheckBox(QCheckBox):
    def __init__(self, parent, object_name, style_sheet=StyleSheets.check_box):
        super().__init__(parent)
        if object_name is not None:
            self.setObjectName(object_name)
        self.setAutoFillBackground(False)
        self.setStyleSheet(style_sheet)

    def setEnabled(self, a0: bool) -> None:
        super().setEnabled(a0)
        self.setStyleSheet(
            StyleSheets.check_box if a0 else StyleSheets.check_box_read_only
        )


class Selector(QComboBox):
    def __init__(self, parent, object_name, size, items, active_item=None):
        super().__init__(parent)
        self.view = QListView()
        self.view.setFont(Font(8))

        self.setObjectName(object_name)
        self.setFont(Font(10))
        self.setFixedSize(size)
        self.addItems(items)
        if active_item is not None:
            self.setCurrentIndex(self.findText(active_item))
        self.setView(self.view)
        self.setStyleSheet(StyleSheets.selector)

    def wheelEvent(self, e: QtGui.QWheelEvent) -> None:
        e.ignore()


class Button(QPushButton):
    def __init__(self, parent, object_name, text, size: QSize):
        super().__init__(parent)
        self.setObjectName(object_name)
        self.setFixedSize(size)
        self.setFont(Font(10))
        self.setText(text)
        self.setStyleSheet(StyleSheets.button)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))


class CheckBoxWithFunction(CheckBox):
    def __init__(
        self, parent, object_name, on_click, style_sheet=StyleSheets.check_box
    ):
        super().__init__(parent, object_name, style_sheet)
        self.clicked.connect(on_click)


class CollapsibleBox(QWidget):
    def __init__(self, parent, object_name, text):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(15)

        self.toggleButton = QToolButton(self)
        self.toggleButton.setObjectName(object_name)
        self.toggleButton.setCheckable(True)
        self.toggleButton.setChecked(False)
        self.toggleButton.setFont(Font(12))
        self.toggleButton.setStyleSheet(StyleSheets.collapsible_box_inactive)
        self.toggleButton.setText(text)
        self.toggleButton.setIcon(QIcon(Icons.right_arrow))
        self.toggleButton.setIconSize(QSize(20, 20))
        self.toggleButton.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonTextBesideIcon
        )
        self.toggleButton.pressed.connect(self.on_pressed)
        self.toggleButton.setStyle(NoShiftStyle())
        self.toggleButton.setCursor(Qt.CursorShape.PointingHandCursor)

        self.layout.addWidget(self.toggleButton, alignment=Qt.AlignmentFlag.AlignTop)

    def on_pressed(self):
        pass


# https://forum.qt.io/topic/15068/prevent-flat-qtoolbutton-from-moving-when-clicked/8
class NoShiftStyle(QProxyStyle):
    def pixelMetric(self, metric, option, widget):
        if (
            metric == QStyle.PixelMetric.PM_ButtonShiftHorizontal
            or metric == QStyle.PixelMetric.PM_ButtonShiftVertical
        ):
            ret = 0
        else:
            ret = QProxyStyle.pixelMetric(self, metric, option, widget)
        return ret


class Icons:
    __base = "assets/images/icons"

    icon = "assets/images/inspo1.png"
    app_splash = "assets/images/app_splash.png"
    splash = "assets/images/splash.png"

    minimize = __base + "/icon_minimize.png"
    restore = __base + "/icon_restore.png"
    maximize = __base + "/icon_maximize.png"
    close = __base + "/icon_close.png"
    menu = __base + "/icon_menu.png"
    home = __base + "/icon_home.png"
    preferences = __base + "/icon_preferences.png"
    settings = __base + "/icon_settings.png"
    bloodweb = __base + "/icon_graph.png"
    help = __base + "/icon_help.png"
    down_arrow = __base + "/icon_down_arrow.png"
    right_arrow = __base + "/icon_right_arrow.png"
    up_arrow = __base + "/icon_up_arrow.png"
    discord = __base + "/icon_discord.png"
    twitter = __base + "/icon_twitter.png"


# TODO space shouldnt deselect
class HotkeyInput(QPushButton):
    def __init__(self, parent, object_name, size, on_activate, on_deactivate):
        super().__init__(parent)
        self.on_activate = on_activate  # on activating THIS button
        self.on_deactivate = on_deactivate  # on deactivating THIS button
        self.pressed_keys = []
        self.pressed_keys_cache = []
        self.setObjectName(object_name)
        self.setFixedSize(size)
        self.setStyleSheet(StyleSheets.button)
        self.set_keys(Config().hotkey())
        self.setFont(Font(10))
        self.clicked.connect(self.on_click)
        self.active = False
        self.listener = None
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def on_click(self):
        if self.active:
            self.set_keys(self.pressed_keys_cache)
            self.setStyleSheet(StyleSheets.button)
            self.on_deactivate()
            self.stop_recording_listener()
            self.active = False
        else:
            self.pressed_keys_cache = self.pressed_keys
            self.pressed_keys = []
            self.setStyleSheet(StyleSheets.button_recording)
            self.setText("Recording keystrokes...")
            self.on_activate()
            self.start_recording_listener()
            self.active = True

    def start_recording_listener(self):
        self.listener = keyboard.Listener(
            on_press=self.on_key_down, on_release=self.on_key_up
        )
        self.listener.start()

    def stop_recording_listener(self):
        self.listener.stop()
        self.listener = None

    def on_key_down(self, key):
        new_key = TextUtil.pynput_to_key_string(self.listener, key)
        key = new_key if new_key else str(key).replace("Key.", "")
        self.pressed_keys = list(dict.fromkeys(self.pressed_keys + [key]))
        self.setText(" + ".join([TextUtil.title_case(k) for k in self.pressed_keys]))

    def on_key_up(self, key):
        new_key = TextUtil.pynput_to_key_string(self.listener, key)
        key = new_key if new_key else str(key).replace("Key.", "")
        self.setText(" + ".join([TextUtil.title_case(k) for k in self.pressed_keys]))

        self.active = False
        self.stop_recording_listener()
        self.on_deactivate()
        self.setStyleSheet(StyleSheets.button)

    def set_keys(self, pressed_keys):
        self.pressed_keys = pressed_keys
        self.setText(" + ".join([TextUtil.title_case(k) for k in self.pressed_keys]))


class ScrollBar(QScrollBar):
    def __init__(self, parent, base_object_name):
        super().__init__(parent)
        self.setObjectName(f"{base_object_name}ScrollBar")
        self.setOrientation(Qt.Orientation.Vertical)
        self.setStyleSheet(StyleSheets.scroll_bar)


class ScrollArea(QScrollArea):
    def __init__(self, parent, base_object_name, scroll_bar):
        super().__init__(parent)
        self.setObjectName(f"{base_object_name}ScrollArea")
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBar(scroll_bar)
        self.setWidgetResizable(True)
        self.setStyleSheet(
            f"""
            QScrollArea#{base_object_name}ScrollArea {{
                background: transparent;
                border: 0px;
            }}"""
        )


class ScrollAreaContent(QWidget):
    def __init__(self, parent, base_object_name):
        super().__init__(parent)
        self.setObjectName(f"{base_object_name}ScrollAreaContent")
        self.setStyleSheet(
            f"""
            QWidget#{base_object_name}ScrollAreaContent {{
                background: transparent;
            }}"""
        )

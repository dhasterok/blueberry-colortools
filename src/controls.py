

from PyQt6.QtCore import Qt, QRect, QPropertyAnimation, pyqtProperty, pyqtSignal, QRect
from PyQt6.QtGui import QPainter, QColor, QAction, QIcon
from PyQt6.QtWidgets import ( QWidget )

from src.ColorManager import is_valid_hex_color

from src.config import ICONPATH, default_font

class ToggleSwitch(QWidget):
    """
    A custom toggle switch widget with animated transitions and customizable colors.

    This widget mimics a modern on/off switch, commonly used in mobile and web UIs. It supports 
    smooth animated transitions between the "on" and "off" states, emits a signal when toggled, 
    and provides optional customization for height, animation duration, and colors.

    Parameters
    ----------
    parent : QWidget, optional
        The parent widget, by default None.
    height : int, optional
        Height of the toggle switch. The width is automatically set to twice the height. Default is 24.
    duration : int, optional
        Duration of the toggle animation in milliseconds. Default is 100.
    fg_color : str, optional
        Foreground color (thumb/slider) in hex format. Default is "#f0f0f0".
    bg_left_color : str, optional
        Background color when the switch is in the "off" position. Default is "#ffffff".
    bg_right_color : str, optional
        Background color when the switch is in the "on" position. Default is "#478ae4".

    Signals
    -------
    stateChanged : bool
        Emitted when the switch state changes.

    Attributes
    ----------
    thumb_pos : float
        Position of the thumb (used for animation).
    
    Methods
    -------
    toggle()
        Toggles the switch state and emits the `stateChanged` signal.
    setChecked(checked)
        Sets the checked state and animates the thumb.
    isChecked() -> bool
        Returns the current checked state.
    """
    stateChanged = pyqtSignal(bool)  # Signal emitted when the state changes

    def __init__(self, parent=None, height=24, duration=100, fg_color="#f0f0f0", bg_left_color="#ffffff", bg_right_color="#478ae4"):
        super().__init__(parent)
        self._height = height
        self._width = height * 2
        self.setFixedSize(self._width, self._height)

        self._checked = False

        self._thumb_pos = 2  # Initial position
        self.duration = duration

        self._animation = QPropertyAnimation(self, b"thumb_pos")
        self._animation.setDuration(duration)  # Smooth animation

        if is_valid_hex_color(fg_color):
            self.fg_color = fg_color
        else:
            self.fg_color = "#f0f0f0"

        # background colors
        if is_valid_hex_color(bg_left_color):
            self.bg_left_color = bg_left_color
        else:
            self.bg_left_color = "#ffffff"
        if is_valid_hex_color(bg_right_color):
            self.bg_right_color = bg_right_color
        else:
            self.bg_right_color="#478ae4"

    def toggle(self):
        """Toggle switch state and emit signal"""
        self._checked = not self._checked
        self._animation.setStartValue(self._thumb_pos)
        self._animation.setEndValue(self._width - self._height + 2 if self._checked else 2)
        self._animation.start()

        self.stateChanged.emit(self._checked)  # Emit signal

    def setChecked(self, checked: bool):
        """Sets the checked state of the toggle switch and triggers the animation

        Parameters
        ----------
        checked : bool
            New check state of the toggle switch.
        """
        # Accept both bool and Qt.CheckState
        if isinstance(checked, Qt.CheckState):
            checked = (checked == Qt.CheckState.Checked)
        if self._checked != checked:
            self._checked = checked
            start = self._thumb_pos
            end = self._width - self._height + 2 if self._checked else 2
            self._animation.stop()
            self._animation.setStartValue(start)
            self._animation.setEndValue(end)
            self._animation.start()
            self.stateChanged.emit(self._checked)


    def isChecked(self) -> bool:
        """Return the current state of the toggle switch.
        
        Returns
        -------
        bool
            Returns checked state of the toggle switch
        """
        return self._checked

    def mousePressEvent(self, event):
        """
        Handles mouse press events to toggle the switch state when clicked.

        If the left mouse button is pressed, this method toggles the checked state of the switch.

        Parameters
        ----------
        event : QMouseEvent
            The mouse event triggered by the user interaction.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.setChecked(not self._checked)

    def sizeHint(self):
        """Returns the size of the toggle switch.
        
        Returns
        -------
        size : QSize
            Returns the size of the toggle switch.
        """
        return self.size()

    def paintEvent(self, event):
        """Draw the toggle switch.

        Draws the toggle switch.

        Parameters
        ----------
        event : QEvent
        """
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Draw background
            bg_color = QColor(self.bg_right_color if self._checked else self.bg_left_color)
            painter.setBrush(bg_color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(0, 0, self._width, self._height, self._height // 2, self._height // 2)


            # Draw the thumb (slider)
            thumb_diameter = self._height - 4
            painter.setBrush(QColor(self.fg_color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QRect(int(self._thumb_pos), 2, thumb_diameter, thumb_diameter))
        finally:
            painter.end()

    def get_thumb_pos(self):
        """Returns the thumb position."""
        return self._thumb_pos

    def set_thumb_pos(self, pos):
        """Sets the thumb position.
        
        Paramters
        ---------
        pos : int
            Thumb position"""
        self._thumb_pos = pos
        self.update()  # Redraw switch

    thumb_pos = pyqtProperty(float, get_thumb_pos, set_thumb_pos)


class CustomAction(QAction):
    """An action that changes icons when checked or the theme changes from light to dark

    Attributes
    ----------
    self._light_icon_unchecked : QIcon
        Icon for light, unchecked state
    self._light_icon_checked : QIcon
        Icon for light, checked state
    self._dark_icon_unchecked : QIcon
        Icon for dark, unchecked state
    self._dark_icon_checked : QIcon
        Icon for dark, checked state
    self._current_theme : str
        "light" or "dark" color theme

    Parameters
    ----------
    text: str
        Text to display by widget
    light_icon_unchecked : str
        Unchecked icon filename for light color theme.
    light_icon_checked : str | None
        Checked icon filename for light color theme.  If None, the icon is not checkable
    dark_icon_unchecked : str
        Unchecked icon filename for dark color theme.
    dark_icon_checked : str | None
        Checked icon filename for dark color theme. If None, the icon is not checkable
    button_size : int
        Size of button in pt.
    icon_size : int
        Size of icon on button in pt.
    parent : QToolButton
        Tool button to set icons.

    Methods
    -------
    set_theme()
        Updates light or dark theme icons
    update_icon()
        Update the icon based on the button's checked state.
    """
    def __init__(
        self,
        text: str,
        light_icon_unchecked: str,
        light_icon_checked: str | None=None,
        dark_icon_unchecked: str | None=None,
        dark_icon_checked: str | None=None,
        parent=None,
    ):
        super().__init__(text, parent)

        def load_icon(filename: str|None, fallback: QIcon=None) -> QIcon:
            """Sets up the QIcon for a given light/dark, checked/unchecked state.

            Parameters
            ----------
            filename : str | None
                Icon filename for a state
            fallback : QIcon, optional
                Fallback icon for a state, by default None

            Returns
            -------
            QIcon
                Icon to use for a given states
            """
            if filename:
                path = ICONPATH / filename
                if path.exists():
                    return QIcon(str(path))
                else:
                    print(f"[Warning] Icon not found: {path}")
            return fallback if fallback else QIcon()

        # Load icons
        self._light_icon_unchecked = load_icon(light_icon_unchecked)
        self._dark_icon_unchecked = load_icon(dark_icon_unchecked, self._light_icon_unchecked)

        if light_icon_checked:
            self.setCheckable(True)
            self._light_icon_checked = load_icon(light_icon_checked, self._light_icon_unchecked)
            self._dark_icon_checked = load_icon(dark_icon_checked, self._light_icon_checked)
        else:
            self.setCheckable(False)
            self._light_icon_checked = None
            self._dark_icon_checked = None

        self._current_theme = "light"

        # Button visual setup
        self.setFont(default_font())

        self.setIconVisibleInMenu(False)

        self.setChecked(False)
        self.update_icon()

        self.triggered.connect(self.update_icon)

    def set_theme(self, theme: str):
        """Updates the icon to light/dark theme."""
        if theme in ["light", "dark"]:
            self._current_theme = theme
            self.update_icon()

    def update_icon(self):
        """Update the icon based on the button's checked state and theme."""
        icon = None
        match self._current_theme:
            case "light":
                icon = self._light_icon_checked if self.isCheckable() and self.isChecked() else self._light_icon_unchecked
            case "dark":
                icon = self._dark_icon_checked if self.isCheckable() and self.isChecked() else self._dark_icon_unchecked

        if icon:
            self.setIcon(icon)
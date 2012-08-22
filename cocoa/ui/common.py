from xibless.textfield import Label, TextAlignment
from xibless.control import ControlSize
from xibless.font import Font, FontTrait
from xibless.color import Color

FIELD_LABEL_FONT = Font("Lucida Grande", 11, [FontTrait.Bold])
FIELD_LABEL_COLOR = Color(0x80, 0x80, 0x80) # light gray
PANEL_TITLE_FONT = Font("Lucida Grande", 18, [FontTrait.Bold])

class FieldLabel(Label):
    def __init__(self, parent, text):
        Label.__init__(self, parent, text)
        self.controlSize = ControlSize.Small
        self.font = FIELD_LABEL_FONT
        self.alignment = TextAlignment.Right
        self.textColor = FIELD_LABEL_COLOR

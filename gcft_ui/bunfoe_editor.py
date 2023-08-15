
import typing
from enum import Enum
import colorsys
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

from gclib import fs_helpers as fs
from gclib.bunfoe import BUNFOE, Field, fields

from gcft_ui.custom_widgets import BigIntSpinbox
from gclib.j3d import RGBA32

class BunfoeEditor(QWidget):
  field_value_changed = Signal()
  
  def clear_layout_recursive(self, layout: QLayout):
    while layout.count():
      item = layout.takeAt(0)
      widget = item.widget()
      if widget:
        widget.deleteLater()
      sublayout = item.layout()
      if sublayout:
        self.clear_layout_recursive(sublayout)
  
  def set_layout_disabled_recursive(self, layout: QLayout, disabled=True):
    for i in range(layout.count()):
      item = layout.itemAt(i)
      widget = item.widget()
      if widget:
        widget.setDisabled(disabled)
      sublayout = item.layout()
      if sublayout:
        self.set_layout_disabled_recursive(sublayout, disabled=disabled)
  
  def prettify_name(self, name: str, title: bool = True):
    pretty_name = name.replace("_", " ").strip()
    if title:
      pretty_name = pretty_name.title()
    return pretty_name
  
  def bunfoe_instance_selected(self, instance, text=None, disabled=False) -> QFormLayout:
    if text:
      self.ui.j3d_sidebar_label.setText(f"Showing {text}.") # TODO: remove or move elsewhere
    
    layout: QBoxLayout = self.ui.scrollAreaWidgetContents.layout()
    
    return self.add_all_widget_fields_to_layout(instance, layout, disabled=disabled)
  
  def add_all_widget_fields_to_layout(self, instance, layout: QBoxLayout, disabled=False):
    form_layout = QFormLayout()
    layout.addLayout(form_layout)
    
    for field in fields(instance):
      self.add_field_widget_to_form_layout(instance, field, form_layout, disabled=disabled)
    
    return form_layout
  
  def add_field_widget_to_form_layout(self, instance, field: Field, form_layout: QFormLayout, disabled=False):
    if field.name.startswith('_padding'):
      # No need to show these.
      return
    
    field_widget = self.make_widget_for_type(instance, field.type, [('attr', field.name)], disabled=disabled)
    if field_widget is None:
      # Field is not implemented.
      return
    
    pretty_field_name = self.prettify_name(field.name)
    
    form_layout.addRow(pretty_field_name, field_widget)
  
  def make_widget_for_type(self, instance, field_type: typing.Type, access_path: list[tuple], disabled=False):
    value = self.get_value(instance, access_path)
    
    if issubclass(field_type, int) and field_type in fs.PRIMITIVE_TYPE_TO_BYTE_SIZE:
      widget = self.make_spinbox_for_int(field_type, value)
    elif issubclass(field_type, float):
      widget = self.make_spinbox_for_float(field_type, value)
    elif issubclass(field_type, bool):
      widget = self.make_checkbox_for_bool(field_type, value)
    elif issubclass(field_type, fs.u16Rot):
      widget = self.make_spinbox_for_rotation(field_type, value)
    elif isinstance(field_type, typing.GenericAlias) and field_type.__origin__ in [fs.FixedStr, fs.MagicStr]:
      widget = self.make_line_edit_for_str(field_type, value)
    elif issubclass(field_type, Enum):
      widget = self.make_combobox_for_enum(field_type, value)
    elif isinstance(field_type, typing.GenericAlias) and field_type.__origin__ in [tuple, list]:
      tuple_layout = QHBoxLayout()
      for i, arg_type in enumerate(typing.get_args(field_type)):
        arg_widget = self.make_widget_for_type(instance, arg_type, access_path + [('item', i)])
        if isinstance(arg_widget, QWidget):
          tuple_layout.addWidget(arg_widget)
        elif isinstance(arg_widget, QLayout):
          tuple_layout.addLayout(arg_widget)
        else:
          raise NotImplementedError
      widget = tuple_layout
    elif issubclass(field_type, RGBA32):
      widget = self.make_button_for_color(field_type, value)
    elif issubclass(field_type, BUNFOE):
      sublayout = QVBoxLayout()
      widget = self.add_all_widget_fields_to_layout(value, sublayout, disabled=disabled)
      widget = sublayout
    else:
      print(f"Field type not implemented: {field_type}")
      raise NotImplementedError
    
    widget.setProperty('field_owner', instance)
    widget.setProperty('field_type', field_type)
    widget.setProperty('access_path', access_path)
    if isinstance(widget, QWidget):
      widget.setDisabled(disabled)
    elif isinstance(widget, QLayout):
      self.set_layout_disabled_recursive(widget, disabled=disabled)
    else:
      raise NotImplementedError
    return widget
  
  def get_value(self, instance, access_path: list[tuple]):
    for access_type, access_arg in access_path:
      if access_type == 'attr':
        instance = getattr(instance, access_arg)
      elif access_type == 'item':
        instance = instance[access_arg]
      else:
        raise NotImplementedError
    return instance
  
  def set_value(self, instance, access_path: list[tuple], value):
    for access_type, access_arg in access_path[:-1]:
      if access_type == 'attr':
        instance = getattr(instance, access_arg)
      elif access_type == 'item':
        instance = instance[access_arg]
      else:
        raise NotImplementedError
    
    access_type, access_arg = access_path[-1]
    if access_type == 'attr':
      setattr(instance, access_arg, value)
    elif access_type == 'item':
      instance[access_arg] = value
    else:
      raise NotImplementedError
  
  def make_checkbox_for_bool(self, field_type: typing.Type, value):
    checkbox = QCheckBox()
    checkbox.setChecked(value)
    checkbox.stateChanged.connect(self.checkbox_state_changed)
    return checkbox
  
  def checkbox_state_changed(self, state: int):
    checkbox: QCheckBox = self.sender()
    field_owner: object = checkbox.property('field_owner')
    access_path = checkbox.property('access_path')
    self.set_value(field_owner, access_path, checkbox.isChecked())
    self.field_value_changed.emit()
  
  def make_combobox_for_enum(self, field_type: typing.Type, value):
    combobox = QComboBox()
    
    for i, enum_value in enumerate(field_type):
      pretty_name = self.prettify_name(enum_value.name, title=False)
      combobox.addItem(pretty_name)
      combobox.setItemData(i, enum_value)
    
    if len(field_type) > 0:
      index_of_value = list(field_type).index(value)
      combobox.setCurrentIndex(index_of_value)
    
    combobox.currentIndexChanged.connect(self.combobox_value_changed)
    
    return combobox
  
  def combobox_value_changed(self, new_index: int):
    combobox: QComboBox = self.sender()
    enum_value = combobox.currentData()
    field_owner: object = combobox.property('field_owner')
    access_path = combobox.property('access_path')
    self.set_value(field_owner, access_path, enum_value)
    self.field_value_changed.emit()
  
  def make_spinbox_for_int(self, field_type, value):
    spinbox = BigIntSpinbox()
    assert field_type in fs.PRIMITIVE_TYPE_TO_BYTE_SIZE
    assert issubclass(field_type, int)
    min_val = 0
    byte_size = fs.PRIMITIVE_TYPE_TO_BYTE_SIZE[field_type]
    max_val = (1 << byte_size*8) - 1
    if fs.PRIMITIVE_TYPE_IS_SIGNED[field_type]:
      min_val -= 1 << (byte_size*8 - 1)
      max_val -= 1 << (byte_size*8 - 1)
    spinbox.setRange(min_val, max_val)
    spinbox.setWrapping(True)
    spinbox.setValue(value)
    spinbox.valueChanged.connect(self.spinbox_value_changed)
    return spinbox
  
  def make_spinbox_for_float(self, field_type, value):
    spinbox = QDoubleSpinBox()
    assert field_type == float
    spinbox.setRange(float('-inf'), float('inf'))
    spinbox.setValue(value)
    spinbox.valueChanged.connect(self.spinbox_value_changed)
    return spinbox
  
  def make_spinbox_for_rotation(self, field_type, value):
    # TODO: need a custom spinbox subclass for u16 rotations.
    assert field_type == fs.u16Rot
    return self.make_spinbox_for_int(fs.u16, value)
  
  def spinbox_value_changed(self, new_value):
    spinbox: QSpinBox = self.sender()
    field_owner: object = spinbox.property('field_owner')
    access_path = spinbox.property('access_path')
    self.set_value(field_owner, access_path, new_value)
    self.field_value_changed.emit()
  
  def make_line_edit_for_str(self, field_type, value):
    line_edit = QLineEdit()
    max_len = typing.get_args(field_type)[0]
    line_edit.setMaxLength(max_len)
    line_edit.setText(value)
    line_edit.editingFinished.connect(self.line_edit_value_changed)
    return line_edit
  
  def line_edit_value_changed(self):
    line_edit: QLineEdit = self.sender()
    field_owner: object = line_edit.property('field_owner')
    access_path = line_edit.property('access_path')
    new_value = line_edit.text()
    self.set_value(field_owner, access_path, new_value)
    self.field_value_changed.emit()
  
  def make_button_for_color(self, field_type, value: RGBA32):
    button = QPushButton()
    button.setText("Click to set color")
    button.clicked.connect(self.open_color_chooser)
    # TODO: set property to enable alpha or disable it, depending on the class of the color
    # or maybe we can just detect that from the existing 'field_type' property
    self.set_background_for_color_button(button, value)
    return button
  
  def set_background_for_color_button(self, button: QPushButton, color: RGBA32):
    # TODO: RGB support
    # if len(color) == 3:
    #   r, g, b = color
    #   a = 255
    # elif len(color) == 4:
    #   r, g, b, a = color
    # else:
    #   QMessageBox.warning(self, "Unknown color format", "Color is neither RGB nor RGBA.")
    #   return
    
    r, g, b = color.r, color.g, color.b
    
    # Depending on the value of the background color of the button, we need to make the text color either black or white for contrast.
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    if v > 0.5:
      text_color = (0, 0, 0)
    else:
      text_color = (255, 255, 255)
    
    button.setStyleSheet(
      "background-color: rgb(%d, %d, %d);" % (r, g, b) + \
      "color: rgb(%d, %d, %d);" % text_color,
    )
  
  def open_color_chooser(self):
    button: QPushButton = self.sender()
    field_owner: object = button.property('field_owner')
    access_path = button.property('access_path')
    
    color = self.get_value(field_owner, access_path)
    
    r, g, b = color.r, color.g, color.b
    a = 255
    has_alpha = True
    if has_alpha:
      a = color.a
    # TODO: RGB/RGBA support with field_type
    # has_alpha = False
    # if len(color) == 3:
    #   r, g, b = color
    #   a = 255
    # elif len(color) == 4:
    #   r, g, b, a = color
    #   has_alpha = True
    # else:
    #   QMessageBox.warning(self, "Unknown color format", "Color is neither RGB nor RGBA.")
    #   return
    
    initial_color = QColor(r, g, b, a)
    color_dialog_options = QColorDialog.ColorDialogOption(0)
    if has_alpha:
      color_dialog_options |= QColorDialog.ShowAlphaChannel
    qcolor = QColorDialog.getColor(initial_color, self, "Select color", options=color_dialog_options)
    if not qcolor.isValid():
      return
    
    color.r = qcolor.red()
    color.g = qcolor.green()
    color.b = qcolor.blue()
    if has_alpha:
      color.a = qcolor.alpha()
    
    self.set_background_for_color_button(button, color)
    self.field_value_changed.emit()

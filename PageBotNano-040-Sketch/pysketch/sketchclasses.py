#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#  S K E T C H A P P 2 P Y
#
#  Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#  www.pagebot.io
#  Licensed under MIT conditions
#
#  Supporting DrawBot, www.drawbot.com
#  Supporting Flat, xxyxyz.org/flat
#  Supporting Sketch, https://github.com/Zahlii/python_sketch_api
# -----------------------------------------------------------------------------
#
#  classes.py
#
#  Site page opening any sketch file format:
#  https://xaviervia.github.io/sketch2json/
#
#  https://gist.github.com/xaviervia/edbea95d321feacaf0b5d8acd40614b2
#  This description is not complete.
#  Additions made where found in the Reading specification of this context.
#
#  http://sketchplugins.com/d/87-new-file-format-in-sketch-43
#
#  This source will not import PageBot. But it is written in close
#  conntection to it, so PageBot can read/write Document and Element
#  instances into SketchApp files.
#
#  Webviewer
#  https://github.com/AnimaApp/sketch-web-viewer
#

import os
import zipfile
import json
import re
import io
import weakref
import time
from random import randint
from inspect import isclass, isfunction

FILETYPE_SKETCH = 'sketch' # SketchApp file extension
UNTITLED_SKETCH = 'untitled.' + FILETYPE_SKETCH # Name for untitled SketchFile.path
IMAGES_PATH = '_images/' # Path extension for image cache directory
DOCUMENT_JSON = 'document.json'
USER_JSON = 'user.json'
META_JSON = 'meta.json'
PAGES_JSON = 'pages/'
IMAGES_JSON = 'images/'
PREVIEWS_JSON = 'previews/' # Internal path for preview images

MS_IMMUTABLE_PAGE = 'MSImmutablePage' # MSJSONFileReference._ref_class value

# Translating Python-valid attribute names to JSON names for Sketch file.
JSON_ATTR_NAMES = dict(_from='from', _to='to')

# Defaults
BASE_FRAME = {}
POINT_ORIGIN = '{0, 0}'
BLACK_COLOR = dict(red=0, green=0, blue=0, alpha=1)
DEFAULT_FONT = 'Verdana'
DEFAULT_FONTSIZE = 12
DEFAULT_WIDTH = DEFAULT_HEIGHT = 100
DEFAULT_NAME = 'Untitled'

APP_VERSION = "61.2"
APP_ID = 'com.bohemiancoding.sketch3'

# SketchApp 43 files JSON types

'''
type UUID = string // with UUID v4 format

type SketchPositionString = string // '{0.5, 0.67135115527602085}'



type FilePathString = string

'''

POINT_PATTERN = re.compile('\{([e0-9\.\-]*), ([e0-9\.\-]*)\}')
  # type SketchPositionString = string // '{0.5, 0.67135115527602085}'

def newObjectID():
  """Answers a new random objectID in the pattern of existing ones.

  >>> len(newObjectID())
  36
  """
  t = ('%08X' % int(time.time()*100))[:8]
  id1 = ('%04X' % randint(0, 99999))[:4]
  id2 = ('%04X' % randint(0, 99999))[:4]
  id3 = ('%04X' % randint(0, 99999))[:4]
  id4 = ('%012X' % randint(0, 999999999999))[:12]
  return '%s-%s-%s-%s-%s' % (t, id1, id2, id3, id4)

class SketchAppBase:
  """Base class for SketchAppReader and SketchAppWriter."""

  def __init__(self, overwriteImages=False):
    self.overwriteImages = overwriteImages

class SketchBase:

  REPR_ATTRS = ['name'] # Attributes to be show in __repr__
  ATTRS = {}

  def __init__(self, **kwargs):
    """Using **kwargs, the attributes can be set as name values, as well as
    being used from dictionaries in the Sketch JSON file.

    >>>
    """
    self._class = self.CLASS # Forces values to default, in case it is not None
    self.parent = None # Save reference to parent layer as weakref.
    self.setAttributes(**kwargs)

  def setAttributes(self, **kwargs):
    """Expects keyword arguments of attrNames and (method_Or_SketchBaseClass,
    default) as value. This way the instance can be created from separate
    attributes, as well as the JSON dict that is read fron a Sketch file.
    Omitted attributes are initialized from the self.ATTRS class dictionary.

    >>> d = dict(x=100, y=200, width=300, height=400)
    >>> SketchRect(**d)
    <SketchRect x=100 y=200 w=300 h=400>
    >>> SketchRect(x=100, y=300)
    <SketchRect x=100 y=300 w=100 h=100>

    >>> frame = dict(x=20, y=30, w=100, h=200)
    >>> artboard = SketchArtboard(frame=frame)
    >>> artboard
    <SketchArtboard name=Artboard w=100 h=100>
    >>> artboard.frame
    <SketchRect x=20 y=30 w=100 h=100>

    >>> frame = dict(width=400, height=500)
    >>> page = SketchPage(frame=frame)
    >>> page.frame
    <SketchRect x=0 y=0 w=400 h=500>

    >>> frame = dict(x=10, y=20, width=30, height=40)
    >>> artboard = SketchArtboard(frame=frame)
    >>> artboard.frame
    <SketchRect x=10 y=20 w=30 h=40>
    """
    for name, value in kwargs.items():
        # If not part of the Sketch ATTRS attribute, just set value unchanged.
        if name not in self.ATTRS:
          setattr(self, name, value)

    for name, (m, value) in self.ATTRS.items(): # Create attribute, using method or class
      jsonName = JSON_ATTR_NAMES.get(name, name)
      if name in kwargs: # Valid if "_from" or "_to" are used as direct attribute names.
        value = kwargs[name]
      elif jsonName in kwargs: # In case "from" and "to" are used
        value = kwargs[jsonName]
      if isclass(m):
        if isinstance(value, m):
          pass # Already SketchBase instance, leave untouched
        elif value is None:
          value = m()
        elif not isinstance(value, dict):
          value = {name: value}
        else:
          value = m(**value)
      elif isfunction(m):
        value = m(value)
      setattr(self, name, value)

  def __repr__(self):
    s = ['<%s' % (self.__class__.__name__ or '')]
    for attrName in self.REPR_ATTRS:
      if hasattr(self, attrName):
        s.append('%s=%s' % (attrName, getattr(self, attrName)))
    return ' '.join(s) + '>'

  def __eq__(self, sko):
    """Answer if self and SketchBase object have the same attribute values.

    >>> p1 = SketchPoint(x=10, y=20)
    >>> p2 = SketchPoint(y=20, x=10)
    >>> p1 == p2
    True
    >>> p2.x = 100
    >>> p1 == p2
    False
    """
    if not isinstance(sko, self.__class__):
      return False
    for name in self.__dict__.keys():
      if getattr(self, name) != getattr(sko, name):
        #print('XXX', name, self, getattr(self, name), sko, getattr(sko, name))
        return False
    return True

  def __ne__(self, sko):
    return not (self == sko)

  def _get_parent(self):
    if self._parent is not None:
      return self._parent() # Get weakref to parent node
    return None
  def _set_parent(self, parent):
    if parent is not None:
      parent = weakref.ref(parent)
    self._parent = parent
  parent = property(_get_parent, _set_parent)

  def _get_root(self):
    """Answers the root (SketchFile instance) of self, searching upwards through
    the chain of parents. Answers None if no root can be found."""
    parent = self.parent # Expand weakref
    if parent is not None:
      return self.parent # Still searching in layer.parent sequence
    return None
  root = property(_get_root)

  def asDict(self):
    d = {}
    if self._class is not None:
      d['_class'] = self._class
    for attrName, (m, default) in self.ATTRS.items():
      d[attrName] = getattr(self, attrName)
    return d

  def find(self, _class=None, name=None, pattern=None, found=None):
    """SketchBase class does not have child layers. Just test if self matches.

    >>> p = SketchPoint(x=0, y=100)
    >>> p.find('point')[0] is p
    True
    >>> p.find(name='myPoint') # No name set, does not find
    []
    >>> p = SketchPoint(x=0, y=200, name='myPoint') # Set attribute, different from ATTRS
    >>> p.name
    'myPoint'
    >>> p.find(name='myPoint')[0] is p # Search by exact name
    True
    >>> p.find(name='myPts')# Search by exact name
    []
    >>> p.find(pattern='myPo')[0] is p # Search by name pattern
    True
    >>> p.find(_class=SketchPoint)[0] is p
    True
    >>> p.find(_class=SketchPoint.CLASS)[0] is p
    True
    """
    if found is None:
      found = []
    if (_class in (self.__class__, self.CLASS)) or \
       (name is not None and hasattr(self, 'name') and self.name == name) or \
       (pattern is not None and hasattr(self, 'name') and pattern in self.name):
      found.append(self)
    return found

  def asJson(self):
    d = {}
    for attrName in self.ATTRS.keys():
      attr = getattr(self, attrName)
      # Translate Python name to JSON name
      attrJsonName = JSON_ATTR_NAMES.get(attrName, attrName)
      if isinstance(attr, (list, tuple)):
        l = []
        for e in attr:
          if hasattr(e, 'asJson'):
            l.append(e.asJson())
          else:
            l.append(e)
        attr = l
      elif hasattr(attr, 'asJson'):
        attr = attr.asJson()
      if attr is not None:
        assert isinstance(attr, (dict, int, float, list, tuple, str)), attr
        d[attrJsonName] = attr
    if not d:
      return None
    if self.CLASS is not None:
      d['_class'] = self.CLASS

    return d


def asRect(sketchNestedPositionString):
  """type SketchNestedPositionString = string // '{{0, 0}, {75.5, 15}}'

  >>> asRect('{{0, 0}, {75.5, 15}}')
  (0, 0, 75.5, 15)
  >>> asRect('{{-100, 20000}, {75.5, 15}}')
  (-100, 20000, 75.5, 15)
  >>> asRect('{{-100, 1234a}, {75.5, 15}}') is None
  True
  """
  if sketchNestedPositionString is None:
    return None
  try:
    (x, y), (w, h) = POINT_PATTERN.findall(sketchNestedPositionString)
    return asNumber(x), asNumber(y), asNumber(w), asNumber(h)
  except ValueError:
    pass
  return None

def asColorNumber(v):
  try:
    return min(1, max(0, float(v)))
  except ValueError:
    return 0

def asNumber(v):
  """Answers the value interpreted as a value or None otherwise.

  >>> asNumber('123')
  123
  >>> asNumber('123.4')
  123.4
  >>> asNumber(123.4)
  123.4
  >>> asNumber('123a')
  0
  """
  try:
    number = float(v)
    if number == int(number):
      return int(number)
    return number
  except ValueError:
    return 0

def asInt(v):
  try:
    return int(v)
  except ValueError:
    return 0

def asBool(v):
  return bool(v)

def asId(v):
  return v

def asString(v):
  return str(v)

def asColorList(v):
  return []

def asGradientList(v):
  return []

def asImageCollection(v):
  return []

def asImages(v):
  return []

def asDict(v):
  return {}

def asList(v):
  return list(v)

def FontList(v):
  return []

def HistoryList(v):
  return ['NONAPPSTORE.57544']

def SketchCurvePointList(curvePointList):
  l = []
  for curvePoint in curvePointList:
    l.append(SketchCurvePoint(**curvePoint))
  return l

def SketchPositionString(v):
  """Sketch files keep points and rectangles as string. Decompose them here,
  before creating a real SketchPoint instance.

  >>> SketchPositionString('{0, 0}')
  <SketchPoint x=0 y=0>
  >>> SketchPositionString('{0000021, -12345}')
  <SketchPoint x=21 y=-12345>
  >>> SketchPositionString('{10.05, -10.66}')
  <SketchPoint x=10.05 y=-10.66>

  """
  sxy = POINT_PATTERN.findall(v)
  assert len(sxy) == 1 and len(sxy[0]) == 2, (sxy, v)
  return SketchPoint(x=asNumber(sxy[0][0]), y=asNumber(sxy[0][1]))

class SketchPoint(SketchBase):
  """Interprets the {x,y} string into a point2D.

  >>> SketchPoint(x=10, y=20)
  <SketchPoint x=10 y=20>
  >>> SketchPoint(x=21, y=-12345)
  <SketchPoint x=21 y=-12345>
  >>> SketchPoint(x=10.05, y=-10.66)
  <SketchPoint x=10.05 y=-10.66>
  """
  REPR_ATTRS = ['x', 'y'] # Attributes to be show in __repr__
  CLASS = 'point'

  def __init__(self, **kwargs):
    self._class = self.CLASS

    self.x = self.y = 0
    for attrName, value in kwargs.items():
      setattr(self, attrName, value)

  def asJson(self):
    return '{%s, %s}' % (self.x, self.y)

class SketchCurvePoint(SketchBase):
  """
  type SketchCurvePoint = {
    _class: 'curvePoint',
    do_objectID: UUID,
    cornerRadius: number,
    curveFrom: SketchPositionString, --> SketchPoint
    curveMode: number,
    curveTo: SketchPositionString, --> SketchPoint
    hasCurveFrom: bool,
    hasCurveTo: bool,
    point: SketchPositionString --> Point
  """
  CLASS = 'curvePoint'
  ATTRS = {
    'do_objectID': (asId, None),
    'cornerRadius': (asNumber, 0),
    'curveFrom': (SketchPositionString, POINT_ORIGIN),
    'curveMode': (asInt, 1),
    'curveTo': (SketchPositionString, POINT_ORIGIN),
    'hasCurveFrom': (asBool, False),
    'hasCurveTo': (asBool, False),
    'point': (SketchPositionString, POINT_ORIGIN),
  }

class SketchImageCollection(SketchBase):
  """
  _class: 'imageCollection',
  images: Unknown // TODO
  """
  CLASS = 'imageCollection'
  ATTRS = {
    'images': (asDict, {})
  }

class SketchColor(SketchBase):
  """
  _class: 'color',
  do_objectID: UUID,
  alpha: number,
  blue: number,
  green: number,
  red: number

  For more extended color functions see PageBot/toolbox/color

  >>> color = SketchColor(red=0.5, green=0.1, blue=1)
  >>> color.red
  0.5
  >>> sorted(color.asDict())
  ['_class', 'alpha', 'blue', 'do_objectID', 'green', 'red']
  """
  REPR_ATTRS = ['red', 'green', 'blue', 'alpha'] # Attributes to be show in __repr__
  CLASS = 'color'
  ATTRS = {
    'do_objectID': (asId, None),
    'red': (asColorNumber, 0),
    'green': (asColorNumber, 0),
    'blue': (asColorNumber, 0),
    'alpha': (asColorNumber, 0),
  }

class SketchBorder(SketchBase):
  """
  _class: 'border',
  isEnabled: bool,
  color: SketchColor,
  fillType: number,
  position: number,
  thickness: number

  For usage in PageBot, use equivalent PageBot/elements/Element.getBorderDict()

  >>> color = SketchColor(red=1)
  >>> color
  <SketchColor red=1 green=0 blue=0 alpha=0>
  >>> border = SketchBorder(color=color, fillType=1)
  >>> border.color
  <SketchColor red=1 green=0 blue=0 alpha=0>
  >>> border.fillType
  1
  """
  CLASS = 'border'
  ATTRS = {
    'isEnabled': (asBool, True),
    'color': (SketchColor, None),
    'fillType': (asInt, 0),
    'position': (asInt, 0),
    'thickness': (asNumber, 1)
  }

class SketchLayoutGrid(SketchBase):
  """
  + isEnabled: bool,
  + columnWidth: number,
  + drawHorizontal: bool,
  + drawHorizontalLines: bool,
  + drawVertical: bool,
  + gutterHeight: number,
  + gutterWidth: number,
  + guttersOutside: bool,
  + horizontalOffset: number,
  + numberOfColumns: number,
  + rowHeightMultiplication: number,
  + totalWidth: number,
  """
  CLASS = 'layoutGrid'
  ATTRS = {
    'isEnabled': (asBool, True),
    'columnWidth': (asNumber, 96),
    'drawHorizontal': (asBool, True),
    'drawHorizontalLines': (asBool, False),
    'drawVertical': (asBool, True),
    'gutterHeight': (asNumber, 24),
    'gutterWidth': (asNumber, 24),
    'guttersOutside': (asBool, False),
    'horizontalOffset': (asNumber, 60),
    'numberOfColumns': (asNumber, 5),
    'rowHeightMultiplication': (asNumber, 3),
    'totalWidth': (asNumber, 576),
  }

class SketchGradientStop(SketchBase):
  """
  _class: 'gradientStop',
  color: SketchColor,
  position: number

  >>> color = SketchColor(blue=1)
  >>> gs = SketchGradientStop(color=color, position=1)
  >>> gs.color, gs.position
  (<SketchColor red=0 green=0 blue=1 alpha=0>, 1)
  >>> gs = SketchGradientStop()
  >>> gs.color, gs.position
  (<SketchColor red=0 green=0 blue=0 alpha=1>, 0)
  """
  CLASS = 'gradientStop'
  ATTRS = {
    'color': (SketchColor, BLACK_COLOR),
    'position': (asNumber, 0),
  }

def SketchGradientStopList(dd):
  l = []
  for d in dd:
    l.append(SketchGradientStop(**d))
  return l

def sketchGradient(parent=None, **d):
  if d:
    return SketchGradient(parent=parent, **d)
  return None

class SketchGradient(SketchBase):
  """
  _class: 'gradient',
  elipseLength: number,
  from: SketchPositionString,
  gradientType: number,
  shouldSmoothenOpacity: bool,
  stops: [SketchGradientStop],
  to: SketchPositionString

  >>> g = SketchGradient()
  """
  CLASS = 'gradient'
  ATTRS = {
    'elipseLength': (asNumber, 0),
    '_from': (SketchPositionString, POINT_ORIGIN),  # Initilaizes to (0, 0)
    'gradientType': (asInt, 0),
    'shouldSmoothenOpacity': (asBool, True),
    'stops': (SketchGradientStopList, []),
    '_to': (SketchPositionString, POINT_ORIGIN),
  }

class SketchGraphicsContextSettings(SketchBase):
  """
  _class: 'graphicsContextSettings',
  blendMode: number,
  opacity: number
  """
  CLASS = 'graphicsContextSettings'
  ATTRS = {
    'blendMode': (asNumber, 0),
    'opacity': (asNumber, 1),
  }

'''
type SketchInnerShadow = {
  _class: 'innerShadow',
  isEnabled: bool,
  blurRadius: number,
  color: SketchColor,
  contextSettings: SketchGraphicsContextSettings,
  offsetX: 0,
  offsetY: 1,
  spread: 0
}
'''

def SketchMSJSONFileReferenceList(refs):
  l = []
  for ref in refs:
    if refs:
      l.append(SketchMSJSONFileReference(**ref))
  return l

def sketchMSJSONFileReference(refs):
  if refs: # Value data, otherwise answer None
    return SketchMSJSONFileReference(**refs)
  return None

class SketchMSJSONFileReference(SketchBase):
  """
  _class: 'MSJSONFileReference',
  _ref_class: 'MSImmutablePage' | 'MSImageData',
  _ref: FilePathString
  """
  CLASS = 'MSJSONFileReference'
  ATTRS = {
    '_ref_class': (asString, 'MSImageData'),
    '_ref': (asString, ''),
  }

def SketchFillList(sketchFills):
  l = []
  for fill in sketchFills:
    l.append(SketchFill(**fill))
  if l:
    return l
  return None # Ignore in output

class SketchFill(SketchBase):
  """
  _class: 'fill',
  isEnabled: bool,
  color: SketchColor,
  contextSettings: SketchGraphicsContextSettings
  image: SketchMSJSONFileReferenceList,
  fillType: number,
  gradient: sketchGradient,
  noiseIndex: number,
  noiseIntensity: number,
  patternFillType: number,
  patternTileScale: number
  """
  CLASS = 'fill'
  ATTRS = {
    'isEnabled': (asBool, True),
    'color': (SketchColor, BLACK_COLOR),
    'contextSettings': (SketchGraphicsContextSettings, {}),
    'fillType': (asInt, 0),
    'image': (sketchMSJSONFileReference, None), # Optional ignore otherwise
    'gradient': (sketchGradient, None), # Optional, ignore otherwise
    'noiseIndex': (asNumber, 0),
    'noiseIntensity': (asNumber, 0),
    'patternFillType': (asNumber, 1),
    'patternTileScale': (asNumber, 1),
  }

class SketchShadow(SketchBase):
  """
  _class: 'shadow',
  isEnabled: bool,
  blurRadius: number,
  color: SketchColor,
  contextSettings: SketchGraphicsContextSettings,
  offsetX: number,
  offsetY: number,
  spread: number
  """
  CLASS = 'shadow'
  ATTRS = {
    'isEnabled': (asBool, True),
    'blurRadius': (asNumber, 0),
    'color': (SketchColor, BLACK_COLOR),
    'contextSettings': (SketchGraphicsContextSettings, {}),
    'offsetX': (asNumber, 0),
    'offsetY': (asNumber, 0),
    'spread': (asNumber, 0),
  }

class SketchBlur(SketchBase):
  """
  _class: 'blur',
  isEnabled: bool,
  center: SketchPositionString,
  motionAngle: number,
  radius: number,
  _type: number
  """
  CLASS = 'blur'
  ATTRS = {
    'isEnabled': (asBool, True),
    'center': (SketchPositionString, POINT_ORIGIN),
    'motionAngle': (asNumber, 0),
    'radius': (asNumber, 0),
    'type': (asInt, 0),
  }

class SketchEncodedAttributes(SketchBase):
  """
  NSKern: number,
  MSAttributedStringFontAttribute: {
    _archive: Base64String,
  },
  NSParagraphStyle: {
    _archive: Base64String
  },
  NSColor: {
    _archive: Base64String
  }
  """
  CLASS = 'sketchEncodedAttributes'
  ATTRS = {}

class SketchRect(SketchBase):
  """
  _class: 'rect',
  + do_objectID: UUID,
  + constrainProportions: bool,
  + height: number,
  + width: number,
  + x: number,
  + y: number
  """
  REPR_ATTRS = ['x', 'y', 'w', 'h'] # Attributes to be show in __repr__
  CLASS = 'rect'
  ATTRS = {
    'do_objectID': (asId, None),
    'x': (asNumber, 0),
    'y': (asNumber, 0),
    'width': (asNumber, 100),
    'height': (asNumber, 100),
    'constrainProportions': (asBool, False),
  }
  def __getitem__(self, i):
    return (self.x, self.y, self.w, self.h)[i]

  def __iter__(self):
    for v in (self.x, self.y, self.w, self.h):
      yield v

  def _get_w(self):
    return self.width
  def _set_w(self, w):
    self.width = w
  w = property(_get_w, _set_w)

  def _get_h(self):
    return self.height
  def _set_h(self, h):
    self.height = h
  h = property(_get_h, _set_h)

class SketchTextStyle(SketchBase):
  """
  _class: 'textStyle',
  encodedAttributes: SketchEncodedAttributes
  """
  CLASS = 'textStyle'
  ATTRS = {
    'encodedAttributes': (SketchEncodedAttributes, None),
  }

class SketchBorderOptions(SketchBase):
  """
  _class: 'borderOptions',
  do_objectID: UUID,
  isEnabled: bool,
  dashPattern: [], // TODO,
  lineCapStyle: number,
  lineJoinStyle: number
  """
  CLASS = 'borderOptions'
  ATTRS = {
    'do_objectID': (asId, None),
    'isEnabled': (asBool, True),
    'dashPattern': (asString, ''),
    'lineCapStyle': (asNumber, 0),
    'lineJoinStyle': (asNumber, 0),
  }

class SketchColorControls(SketchBase):
  """
  _class: 'colorControls',
  isEnabled: bool,
  brightness: number,
  contrast: number,
  hue: number,
  saturation: number
  """
  CLASS = 'colorControls'
  ATTRS = {
    'isEnabled': (asBool, True),
    'brightness': (asNumber, 1),
    'contrast': (asNumber, 1),
    'hue': (asNumber, 1),
    'saturation': (asNumber, 1),
  }

def SketchBordersList(sketchBorders):
  l = []
  for sketchBorder in sketchBorders:
    l.append(SketchBorder(**sketchBorder))
  if l:
    return l
  return None

def SketchShadowsList(sketchShadows):
  l = []
  for sketchShadow in sketchShadows:
    l.append(SketchShadow(**sketchShadow))
  if l:
    return l
  return None

class SketchStyle(SketchBase):
  """
  _class: 'style',
  + do_objectID: UUID,
  blur: ?[SketchBlur],
  + borders: ?[SketchBorder],
  borderOptions: ?SketchBorderOptions,
  contextSettings: ?SketchGraphicsContextSettings,
  colorControls: ?SketchColorControls,
  endDecorationType: number,
  + fills: [SketchFill],
  innerShadows: [SketchInnerShadow],
  + miterLimit: number,
  + shadows: ?[SketchShadow],
  sharedObjectID: UUID,
  startDecorationType: number,
  textStyle: ?SketchTextStyle
  + endMarkerType: number,
  + startMarkerType: number,
  + windingRule: number,
  """
  CLASS = 'style'
  ATTRS = {
    'do_objectID': (asId, None),
    'endMarkerType': (asInt, 0),
    'borders': (SketchBordersList, []),
    'fills': (SketchFillList, []),
    'shadows': (SketchShadowsList, []),
    'miterLimit': (asInt, 10),
    'startMarkerType': (asInt, 0),
    'windingRule': (asInt, 1)
  }

class SketchSharedStyle(SketchBase):
  """
  _class: 'sharedStyle',
  do_objectID: UUID,
  name: string,
  value: SketchStyle
  """
  CLASS = 'sharedStyle'
  ATTRS = {
    'do_objectID': (asId, None),
    'name': (asString, 'Untitled'),
    'value': (SketchStyle, None),
  }

def SketchExportFormatList(exporFormats):
  l = []
  for exportFormat in exporFormats:
    l.append(SketchExportFormat(**exportFormat))
  return l

class SketchExportFormat(SketchBase):
  """
  _class: 'exportFormat',
  absoluteSize: number,
  fileFormat: string,
  name: string,
  namingScheme: number,
  scale: number,
  visibleScaleType: number
  """
  CLASS = 'exportFormat'
  ATTRS = {
    'absoluteSize': (asNumber, 1),
    'fileFormat': (asString, ''),
    'name': (asString, ''),
    'namingSchema': (asNumber, 0),
    'scale': (asNumber, 1),
    'visibleScaleType': (asNumber, 0),
  }

class SketchExportOptions(SketchBase):
  """
  _class: 'exportOptions',
  + do_objectID: UUID,
  + exportFormats: [SketchExportFormat],
  + includedLayerIds: [], // TODO
  + layerOptions: number,
  + shouldTrim: bool
  """
  CLASS = 'exportOptions'
  ATTRS = {
    'do_objectID': (asId, None),
    'exportFormats': (SketchExportFormatList, []),
    'layerOptions': (asInt, 0),
    'includedLayerIds': (asList, []),
    'shouldTrim': (asBool, False),
  }

class SketchSharedStyleContainer(SketchBase):
  """
  _class: 'sharedStyleContainer',
  objects: [SketchSharedStyle]
  """
  CLASS = 'sharedStyleContainer'
  ATTRS = {
    'objects': (asList, []),
  }

class SketchSymbolContainer(SketchBase):
  """
  _class: 'symbolContainer',
  objects: [] // TODO
  """
  CLASS = 'symbolContainer'
  ATTRS = {
    'objects': (asList, []),
  }

class SketchSharedTextStyleContainer(SketchBase):
  """
  _class: 'sharedTextStyleContainer',
  objects: [SketchSharedStyle]
  """
  CLASS = 'sharedTextStyleContainer'
  ATTRS = {
    'objects': (asList, []),
  }

class SketchAssetsCollection(SketchBase):
  """
  _class: 'assetCollection',
  colors: [], // TODO
  gradients: [], // TODO
  imageCollection: SketchImageCollection,
  images: [] // TODO
  """
  CLASS = 'assetCollection'
  ATTRS = {
    'colors': (asColorList, []),
    'gradients': (asGradientList, []),
    'imageCollection': (SketchImageCollection, []),
    'images': (asImages, []),
  }

class SketchCreated(SketchBase):
  """
  commit: string,
  appVersion: string,
  build: number,
  app: string,
  version: number,
  variant: string // 'BETA'
  compatibilityVersion': number,
  """
  CLASS = None
  ATTRS = {
    'commit': (asString, ''),
    'appVersion': (asString, APP_VERSION),
    'build': (asNumber, 0),
    'app': (asString, APP_ID),
    'version': (asInt, 0),
    'variant': (asString, ''),
    'compatibilityVersion': (asInt, 99)
  }

class SketchFontDescriptorAttributes(SketchBase):
  """
  name: string
  size: number
  """
  CLASS = None
  ATTRS = {
    'name': (asString, DEFAULT_FONT),
    'size': (asNumber, DEFAULT_FONTSIZE),
  }

class SketchFontDescriptor(SketchBase):
  """
  _class: 'fontDescriptor',
  attributes: SketchFontDescriptorAttributes
  """
  CLASS = 'fontDescriptor'
  ATTRS = {
    'attributes': (SketchFontDescriptorAttributes, {})
  }

class SketchParagraphStyle(SketchBase):
  """
  _class: 'paragraphStyle',
  alignment: number,
  minimumLineHeight: number,
  maximumLineHeight: number,
  paragraphSpacing: number,
  """
  CLASS = 'paragraphStyle'
  ATTRS = {
    'alignment': (asInt, 2),
    'minimumLineHeight': (asNumber, 0),
    'maximumLineHeight': (asNumber, 0),
    'paragraphSpacing': (asNumber, 1),
  }

class SketchAttributes(SketchBase):
  """
  MSAttributedStringFontAttribute: SketchFontDescriptor
  MSAttributedStringColorAttribute: SketchColor
  textStyleVerticalAlignmentKey: number
  kerning: number, # Wrong name for tracking.
  paragraphStyle: SketchParagraphStyle
  """
  CLASS = None
  ATTRS = {
    'MSAttributedStringFontAttribute': (SketchFontDescriptor, None),
    'MSAttributedStringColorAttribute': (SketchColor, BLACK_COLOR),
    'textStyleVerticalAlignmentKey': (asInt, 0),
    'kerning': (asNumber, 0), # Wrong name for tracking
    'paragraphStyle': (SketchParagraphStyle, {}),
  }

class SketchStringAttribute(SketchBase):
  """
  _class: 'stringAttribute';
  length: number,
  attributes: [SketchAttributes]
  """
  CLASS = 'stringAttribute'
  ATTRS = {
    'location': (asInt, 0),
    'length': (asInt, 0),
    'attributes': (SketchAttributes, None),
  }

def SketchStringAttributeList(stringAttributes):
  l = []
  for stringAttribute in stringAttributes:
    l.append(SketchStringAttribute(**stringAttribute))
  return l

class SketchAttributedString(SketchBase):
  """
  _class: 'attributedString',
  string: str,
  attributes: [StringAttribute],
  """
  CLASS = 'attributedString'
  ATTRS = {
    'string': (asString, ''),
    'attributes': (SketchStringAttributeList, [])
  }

class SketchRulerData(SketchBase):
  """
  _class: 'rulerData',
  + do_objectID: UUID,
  + base: number,
  + guides: [] // TODO
  """
  CLASS = 'rulerData'
  ATTRS = {
    'do_objectID': (asId, None),
    'base': (asInt, 0),
    'guides': (asList, []),
  }

class SketchText(SketchBase):
  """
  _class: 'text',
  do_objectID: UUID,
  exportOptions: SketchExportOptions,
  frame: SketchRect,
  isFlippedVertical: bool,
  isFlippedHorizontal: bool,
  isLocked: bool,
  isVisible: bool,
  layerListExpandedType: number,
  name: string,
  nameIsFixed: bool,
  originalObjectID: UUID,
  resizingType: number,
  rotation: number,
  shouldBreakMaskChain: bool,
  style: SketchStyle,
  attributedString: SketchAttributedString,
  automaticallyDrawOnUnderlyingPath: bool,
  dontSynchroniseWithSymbol: bool,
  glyphBounds: SketchNestedPositionString,
  heightIsClipped: bool,
  lineSpacingBehaviour: number,
  textBehaviour: number
  """
  CLASS = 'text'
  ATTRS = {
    'do_objectID': (asId, None),
    'booleanOperation': (asInt, -1),
    'exportOptions': (SketchExportOptions, {}),
    'frame': (SketchRect, BASE_FRAME),
    'isFixedToViewport': (asBool, False),
    'isFlippedHorizontal': (asBool, False),
    'isFlippedVertical': (asBool, False),
    'isLocked': (asBool, False),
    'isVisible': (asBool, True),
    'layerListExpandedType': (asInt, 0),
    'name': (asString, 'Untitled'),
    'nameIsFixed': (asBool, False),
    'resizingConstraint': (asInt, 47),
    'resizingType': (asInt, 0),
    'rotation': (asNumber, 0),
    'shouldBreakMaskChain': (asBool, False),
    'userInfo': (asDict, {}),
    'style': (SketchStyle, None),
    'attributedString': (SketchAttributedString, None),
    'automaticallyDrawOnUnderlyingPath': (asBool, False),
    'dontSynchroniseWithSymbol': (asBool, False),
    'glyphBounds': (asString, "{{0, 0}, {100, 100}}"),
    'lineSpacingBehaviour': (asInt, 2),
    'textBehaviour': (asInt, 0),
  }

class SketchLayer(SketchBase):
  """Abstract base layer class if there is an "self.layers" attributes."""
  def __init__(self, **kwargs):
    SketchBase.__init__(self, **kwargs)
    self._class = self.CLASS
    self.layers = [] # List of Sketch element instances.
    for layerDict in kwargs.get('layers', []):
      # Create new layer
      if not layerDict['_class'] in SKETCHLAYER_PY:
        print('SketchLayer: Layer class "%s" not implemented' % layerDict['_class'])
      else:
        self.layers.append(SKETCHLAYER_PY[layerDict['_class']](**layerDict))

  def __getitem__(self, layerIndex):
    """In case the layer has layers, then answer them by index."""
    return self.layers[layerIndex]

  def __len__(self):
    """Answer the number of layers that this SketchLayer is holding"""
    return len(self.layers)

  def append(self, layer):
    """Add layer to self.layers and set layer.parent to self.
    TODO: If layer.parent is already set, then remove it from its parent
    TODO: If layer is already in self.layers, then move it to end of the list.
    """
    assert isinstance(layer, SketchBase)
    self.layers.append(layer)
    layer.parent = self

  def find(self, _class=None, name=None, pattern=None, found=None):
    """Check if self matches class, name or pattern. Then search for
    all layers in self.layers.
    """
    found = SketchBase.find(self, _class=_class, name=name, pattern=pattern, found=found)
    for layer in self.layers:
        layer.find(_class=_class, name=name, pattern=pattern, found=found)
    return found

  def _get_artBoards(self):
    artBoards = []
    for layer in self.layers:
      if isinstance(layer, SketchArtboard):
        artBoards.append(layer)
    return artBoards
  artBoards = property(_get_artBoards)

  def asJson(self):
    """Get attributes from base as JSON dict."""
    d = SketchBase.asJson(self)
    d['layers'] = layers = [] # Add layers list
    for layer in self.layers:
      layers.append(layer.asJson())
    return d

class SketchSlice(SketchLayer):
  """
  _class: 'slice',
  + hasBackgroundColor: bool,
  + backgroundColor: SketchColor,
  + frame: SketchRect,
  """
  CLASS = 'slice'
  ATTRS = {
    'do_objectID': (asId, None),
    'frame': (SketchRect, BASE_FRAME),
    'backgroundColor': (SketchColor, None),
    'hasBackgroundColor': (asBool, False),
  }

class SketchShapeGroup(SketchLayer):
  """
  _class: 'shapeGroup',
  + do_objectID: UUID,
  + booleanOperation: number,
  + exportOptions: SketchExportOptions,
  + frame: SketchRect,
  + isFixedToViewport: bool,
  + isFlippedVertical: bool,
  + isFlippedHorizontal: bool,
  + isLocked: bool,
  + isVisible: bool,
  + layerListExpandedType: number,
  + name: string,
  + nameIsFixed: bool,
  + originalObjectID: UUID,
  + resizingConstraint: number,
  + resizingType: number,
  + rotation: number,
  + shouldBreakMaskChain: bool,
  + userInfo: {}
  + style: SketchStyle,
  + hasClickThrough: bool,
  # layers: [SketchLayer], # Implemented by inherited SketchLayer
  + clippingMaskMode: number,
  + hasClippingMask: bool,
  + windingRule: number
  """
  CLASS = 'shapeGroup'
  ATTRS = {
    'do_objectID': (asId, None),
    'booleanOperation': (asNumber, -1),
    'exportOptions': (SketchExportOptions, {}),
    'frame': (SketchRect, BASE_FRAME),
    'isFixedToViewport': (asBool, False),
    'isFlippedVertical': (asBool, False),
    'isFlippedHorizontal': (asBool, False),
    'isLocked': (asBool, False),
    'isVisible': (asBool, True),
    'layerListExpandedType': (asInt, 0),
    'name': (asString, ''),
    'nameIsFixed': (asBool, False),
    'originalObjectID': (asId, None),
    'resizingConstraint': (asInt, 63),
    'resizingType': (asInt, 0),
    'rotation': (asNumber, 0),
    'shouldBreakMaskChain': (asBool, False),
    'userInfo': (asDict, {}),
    'style': (SketchStyle, None),
    'hasClickThrough': (asBool, False),
    'clippingMaskMode': (asInt, 0),
    'hasClippingMask': (asBool, False),
    'windingRule': (asInt, 1),
    #'layers': (asList, []), # Implemented by inherited SketchLayer
  }

class SketchPath(SketchBase):
  """
  _class: 'path',
  isClosed: bool,
  points: [SketchCurvePoint]
  """
  CLASS = 'path'
  ATTRS = {
    'isClosed': (asBool, False),
    'points': (SketchCurvePointList, []),
  }

def SketchPathOptional(sketchPath):
  sp = SketchPath(**sketchPath)
  if sp.points: # Any points, then keep it
    return sp
  return None # Otherwise ignore the pat.

class SketchShapePath(SketchBase):
  """
  _class: 'shapePath',
  do_objectID: UUID,
  exportOptions: SketchExportOptions,
  frame: SketchRect,
  isFlippedVertical: bool,
  isFlippedHorizontal: bool,
  isLocked: bool,
  isVisible: bool,
  isClosed: bool
  layerListExpandedType: number,
  name: string,
  nameIsFixed: bool,
  resizingType: number,
  rotation: number,
  shouldBreakMaskChain: bool,
  booleanOperation: number,
  edited: bool,
  path: SketchPathOptional
  shouldBreakMaskChain: bool,
  edited: bool,
  pointRadiusBehaviour: number,
  points: SketchCurvePointList,
  path: SketchPathOptional,

  """
  CLASS = 'shapePath'
  ATTRS = {
    'do_objectID': (asId, None),
    'exportOptions': (SketchExportOptions, {}),
    'frame': (SketchRect, BASE_FRAME),
    'booleanOperation': (asInt, -1),
    'isFlippedHorizontal': (asBool, False),
    'isFlippedVertical': (asBool, False),
    'resizingConstraint': (asInt, 63), # ?? value
    'resizingType': (asBool, False),
    'isLocked': (asBool, False),
    'isVisible': (asBool, True),
    'isClosed': (asBool, False),
    'edited': (asBool, True),
    'rotation': (asNumber, 0),
    'layerListExpandedType': (asInt, 0),
    'name': (asString, ''),
    'nameIsFixed': (asBool, False),
    'shouldBreakMaskChain': (asBool, False),
    'pointRadiusBehaviour': (asInt, 1),
    'points': (SketchCurvePointList, []),
    'path': (SketchPathOptional, {}),
  }

class SketchArtboard(SketchLayer):
  """
  _class: 'artboard',
  + do_objectID: UUID,
  + booleanOperation: number,
  + exportOptions: SketchExportOptions,
  + frame: SketchRect,
  + isFixedToViewport: bool,
  + isFlippedHorizontal: bool,
  + isFlippedVertical: bool,
  + isLocked: bool,
  + isVisible: bool,
  + layerListExpandedType: number,
  + name: string,
  + nameIsFixed: bool,
  + resizingConstraint: number,
  + resizingType: number,
  + rotation: number,
  + shouldBreakMaskChain: bool,
  + style: SketchStyle,
  + hasClickThrough: bool,
  # layers: [SketchLayer], # Implemented by inherited SketchLayer
  + backgroundColor: SketchColor,
  + hasBackgroundColor: bool,
  + horizontalRulerData: SketchRulerData,
  + verticalRulerData: SketchRulerData,
  + includeBackgroundColorInExport: bool,
  + includeInCloudUpload: bool,
  + isFlowHome: (asBool, False),
  + userInfo: {}
  + layout: SketchLayoutGrid,
  + resizesContent: bool,
  """
  CLASS = 'artboard'
  ATTRS = {
    'do_objectID': (asId, None),
    'booleanOperation': (asInt, -1),
    'exportOptions': (SketchExportOptions, {}),
    'frame': (SketchRect, BASE_FRAME),
    'isFixedToViewport': (asBool, False),
    'isFlippedHorizontal': (asBool, False),
    'isFlippedVertical': (asBool, False),
    'isLocked': (asBool, False),
    'isVisible': (asBool, True),
    'layerListExpandedType': (asInt, 0),
    'name': (asString, 'Artboard'),
    'nameIsFixed': (asBool, False),
    'resizingConstraint': (asNumber, 63),
    'resizingType': (asInt, 0),
    'rotation': (asNumber, 0),
    'shouldBreakMaskChain': (asBool, False),
    'style': (SketchStyle, None),
    'hasClickThrough': (asBool, False),
    'backgroundColor': (SketchColor, None),
    'hasBackgroundColor': (asBool, False),
    'horizontalRulerData': (SketchRulerData, None),
    'verticalRulerData': (SketchRulerData, None),
    'isFlowHome': (asBool, False),
    'includeBackgroundColorInExport': (asBool, False),
    'includeInCloudUpload': (asBool, True),
    'layers': (asList, []),
    'userInfo': (asDict, {}),
    'layout': (SketchLayoutGrid, None),
    'resizesContent': (asBool, True),
  }
  def __repr__(self):
    return '<%s name=%s w=%d h=%d>' % (self.__class__.__name__, self.name, self.frame.w, self.frame.h)

class SketchBitmap(SketchBase):
  """
  _class: 'bitmap',
  + do_objectID: UUID,
  + booleanOperation: number,
  + exportOptions: SketchExportOptions,
  + frame: SketchRect,
  isFlippedHorizontal: bool,
  isFlippedVertical: bool,
  + isFixedToViewport: bool,
  isLocked: bool,
  isVisible: bool,
  intendedDPI:number,
  layerListExpandedType: number,
  name: string,
  nameIsFixed: bool,
  resizingConstraint: number,
  resizingType: number,
  rotation: number,
  shouldBreakMaskChain: bool,
  style: SketchStyle,
  userInfo: {}
  clippingMask: SketchNestedPositionString,
  fillReplacesImage: bool,
  image: SketchMSJSONFileReference,
  nineSliceCenterRect: SketchNestedPositionString,
  nineSliceScale: SketchPositionString
  """
  CLASS = 'bitmap'
  ATTRS = {
    'do_objectID': (asId, None),
    'booleanOperation': (asInt, -1),
    'exportOptions': (SketchExportOptions, {}),
    'frame': (SketchRect, BASE_FRAME),
    'isFlippedHorizontal': (asBool, False),
    'isFlippedVertical': (asBool, False),
    'isFixedToViewport': (asBool, False),
    'isLocked': (asBool, False),
    'isVisible': (asBool, True),
    'intendedDPI': (asNumber, 72),
    'layerListExpandedType': (asInt, 0),
    'name': (asString, ''),
    'resizingConstraint': (asNumber, 63),
    'nameIsFixed': (asBool, False),
    'resizingType': (asInt, 0),
    'rotation': (asNumber, 0),
    'shouldBreakMaskChain': (asBool, False),
    'style': (SketchStyle, None),
    'userInfo': (asDict, {}),
    'clippingMask': (asString, BASE_FRAME),
    'fillReplacesImage': (asBool, False),
    'image': (SketchMSJSONFileReference, None),
    'nineSliceCenterRect': (asRect, None),
    'nineSliceScale': (asRect, None)
  }

class SketchSymbolInstance(SketchBase):
  """
  _class: 'symbolInstance',
  do_objectID: UUID,
  exportOptions: SketchExportOptions,
  frame: SketchRect,
  isFlippedHorizontal: bool,
  isFlippedVertical: bool,
  isLocked: bool,
  isVisible: bool,
  layerListExpandedType: number,
  name: string,
  nameIsFixed: bool,
  resizingType: number,
  rotation: number,
  shouldBreakMaskChain: bool,
  style: SketchStyle,
  horizontalSpacing: number,
  masterInfluenceEdgeMaxXPadding: number,
  masterInfluenceEdgeMaxYPadding: number,
  masterInfluenceEdgeMinXPadding: number,
  masterInfluenceEdgeMinYPadding: number,
  symbolID: number,
  verticalSpacing: number,
  overrides: {
    "0": {} // TODO
  }
  """
  CLASS = 'symbolInstance'
  ATTRS = {
    'do_objectID': (asId, None),
    'exportOptions': (SketchExportOptions, {}),
    'frame': (SketchRect, BASE_FRAME),
    'isFlippedHorizontal': (asBool, False),
    'isFlippedVertical': (asBool, False),
    'isFixedToViewport': (asBool, False),
    'isLocked': (asBool, False),
    'isVisible': (asBool, True),
    'layerListExpandedType': (asInt, 0),
    'name': (asString, ''),
    'nameIsFixed': (asBool, False),
    'resizingType': (asInt, 0),
    'rotation': (asNumber, 0),
    'shouldBreakMaskChain': (asBool, False),
    'style': (SketchStyle, None),
    'horizontalSpacing': (asInt, 0), # Or {} ??
    'masterInfluenceEdgeMaxXPadding': (asNumber, 0),
    'masterInfluenceEdgeMaxYPadding': (asNumber, 0),
    'masterInfluenceEdgeMinXPadding': (asNumber, 0),
    'masterInfluenceEdgeMinYPadding': (asNumber, 0),
    'symbolID': (asId, None),
    'verticalSpacing': (asInt, 0), # Or {} ??
  }

class SketchGroup(SketchLayer):
  """
  _class: 'group',
  do_objectID: UUID,
  exportOptions: SketchExportOptions,
  frame: SketchRect,
  isFlippedHorizontal: bool,
  isFlippedVertical: bool,
  isLocked: bool,
  isVisible: bool,
  layerListExpandedType: number,
  name: string,
  nameIsFixed: bool,
  originalObjectID: UUID,
  resizingType: number,
  rotation: number,
  shouldBreakMaskChain: bool,
  hasClickThrough: bool,
  # layers: [SketchLayer] # Implemented by inherited SketchLayer
  """
  CLASS = 'group'
  ATTRS = {
    'do_objectID': (asId, None),
    'exportOptions': (SketchExportOptions, {}),
    'frame': (SketchRect, BASE_FRAME),
    'isFlippedHorizontal': (asBool, False),
    'isFlippedVertical': (asBool, False),
    'isLocked': (asBool, False),
    'isVisible': (asBool, True),
    'layerListExpandedType': (asInt, 0),
    'name': (asString, 'Group'),
    'nameIsFixed': (asBool, False),
    'originalObjectID': (asId, None),
    'resizingType': (asInt, 0),
    'rotation': (asNumber, 0),
    'shouldBreakMaskChain': (asBool, False),
    'hasClickThrough': (asBool, False),
  }

class SketchRectangle(SketchBase):
  """
  _class: 'rectangle',
  do_objectID: UUID,
  booleanOperation: number,
  exportOptions: SketchExportOptions,
  frame: SketchRect,
  isFixedToViewport': bool,
  isFlippedHorizontal: bool,
  isFlippedVertical: bool,
  isLocked: bool,
  isVisible: bool,
  layerListExpandedType: number,
  name: string,
  nameIsFixed: bool,
  resizingType: number,
  resizingConstraint: number,
  rotation: number,
  shouldBreakMaskChain: bool,
  edited: bool,
  isClosed: bool,
  pointRadiusBehaviour: number,
  points: CurvePointList,
  path: SketchPathOptional,
  fixedRadius: number,
  hasConvertedToNewRoundCorners: bool,
  style: SketchStyle,
  """
  CLASS = 'rectangle'
  ATTRS = {
    'do_objectID': (asId, None),
    'booleanOperation': (asInt, -1),
    'exportOptions': (SketchExportOptions, {}),
    'frame': (SketchRect, BASE_FRAME),
    'isFixedToViewport': (asBool, False),
    'isFlippedHorizontal': (asBool, bool),
    'isFlippedVertical': (asBool, bool),
    'isLocked': (asBool, bool),
    'isVisible': (asBool, bool),
    'layerListExpandedType': (asNumber, 0),
    'name': (asString, 'Rectangle'),
    'nameIsFixed': (asBool, bool),
    'resizingConstraint': (asNumber, 63),
    'resizingType': (asInt, 0),
    'rotation': (asNumber, 0),
    'shouldBreakMaskChain': (asBool, False),
    'edited': (asBool, False),
    'isClosed': (asBool, True),
    'pointRadiusBehaviour': (asInt, 0),
    'path': (SketchPathOptional, {}),
    'points': (SketchCurvePointList, []),
    'fixedRadius': (asNumber, 0),
    'hasConvertedToNewRoundCorners': (asBool, True),
    'style': (SketchStyle, None),
  }

class SketchOval(SketchBase):
  """
  _class: 'oval',
  do_objectID: UUID,
  exportOptions: SketchExportOptions,
  frame: SketchRect,
  isFlippedHorizontal: bool,
  isFlippedVertical: bool,
  isLocked: bool,
  isVisible: bool,
  layerListExpandedType: number,
  name: string,
  nameIsFixed: bool,
  resizingType: number,
  rotation: number,
  shouldBreakMaskChain: bool,
  booleanOperation: number,
  edited: bool,
  path: SketchPathOptional,
  """
  CLASS = 'oval'
  ATTRS = {
    'do_objectID': (asId, None),
    'booleanOperation': (asBool, -1),
    'exportOptions': (SketchExportOptions, {}),
    'frame': (SketchRect, BASE_FRAME),
    'isFixedToViewport': (asBool, False),
    'isFlippedHorizontal': (asBool, False),
    'isFlippedVertical': (asBool, False),
    'isLocked': (asBool, False),
    'isVisible': (asBool, True),
    'layerListExpandedType': (asInt, 0),
    'name': (asString, CLASS),
    'nameIsFixed': (asBool, False),
    'resizingConstraint': (asInt, 63),
    'resizingType': (asInt, 0),
    'rotation': (asNumber, 0),
    'shouldBreakMaskChain': (asBool, False),
    'edited': (asBool, False),
    'isClosed': (asBool, True),
    'pointRadiusBehaviour': (asInt, 1),
    'points': (SketchCurvePointList, []),
    'path': (SketchPathOptional, {}),
  }


class SketchStar(SketchBase):
  """
  _class: 'star',
  do_objectID: UUID,
  exportOptions: SketchExportOptions,
  frame: SketchRect,
  isFlippedHorizontal: bool,
  isFlippedVertical: bool,
  isLocked: bool,
  isVisible: bool,
  layerListExpandedType: number,
  name: string,
  nameIsFixed: bool,
  resizingType: number,
  rotation: number,
  shouldBreakMaskChain: bool,
  booleanOperation: number,
  edited: bool,
  path: SketchPathOptional,
  """
  CLASS = 'star'
  ATTRS = {
    'do_objectID': (asId, None),
    'booleanOperation': (asBool, -1),
    'exportOptions': (SketchExportOptions, {}),
    'frame': (SketchRect, BASE_FRAME),
    'isFixedToViewport': (asBool, False),
    'isFlippedHorizontal': (asBool, False),
    'isFlippedVertical': (asBool, False),
    'isLocked': (asBool, False),
    'isVisible': (asBool, True),
    'layerListExpandedType': (asInt, 0),
    'name': (asString, CLASS),
    'nameIsFixed': (asBool, False),
    'resizingConstraint': (asInt, 63),
    'resizingType': (asInt, 0),
    'rotation': (asNumber, 0),
    'shouldBreakMaskChain': (asBool, False),
    'edited': (asBool, False),
    'path': (SketchPathOptional, {}),
    'isClosed': (asBool, True),
    'pointRadiusBehaviour': (asInt, 1),
    'points': (SketchCurvePointList, []),
  }

class SketchPolygon(SketchBase):
  """
  _class: 'polygon',
  do_objectID: UUID,
  exportOptions: SketchExportOptions,
  frame: SketchRect,
  isFlippedHorizontal: bool,
  isFlippedVertical: bool,
  isLocked: bool,
  isVisible: bool,
  layerListExpandedType: number,
  name: string,
  nameIsFixed: bool,
  resizingType: number,
  rotation: number,
  shouldBreakMaskChain: bool,
  booleanOperation: number,
  edited: bool,
  path: SketchPathOptional
  """
  CLASS = 'polygon'
  ATTRS = {
    'do_objectID': (asId, None),
    'booleanOperation': (asBool, -1),
    'exportOptions': (SketchExportOptions, {}),
    'frame': (SketchRect, BASE_FRAME),
    'isFixedToViewport': (asBool, False),
    'isFlippedHorizontal': (asBool, False),
    'isFlippedVertical': (asBool, False),
    'isLocked': (asBool, False),
    'isVisible': (asBool, True),
    'layerListExpandedType': (asInt, 0),
    'name': (asString, CLASS),
    'nameIsFixed': (asBool, False),
    'resizingConstraint': (asInt, 63),
    'resizingType': (asInt, 0),
    'rotation': (asNumber, 0),
    'shouldBreakMaskChain': (asBool, False),
    'edited': (asBool, False),
    'isClosed': (asBool, True),
    'path': (SketchPathOptional, {}),
    'pointRadiusBehaviour': (asInt, 1),
    'points': (SketchCurvePointList, []),
  }

class SketchSymbolMaster(SketchBase):
  """
  _class: 'symbolMaster',
  backgroundColor: SketchColor,
  do_objectID: UUID,
  exportOptions: [SketchExportOptions],
  frame: SketchRect,
  hasBackgroundColor: bool,
  hasClickThrough: bool,
  horizontalRulerData: SketchRulerData,
  includeBackgroundColorInExport: bool,
  includeBackgroundColorInInstance: bool,
  includeInCloudUpload: bool,
  isFlippedHorizontal: bool,
  isFlippedVertical: bool,
  isLocked: bool,
  isVisible: bool,
  layerListExpandedType: number,
  #layers: SketchLayerList, # Implemented by inherited SketchLayer
  name: string,
  nameIsFixed: bool,
  resizingType: number,
  rotation: number,
  shouldBreakMaskChain: bool,
  style: SketchStyle,
  symbolID: UUID,
  verticalRulerData: SketchRulerData
  """
  CLASS = 'symbolMaster'
  ATTRS = {
    'backgroundColor': (SketchColor, None),
    'do_objectID': (asId, None),
    'exportOptions': (SketchExportOptions, []),
    'frame': (SketchRect, BASE_FRAME),
    'hasBackgroundColor': (asBool, False),
    'hasClickThrough': (asBool, False),
    'horizontalRulerData': (SketchRulerData, {}),
    'includeBackgroundColorInExport': (asBool, False),
    'includeBackgroundColorInInstance': (asBool, False),
    'includeInCloudUpload': (asBool, False),
    'isFlippedHorizontal': (asBool, False),
    'isFlippedVertical': (asBool, False),
    'isLocked': (asBool, False),
    'isVisible': (asBool, True),
    'layerListExpandedType': (asInt, 0),
    #layers: SketchLayerList, # Implemented by inherited SketchLayer
    'name': (asString, CLASS),
    'nameIsFixed': (asBool, False),
    'resizingType': (asNumber, 0),
    'rotation': (asNumber, 0),
    'shouldBreakMaskChain': (asBool, False),
    'style': (SketchStyle, None),
    'symbolID': (asId, None),
    'verticalRulerData': (SketchRulerData, {}),
  }

# Conversion of Sketch layer class name to Python class.
SKETCHLAYER_PY = {
  'text': SketchText,
  'slice': SketchSlice,
  'shapeGroup': SketchShapeGroup,
  'shapePath': SketchShapePath,
  'bitmap': SketchBitmap,
  'artboard': SketchArtboard,
  'symbolInstance': SketchSymbolInstance,
  'symbolMaster': SketchSymbolMaster,
  'group': SketchGroup,
  'rectangle': SketchRectangle,
  'oval': SketchOval,
  'star': SketchStar,
  'polygon': SketchPolygon,
}

# document.json
class SketchDocument(SketchBase):
  """
  _class: 'document',
  + do_objectID: UUID,
  + assets: SketchAssetsCollection,
  + colorSpace: number,
  + currentPageIndex: number,
  ? enableLayerInteraction: bool,
  ? enableSliceInteraction: bool,
  + foreignSymbols: [], // TODO
  + layerStyles: SketchSharedStyleContainer,
  + layerSymbols: SketchSymbolContainer,
  + layerTextStyles: SketchSharedTextStyleContainer,
  + pages: SketchMSJSONFileReferenceList,
  """
  CLASS = 'document'
  ATTRS = {
    'do_objectID': (asId, None),
    'assets': (SketchAssetsCollection, []),
    'colorSpace': (asInt, 0),
    'currentPageIndex': (asInt, 0),
    #'enableLayerInteraction': (asBool, False), ??
    #'enableSliceInteraction': (asBool, False), ??
    'foreignLayerStyles': (asList, []),
    'foreignSymbols': (asList, []),
    'foreignTextStyles': (asList, []),
    'layerStyles': (SketchSharedStyleContainer, {}),
    'layerSymbols': (SketchSymbolContainer, {}),
    'layerTextStyles': (SketchSharedTextStyleContainer, {}),
    'pages': (SketchMSJSONFileReferenceList, []),
  }

# pages/*.json
class SketchPage(SketchLayer):
  """
  _class: 'page',
  do_objectID: UUID,
  + booleanOperation: number,
  + exportOptions: SketchExportOptions,
  + frame: SketchRect,
  + hasClickThrough: bool,
  + horizontalRulerData: SketchRulerData,
  + includeInCloudUpload: bool,
  + isFlippedHorizontal: bool,
  + isFlippedVertical: bool,
  + isLocked: bool,
  + isVisible: bool,
  + layerListExpandedType: number,
  # layers: [SketchSymbolMaster], # Implemented by inherited SketchLayer
  + name: string,
  + nameIsFixed: bool,
  + resizingConstraint: number,
  + resizingType: number,
  + rotation: number,
  + shouldBreakMaskChain: bool,
  + style: SketchStyle,
  + verticalRulerData: SketchRulerData
  + userInfo: {},
  + clippingMaskMode: number,
}
  """
  CLASS = 'page'
  ATTRS = {
    'do_objectID': (asId, None),
    'booleanOperation': (asInt, -1),
    'frame': (SketchRect, BASE_FRAME),
    'exportOptions': (SketchExportOptions, {}),
    'hasClickThrough': (asBool, True),
    'includeInCloudUpload': (asBool, False),
    'isFlippedHorizontal': (asBool, False),
    'isFlippedVertical': (asBool, False),
    'isLocked': (asBool, False),
    'isVisible': (asBool, True),
    'layerListExpandedType': (asInt, 0),
    'name': (asString, 'Untitled'),
    'nameIsFixed': (asBool, False),
    'resizingConstraint': (asNumber, 63),
    'resizingType': (asInt, 0),
    'rotation': (asNumber, 0),
    'shouldBreakMaskChain': (asBool, False),
    'style': (SketchStyle, None),
    'verticalRulerData': (SketchRulerData, None),
    'horizontalRulerData': (SketchRulerData, None),
    'userInfo': (asDict, {}),
    'clippingMaskMode': (asInt, 0),
  }

# meta.json
class SketchMeta(SketchBase):
  """
  commit: string,
  appVersion: string,
  build: number,
  app: string,
  pagesAndArtboards: {
    [key: UUID]: { name: string }
  },
  fonts: [string], // Font names
  version: number,
  saveHistory: [ string ], // 'BETA.38916'
  autosaved: number,
  variant: string // 'BETA'
  compatibilityVersion': number,
  """
  CLASS = None
  ATTRS = {
    'commit': (asString, ''),
    'appVersion': (asString, APP_VERSION),
    'build': (asNumber, 0),
    'app': (asString, APP_ID),
    'pagesAndArtboards': (asList, []), # To be filled by self.__init__
    'fonts': (FontList, []), # Font names
    'version': (asInt, 0),
    'saveHistory': (HistoryList, []), # 'BETA.38916'
    'autosaved': (asInt, 0),
    'variant': (asString, ''),
    'created': (SketchCreated, {}),
    'compatibilityVersion': (asInt, 99),
  }

  def __init__(self, **kwargs):
    SketchBase.__init__(self, **kwargs)
    self.pagesAndArtboards = {} # Dictionary of Sketch element instances.
    for pageId, page in self.root.pages.items():
      # Create page or artboard reference
      artboards = {}
      self.pagesAndArtboards[page.do_objectID] = dict(name=page.name, artboards=artboards)
      for layer in page.layers:
        if layer._class == 'artboard':
          artboards[layer.do_objectID] = dict(name=layer.name)

# user.json
class SketchUser(SketchBase):
  """
  [key: SketchPageId]: {
    scrollOrigin: SketchPositionString,
    zoomValue: number
  },
  [key: SketchDocumentId]: {
    pageListHeight: number,
    cloudShare: Unknown // TODO
  }
  """
  CLASS = 'user'
  ATTRS = {
  }
  def __init__(self, **kwargs):
    SketchBase.__init__(self, **kwargs)
    self.document = dict(pageListHeight=118)

  def asJson(self):
    return dict(document=dict(pageListHeight=self.document['pageListHeight']))

class SketchFile(SketchBase):
  """Holds entire data file. Top of layer.parent-->layer.parent-->sketchFile chain.
  """
  ATTRS = {
    'pages': (asDict, {}),
    'document': (SketchDocument, None),
    'user': (SketchUser, None),
    'meta': (SketchMeta, None),
  }
  def __init__(self, path=None):
    self.path = path or UNTITLED_SKETCH
    self.pages = {}
    self.document = None
    self.user = None
    self.meta = None

  def __repr__(self):
    return '<%s path=%s>' % (self.__class__.__name__, self.path.split('/')[-1])

  def find(self, _class=None, name=None, pattern=None):
    found = []
    for pageId, page in self.pages.items():
      page.find(_class=_class, name=name, pattern=pattern, found=found)
    return found

  def _get_orderedPages(self):
    """Answer a list of pages in the order of the self.document.pages"""
    orderedPages = []
    for pageRef in self.document.pages:
      if pageRef._ref_class == MS_IMMUTABLE_PAGE:
        pageId = pageRef._ref.split('/')[-1]
        orderedPages.append(self.pages[pageId])
    return orderedPages
  orderedPages = property(_get_orderedPages)

  def _get_imagesPath(self):
    """Answer the _images/ path, related to self.path

    >>> SketchFile('/a/b/c/d.sketch').imagesPath
    '/a/b/c/d_images/'
    >>> SketchFile('d.sketch').imagesPath
    'd_images/'
    >>> SketchFile('a/b/c').imagesPath
    'a/b/c/_images/'
    >>> SketchFile().imagesPath
    'untitled_images/'
    """
    path = self.path
    if path.endswith('.' + FILETYPE_SKETCH):
      parts = path.split('/')
      if len(parts) > 1:
        imagesPath = '/'.join(parts[:-1]) + '/'
      else:
        imagesPath = ''
      imagesPath += (parts[-1].replace('.'+FILETYPE_SKETCH, '')) + IMAGES_PATH
    else:
      if not path.endswith('/'):
        path += '/'
      imagesPath = path + IMAGES_PATH
    return imagesPath
  imagesPath = property(_get_imagesPath) # Read only


if __name__ == '__main__':
  import doctest
  import sys
  sys.exit(doctest.testmod()[0])

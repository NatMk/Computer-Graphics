# Kebede, Natnael M.
# nmk9004
# 2018-10-26

#----------------------------------------------------------------------
# This code was originally created by Prof. Farhad Kamangar.
# It has been significantly modified and updated by Brian A. Dalio for
# use in CSE 4303 / CSE 5365 in the 2018 Fall semester.

#----------------------------------------------------------------------
import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog

import myGraphics as Graphics
#DataPopulation is an instanace of ModelData class form ModelData.py
import ModelData as DataPopulation
import os
#width and height of the canvas
width = 0; height = 0; DataSet = 0
#----------------------------------------------------------------------
class cl_widgets :
  def __init__( self, ob_root_window, ob_world = [] ) :
    self.ob_root_window = ob_root_window
    self.ob_world = ob_world

    self.menu = cl_menu( self )

    self.toolbar = cl_toolbar( self )

    self.statusBar_frame = cl_statusBar_frame( self.ob_root_window )
    self.statusBar_frame.pack( side = tk.BOTTOM, fill = tk.X )
    self.statusBar_frame.set( 'This is the status bar' )

    self.ob_canvas_frame = cl_canvas_frame( self )
    self.ob_world.add_canvas( self.ob_canvas_frame.canvas )

#----------------------------------------------------------------------
class cl_canvas_frame :
  def __init__( self, master ) :
    self.master = master
    self.canvas = tk.Canvas(
      master.ob_root_window, width=1, height=1, bg='purple' )

    self.canvas.pack( expand=tk.YES, fill=tk.BOTH )
    self.canvas.bind( '<Configure>',       self.canvas_resized_callback )
    self.canvas.bind( '<ButtonPress-1>',   self.left_mouse_click_callback )
    self.canvas.bind( '<ButtonRelease-1>', self.left_mouse_release_callback )
    self.canvas.bind( '<B1-Motion>',       self.left_mouse_down_motion_callback )
    self.canvas.bind( '<ButtonPress-2>',   self.middle_mouse_click_callback )
    self.canvas.bind( '<ButtonRelease-2>', self.middle_mouse_release_callback )
    self.canvas.bind( '<B2-Motion>',       self.middle_mouse_down_motion_callback )
    self.canvas.bind( '<ButtonPress-3>',   self.right_mouse_click_callback )
    self.canvas.bind( '<ButtonRelease-3>', self.right_mouse_release_callback )
    self.canvas.bind( '<B3-Motion>',       self.right_mouse_down_motion_callback )
    self.canvas.bind( '<Key>',             self.key_pressed_callback )
    self.canvas.bind( '<Up>',              self.up_arrow_pressed_callback )
    self.canvas.bind( '<Down>',            self.down_arrow_pressed_callback )
    self.canvas.bind( '<Right>',           self.right_arrow_pressed_callback )
    self.canvas.bind( '<Left>',            self.left_arrow_pressed_callback )
    self.canvas.bind( '<Shift-Up>',        self.shift_up_arrow_pressed_callback )
    self.canvas.bind( '<Shift-Down>',      self.shift_down_arrow_pressed_callback )
    self.canvas.bind( '<Shift-Right>',     self.shift_right_arrow_pressed_callback )
    self.canvas.bind( '<Shift-Left>',      self.shift_left_arrow_pressed_callback )

  def key_pressed_callback( self, event ) :
    msg = f'{event.char!r} ({ord( event.char )})' \
      if len( event.char ) > 0 else '<non-printing char>'

    self.master.statusBar_frame.set(
      f'{msg} pressed at ({event.x},{event.y})' )

  def up_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Up arrow pressed' )

  def down_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Down arrow pressed' )

  def right_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Right arrow pressed' )

  def left_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Left arrow pressed' )

  def shift_up_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Shift up arrow pressed' )

  def shift_down_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Shift down arrow pressed' )

  def shift_right_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Shift right arrow pressed' )

  def shift_left_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Shift left arrow pressed' )

  def left_mouse_click_callback( self, event ) :
    self.master.statusBar_frame.set( f'LMB down. ({event.x}, {event.y})' )
    self.x = event.x
    self.y = event.y
    self.canvas.focus_set()

  def left_mouse_release_callback( self, event ) :
    self.master.statusBar_frame.set( f'LMB released. ({event.x}, {event.y})' )
    self.x = None
    self.y = None

  def left_mouse_down_motion_callback( self, event ) :
    self.master.statusBar_frame.set( f'LMB dragged. ({event.x}, {event.y})' )
    self.x = event.x
    self.y = event.y

  def middle_mouse_click_callback( self, event ) :
    self.master.statusBar_frame.set( f'MMB down. ({event.x}, {event.y})' )
    self.x = event.x
    self.y = event.y
    self.canvas.focus_set()

  def middle_mouse_release_callback( self, event ) :
    self.master.statusBar_frame.set( f'MMB released. ({event.x}, {event.y})' )
    self.x = None
    self.y = None

  def middle_mouse_down_motion_callback( self, event ) :
    self.master.statusBar_frame.set( f'MMB dragged. ({event.x}, {event.y})' )
    self.x = event.x
    self.y = event.y

  def right_mouse_click_callback( self, event ) :
    self.master.statusBar_frame.set( f'RMB down. ({event.x}, {event.y})' )
    self.x = event.x
    self.y = event.y

  def right_mouse_release_callback( self, event ) :
    self.master.statusBar_frame.set( f'RMB released. ({event.x}, {event.y})' )
    self.x = None
    self.y = None

  def right_mouse_down_motion_callback( self, event ) :
    self.master.statusBar_frame.set( f'RMB dragged. ({event.x}, {event.y})' )
    self.x = event.x
    self.y = event.y

  def canvas_resized_callback( self, event ) :
    global width; global height
    self.canvas.config( width = event.width-4, height = event.height-4 )

    self.master.statusBar_frame.pack( side = tk.BOTTOM, fill = tk.X )
    self.master.statusBar_frame.set(
      f'Canvas width, height ({self.canvas.cget( "width" )}, ' +
      f'{self.canvas.cget( "height" )})' )

    self.canvas.pack()
    self.master.ob_world.redisplay( self.master.ob_canvas_frame.canvas, event )

    # Get the current canvas width and height
    width = int(self.canvas.cget("width")); height = int(self.canvas.cget("height"))


#----------------------------------------------------------------------
class cl_statusBar_frame( tk.Frame ) :
  def __init__( self, master ) :
    tk.Frame.__init__( self, master )
    self.label = tk.Label( self, bd = 1, relief = tk.SUNKEN, anchor = tk.W )
    self.label.pack( fill = tk.X )

  def set( self, formatStr, *args ) :
    str_name = "nmk9004: "
    self.label.config(text = str_name + formatStr % args)
    self.label.update_idletasks()

  def clear( self ) :
    self.label.config( text='' )
    self.label.update_idletasks()

#----------------------------------------------------------------------
class cl_menu :
  def __init__( self, master ) :
    self.master = master
    self.menu = tk.Menu( master.ob_root_window )
    master.ob_root_window.config( menu = self.menu )

    self.filemenu = tk.Menu( self.menu )
    self.menu.add_cascade( label = 'File', menu = self.filemenu )
    self.filemenu.add_command( label = 'New', command = lambda : self.menu_callback( 'file>new' ) )
    self.filemenu.add_command( label = 'Open...', command = lambda : self.menu_callback( 'file>open' ) )
    self.filemenu.add_separator()
    self.filemenu.add_command( label = 'Exit', command = lambda : self.menu_callback( 'file>exit' ) )

    self.dummymenu = tk.Menu( self.menu )
    self.menu.add_cascade( label = 'Settings', menu = self.dummymenu )
    self.dummymenu.add_command( label = 'Item1', command = lambda : self.menu_callback( 'settings>item1' ) )
    self.dummymenu.add_command( label = 'Item2', command = lambda : self.menu_callback( 'settings>item2' ) )

    self.helpmenu = tk.Menu( self.menu )
    self.menu.add_cascade( label = 'Help', menu = self.helpmenu )
    self.helpmenu.add_command( label = 'About...', command = lambda : self.menu_callback( 'help>about' ) )

  def menu_callback( self, which = None ) :
    item = 'menu' if which is None else which
    self.master.statusBar_frame.set( f'{item!r} callback' )

#----------------------------------------------------------------------
class cl_toolbar :
  def __init__( self, master ) :
    self.master = master
    self.toolbar = tk.Frame( master.ob_root_window )
    self.button = tk.Button( self.toolbar, text = 'Reset', width = 16, command = self.toolbar_reset_callback )
    self.button.pack( side = tk.LEFT, padx = 2, pady = 2 )
    self.button = tk.Button( self.toolbar, text = 'Load', width = 16, command = self.toolbar_load_callback )
    self.button.pack( side = tk.LEFT, padx = 2, pady = 2 )
    self.button = tk.Button( self.toolbar, text = 'Draw', width = 16, command = self.toolbar_draw_callback )
    self.button.pack( side = tk.LEFT, padx = 2, pady = 2 )
    self.toolbar.pack( side = tk.TOP, fill = tk.X )

  def toolbar_reset_callback( self ) :
    self.master.ob_world.reset()
    #self.master.statusBar_frame.set('Reset callback')
    self.master.statusBar_frame.set('Display Cleared')

  def toolbar_load_callback( self ) :
    global DataSet
    #self.master.statusBar_frame.set('Load callback')
    #fName is the path of the file and we get a filename and (if the user didn't CANCEL)
    fName = tk.filedialog.askopenfilename(filetypes=[("allfiles", "*")])
    if ( len(fName) ) == 0:
      #user did not select a file to load
      self.master.statusBar_frame.set("%s","[Load was cancelled]")
    else:
      #file_name is the filename itself (such us file.txt)
      file_name = os.path.basename(fName)
      self.master.statusBar_frame.set("%s" + " is Loaded ",file_name)
      # Dataset is a variable to store DataPopulation results
      # we load the mesh by making (and saving) an instance of ModelData
      DataSet = DataPopulation.ModelData(file_name)
      viewport = DataSet.getViewport()
      window = DataSet.getWindow()
      #print(window) print(viewport) print('Bounding box:', DataSet.getBoundingBox())

  def toolbar_draw_callback( self ) :
    global DataSet;
    #self.master.statusBar_frame.set( 'Draw callback' )

    if DataSet == 0:
      return #Return at once if a mesh hasn't been loaded.
    else:
      self.master.statusBar_frame.set('Drawing...')
      #Get the Window and Viewport info from the ModelData instance.
      w  = DataSet.getWindow(); v =  DataSet.getViewport()
      #Construct the transform using constructTransform()
      (ax, ay, sx, sy) = DataPopulation.constructTransform(w, v, width, height)
      #Specify the transform to the ModelData instance.
      DataSet.specifyTransform(ax, ay, sx, sy)
      #print(f' width {width} height {height}')
      #print(f' ax {ax: .3f} ay {ay: .3f} sx {sx: .3f} sy {sy: .3f}')
      #Invoke the create_graphic_objects() method, passing the canvas and the ModelData instance.
      self.master.ob_world.create_graphic_objects(self.master.ob_canvas_frame.canvas, DataSet)


#----------------------------------------------------------------------


# Kebede, Natnael M.
# nmk9004
# 2018-10-5

#----------------------------------------------------------------------
# This code was originally created by Prof. Farhad Kamangar.
# It has been significantly modified and updated by Brian A. Dalio for
# use in CSE 4303 / CSE 5365 in the 2018 Fall semester.

#----------------------------------------------------------------------
class cl_world :
  def __init__( self, objects = [], canvases = [] ) :
    self.objects = objects
    self.canvases = canvases

  def add_canvas( self, canvas ) :
    self.canvases.append( canvas )
    canvas.world = self

  def reset( self ) :
    self.objects = []
    for canvas in self.canvases :
      canvas.delete( 'all' )

  def create_graphic_objects( self, canvas ) :
    # 1. Create a line that goes from the upper left
    #    to the lower right of the canvas.
    self.objects.append( canvas.create_line(
      0, 0, canvas.cget( 'width' ), canvas.cget( 'height' ) ) )

    # 2. Create a line that goes from the lower left
    #    to the upper right of the canvas.
    self.objects.append( canvas.create_line(
      canvas.cget( 'width' ), 0, 0, canvas.cget( 'height' ) ) )

    # 3. Create an oval that is centered on the canvas and
    #    is 50% as wide and 50% as high as the canvas.
    self.objects.append( canvas.create_oval(
      int( 0.25 * int( canvas.cget( 'width' ) ) ),
      int( 0.25 * int( canvas.cget( 'height' ) ) ),
      int( 0.75 * int( canvas.cget( 'width' ) ) ),
      int( 0.75 * int( canvas.cget( 'height' ) ) ) ) )

  def redisplay( self, canvas, event ) :
    if self.objects :
      canvas.coords(self.objects[ 0 ], 0, 0, event.width, event.height )
      canvas.coords(self.objects[ 1 ], event.width, 0, 0, event.height )
      canvas.coords(self.objects[ 2 ],
        int( 0.25 * int( event.width ) ),
        int( 0.25 * int( event.height ) ),
        int( 0.75 * int( event.width ) ),
        int( 0.75 * int( event.height ) ) )

#----------------------------------------------------------------------

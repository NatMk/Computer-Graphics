# Kebede, Natnael M.
# nmk9004
# 2018-10-26

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

  def create_graphic_objects( self, canvas, DataSet) :

    viewport = DataSet.getViewport(); face = DataSet.getFaces()

    #Draw the Viewport rectangle.
    self.objects.append(canvas.create_rectangle
                        (float(viewport[0]) * float(canvas.cget("width")),
                         float(viewport[1]) * float(canvas.cget("height")),
                         float(viewport[2]) * float(canvas.cget("width")),
                         float(viewport[3]) * float(canvas.cget("height"))))

    for i in range(len(face)):
      #temporary values to store each face value and the transformed value respectively
       temp1 = face[i][0]; temp2 = face[i][1]; temp3 = face[i][2]
       #For each face from the ModelData instance, get the three vertex numbers for that face then Get from the
       # ModelData instance the transformed vertex coordinates.

       #vertice 1 (x, y) for the first face value
       x1 = DataSet.getTransformedVertex(temp1)[0]; y1 = DataSet.getTransformedVertex(temp1)[1]
       #vertice 2 (x, y) for the second face value
       x2 = DataSet.getTransformedVertex(temp2)[0]; y2 = DataSet.getTransformedVertex(temp2)[1]
       #vertice 3 (x, y) for the third face value
       x3 = DataSet.getTransformedVertex(temp3)[0]; y3 = DataSet.getTransformedVertex(temp3)[1]

       #draw three lines, v1->v2, v2->v3, and v3->v1
       self.objects.append(canvas.create_line( (x1,y1),(x2,y2),(x3,y3),(x1,y1) ) )

  def redisplay( self, canvas, event ) :
    pass

#----------------------------------------------------------------------

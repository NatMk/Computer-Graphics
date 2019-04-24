# Kebede, Natnael M.
# nmk9004
# 2018-10-26

#----------------------------------------------------------------------
# This code was originally created by Prof. Farhad Kamangar.
# It has been significantly modified and updated by Brian A. Dalio for
# use in CSE 4303 / CSE 5365 in the 2018 Fall semester.

#----------------------------------------------------------------------
from CohenSutherland import clipLine

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

  def create_graphic_objects(self, canvas, DataSet, doClip = False, doPerspective = False) :

     viewport = DataSet.getViewport(); faces = DataSet.getFaces()
     portal = []

    #Draw the Viewport rectangle.
     self.objects.append(canvas.create_rectangle
                        (float(viewport[0]) * float(canvas.cget("width")),
                         float(viewport[1]) * float(canvas.cget("height")),
                         float(viewport[2]) * float(canvas.cget("width")),
                         float(viewport[3]) * float(canvas.cget("height"))))

     # create an array to store the xmin, ymin, xmax and ymax values in the pixel
     # the values are the pixel or screen representation of the viewport window

     portal.append(float(viewport[0]) * float(canvas.cget("width")))  # xmin
     portal.append(float(viewport[1]) * float(canvas.cget("height"))) # ymin
     portal.append(float(viewport[2]) * float(canvas.cget("width")))  # xmax
     portal.append(float(viewport[3]) * float(canvas.cget("height"))) # ymax

     # For each face from the ModelData instance, get the three vertex numbers for that face then Get from the
     # ModelData instance the transformed vertex coordinates.

     for v1Num, v2Num, v3Num in faces :
        # vertice 1 contains (x1, y1) for the first face value
        v1 = DataSet.getTransformedVertex (v1Num,doPerspective)

        # vertice 2 contains (x2, y2) for the second face value
        v2 = DataSet.getTransformedVertex (v2Num,doPerspective)

        # vertice 3 contains (x3, y3) for the third face value
        v3 = DataSet.getTransformedVertex (v3Num,doPerspective)

        # x and y values of each vertex
        x1 = v1[0];  y1 = v1[1]; x2 = v2[0];  y2 = v2[1]; x3 = v3[0];  y3 = v3[1];

        #create a copy of v1, v2 and v3 so that we don't modify their orignal values
        x1_temp = x1; y1_temp = y1; x2_temp = x2; y2_temp = y2; x3_temp = x3; y3_temp = y3

        # calls the clipLine definition in the Cohensutherland.py
        # checks if the do Draw value is true or false and returns the clipped co-ordinate for given two points
        # if the doDraw value is true then draw the line based on the new points(X1_new, Y1_new, X2_new, Y2_new) returned
        # by the clipping function and draw three lines, v1->v2, v2->v3, and v3->v1

        if doClip:
            # create a copy of v1, v2 and v3 so that we don't modify their orignal values
            #x1_temp = x1; y1_temp = y1; x2_temp = x2; y2_temp = y2; x3_temp = x3; y3_temp = y3
            doDraw, X1_new, Y1_new, X2_new, Y2_new = clipLine(x1_temp, y1_temp, x2_temp, y2_temp, portal)

            if doDraw:
                self.objects.append(canvas.create_line((X1_new, Y1_new), (X2_new, Y2_new)))
                doDraw, X1_new, Y1_new, X2_new, Y2_new = clipLine(x2_temp, y2_temp, x3_temp, y3_temp, portal)

            if doDraw:
                self.objects.append(canvas.create_line((X1_new, Y1_new), (X2_new, Y2_new)))
                doDraw, X1_new, Y1_new, X2_new, Y2_new = clipLine(x3_temp, y3_temp, x1_temp, y1_temp, portal)

            if doDraw:
                self.objects.append(canvas.create_line((X1_new, Y1_new), (X2_new, Y2_new)))
        else:
            #draw three lines, v1->v2, v2->v3, and v3->v1
            self.objects.append(canvas.create_line( (x1,y1),(x2,y2),(x3,y3),(x1,y1) ) )

  def redisplay( self, canvas, event ) :
    pass

#----------------------------------------------------------------------

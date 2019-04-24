# Kebede, Natnael M.
# nmk9004
# 2018-10-26

#----------------------------------------------------------------------
# This code was originally created by Prof. Farhad Kamangar.
# It has been significantly modified and updated by Brian A. Dalio for
# use in CSE 4303 / CSE 5365 in the 2018 Fall semester.

#----------------------------------------------------------------------
from CohenSutherland import clipLine
from BézierPatch import resolve
#_______________________________________________________________________________________________________________________
class cl_world :
  def __init__( self, objects = [], canvases = [] ) :
    self.objects = objects
    self.canvases = canvases
#-----------------------------------------------------------------------------------------------------------------------
  def add_canvas( self, canvas ) :
    self.canvases.append( canvas )
    canvas.world = self
#-----------------------------------------------------------------------------------------------------------------------
  def reset( self ) :
    self.objects = []
    for canvas in self.canvases :
      canvas.delete( 'all' )
#-----------------------------------------------------------------------------------------------------------------------
  def create_graphic_objects(self, canvas, resolution, DataSet, doClip = False, doPerspective = False, doEuler = False):

     viewport = DataSet.getViewport(); vertices = DataSet.getVertices()
     faces = DataSet.getFaces(); patches = DataSet.getPatches()
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
        v1 = DataSet.getTransformedVertex (v1Num,doPerspective,doEuler)

        # vertice 2 contains (x2, y2) for the second face value
        v2 = DataSet.getTransformedVertex (v2Num,doPerspective,doEuler)

        # vertice 3 contains (x3, y3) for the third face value
        v3 = DataSet.getTransformedVertex (v3Num,doPerspective,doEuler)

        #draws image
        self.drawTriangle(canvas, v1, v2, v3,portal, doClip)

        # iterate over the patches to get (x, y, z)
     for i in range(len(patches)):
        generated_patch_points = resolve(resolution, patches[i], vertices)
        self.getTrianglePoints(resolution, generated_patch_points, DataSet, portal, canvas, doEuler, doPerspective)
#-----------------------------------------------------------------------------------------------------------------------
  def getTrianglePoints(self, resolution, pointList, DataSet, portal,canvas,doEuler, doPerspective):
      #Given the generated patch points, the triangles of the patch can be created
      for row in range(0, resolution - 1):
          rowStart = row * resolution

          for col in range(0, resolution - 1):
            here = rowStart + col
            there = here + resolution

            triangleA = (pointList[here], pointList[there], pointList[there + 1])
            triangleB = (pointList[there + 1], pointList[here + 1], pointList[here])

            # Clipping and drawing for triangle A
            self.draw_Patch_Triangle(canvas, portal, DataSet, triangleA, doEuler, doPerspective)

            #Clipping and drawing for triangle B
            self.draw_Patch_Triangle(canvas, portal, DataSet, triangleB, doEuler, doPerspective)
#-----------------------------------------------------------------------------------------------------------------------
  def drawTriangle(self, canvas, v1, v2, v3, portal, doClip):
      # x and y values of each vertex
      x1 = v1[0]; y1 = v1[1];x2 = v2[0];y2 = v2[1];x3 = v3[0];y3 = v3[1]
      # create a copy of v1, v2 and v3 so that we don't modify their orignal values
      x1_temp = x1; y1_temp = y1; x2_temp = x2; y2_temp = y2; x3_temp = x3; y3_temp = y3

      # calls the clipLine definition in the Cohensutherland.py
      # checks if the do Draw value is true or false and returns the clipped co-ordinate for given two points
      # if the doDraw value is true then draw the line based on the new points(X1_new, Y1_new, X2_new, Y2_new) returned
      # by the clipping function and draw three lines, v1->v2, v2->v3, and v3->v1

      if doClip:
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
          # draw three lines, v1->v2, v2->v3, and v3->v1
          self.objects.append(canvas.create_line((x1, y1), (x2, y2), (x3, y3), (x1, y1)))
#-----------------------------------------------------------------------------------------------------------------------
  def draw_Patch_Triangle(self, canvas, portal, DataSet, Triangle_name,doEuler,doPerspective):
      (p1x, p1y) = DataSet.transformXYZ(Triangle_name[0][0], Triangle_name[0][1], Triangle_name[0][2],
                                        doEuler, doPerspective)
      (p2x, p2y) = DataSet.transformXYZ(Triangle_name[1][0], Triangle_name[1][1], Triangle_name[1][2],
                                        doEuler, doPerspective)
      (p3x, p3y) = DataSet.transformXYZ(Triangle_name[2][0], Triangle_name[2][1], Triangle_name[2][2],
                                        doEuler, doPerspective)

      doDraw, X1_new, Y1_new, X2_new, Y2_new = clipLine(p1x, p1y, p2x, p2y, portal)
      if doDraw:
          self.objects.append(canvas.create_line((X1_new, Y1_new), (X2_new, Y2_new)))

      doDraw, X1_new, Y1_new, X2_new, Y2_new = clipLine(p2x, p2y, p3x, p3y, portal)

      if doDraw:
          self.objects.append(canvas.create_line((X1_new, Y1_new), (X2_new, Y2_new)))

      doDraw, X1_new, Y1_new, X2_new, Y2_new = clipLine(p3x, p3y, p1x, p1y, portal)

      if doDraw:
          self.objects.append(canvas.create_line((X1_new, Y1_new), (X2_new, Y2_new)))
#-----------------------------------------------------------------------------------------------------------------------
  def redisplay( self, canvas, event ) :
    pass
#-----------------------------------------------------------------------------------------------------------------------


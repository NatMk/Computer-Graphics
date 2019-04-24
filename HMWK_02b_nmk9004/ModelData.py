# Kebede, Natnael M.
# nmk9004
# 2018-10-09

import sys

class ModelData() :
  def __init__( self, inputFile = None ) :
    self.m_Vertices = []
    self.m_Faces    = []
    self.m_Window   = []
    self.m_Viewport = []
    self.bounding_box = []
    self.Transformation_Matrix = []
    self.New_Transformation = []

    if inputFile is not None :
    # File name was given.  Read the data from the file.
      self.loadFile( inputFile )

  def loadFile( self, inputFile ) :
     # Count variable to keep track of s and w occurrences since they can only occur once.
     s_count = 0; w_count = 0

     # Read each line of the file.
     with open(inputFile, 'r') as fp:
         lines = fp.read().replace('\r', '').split('\n')

     for (index, line) in enumerate(lines, start=1):
         line = line.strip()
         _char = line[:1]

         for x in _char:
             strVar = line.split()  # tokenize each line of file w.r.t space
             # Ignore any line that starts with a #.
             if _char == "#":
                 continue

             # Ignore any blank line (or line that's only whitespace characters).
             elif line == " ":
                 continue

             elif _char is "v":
                 if len(strVar) == 4:  # save up to 3 floats only
                     try:  # conversion of strings into floats
                         self.m_Vertices.append((float(strVar[1]), float(strVar[2]), float(strVar[3])))
                     except:
                         print("Line %d is a malformed vertex spec." % index)  # Incase of conversion errors.
                 else:
                     print("Line %d is a malformed vertex spec." % index)
                     continue

             elif _char is "f":
                 if len(strVar) == 4:  # save up to 3 ints only
                     try:  # conversion of strings into ints
                         self.m_Faces.append((int(strVar[1]) - 1, int(strVar[2]) - 1, int(strVar[3]) - 1))
                     except:
                         print("Line %d is a malformed face spec." % index)  # Incase of conversion errors.
                 else:
                     print("Line %d is a malformed face spec." % index)
                     continue

             elif _char is "w":
                 w_count = w_count + 1
                 if len(strVar) == 5:  # save up to 4 floats only
                     try:  # conversion of strings into floats
                         # temporary storage location to store the first possible tuple
                         current_Window = (float(strVar[1]), float(strVar[2]), float(strVar[3]), float(strVar[4]))
                         self.m_Window = current_Window  # set previous value with the most recent duplicate
                         w_flag = 1  # indicates valid data for v
                     except:  # Incase of conversion errors.
                         print("Line %d is a malformed window spec." % index)
                         w_flag = -1  # incorrect value for window detected
                         w_count = w_count - 1  # Don't add this as a valid w value
                 else:
                     print("Line %d is a malformed window spec." % index)
                     w_flag = -1  # incorrect value for window detected

                 # It is an error if the model file has more than one w line.
                 # Print an error message for this occurence, but keep going.
                 if w_count > 1 and w_flag == 1:
                     print("Line %d is a duplicate window spec." % index)
                     continue

             elif _char is "s":
                 s_count = s_count + 1
                 if len(strVar) == 5:  # save up to 4 floats only
                     try:  # conversion of strings into floats
                         # temporary storage location to store the first possible tuple
                         current_Viewport = (float(strVar[1]), float(strVar[2]), float(strVar[3]), float(strVar[4]))
                         self.m_Viewport = current_Viewport  # set previous value with the most recent duplicate
                         s_flag = 1  # indicates valid data for v
                     except:  # Incase of conversion errors.
                         print("Line %d is a malformed viewport spec." % index)
                         s_flag = -1  # incorrect value for viewport detected
                         s_count = s_count - 1  # Don't add this as a valid s value
                 else:
                     print("Line %d is a malformed viewport spec." % index)
                     s_flag = -1

                 # It is an error if the model file has more than one s line.
                 # Print an error message for this occurence, but keep going.
                 if s_count > 1 and s_flag == 1:
                     print("Line %d is a duplicate viewport spec." % index)
                     continue

             # It is an error if a line starts with any other character.
             # Print an error message for that line, but keep going and look
             # at the rest of the lines.
             else:
                 print("Line %d starts with invalid character." % index)
                 continue

     #save each occurances of x,y and z vertex values
     x_Vertices = [x[0] for x in self.m_Vertices]
     y_Vertices = [y[1] for y in self.m_Vertices]
     z_Vertices = [z[2] for z in self.m_Vertices]

     #calclate the max and min of each vertices
     xmin = min(x_Vertices); xmax = max(x_Vertices); ymin = min(y_Vertices)
     ymax = max(y_Vertices); zmin = min(z_Vertices); zmax = max(z_Vertices)

     #save the components of the bounding box
     self.bounding_box = (xmin, xmax, ymin, ymax, zmin, zmax)

     # routine for the bounding box to return a tuple with six elements
  def getBoundingBox( self ): return self.bounding_box

  def specifyTransform( self, ax, ay, sx, sy ) :
    #Transformation Matrix to use for each of the vertices
    self.Transformation_Matrix = [ [sx, 0, ax ],[0, sy, ay],[0, 0, 1] ]

    #The transformation of each vertex v in the file
    for i in range(len(self.m_Vertices)):
        x_new = self.Transformation_Matrix[0][0] * self.m_Vertices[i][0] + self.Transformation_Matrix[0][1] * self.m_Vertices[i][1] + self.Transformation_Matrix[0][2] * 1
        y_new = self.Transformation_Matrix[1][0] * self.m_Vertices[i][0] + self.Transformation_Matrix[1][1] * self.m_Vertices[i][1] + self.Transformation_Matrix[1][2] * 1
        z_new = self.Transformation_Matrix[2][0] * self.m_Vertices[i][0] + self.Transformation_Matrix[2][1] * self.m_Vertices[i][1] + self.Transformation_Matrix[2][2] * 1 * 0.0
        self.New_Transformation.append((x_new, y_new, z_new))

  def getTransformedVertex( self, vNum ) :
      #Return a transformed version of vertex n. the return is a tuple with three elements (x', y', z')
      return self.New_Transformation[vNum]

  def getFaces( self )    : return self.m_Faces
  def getVertices( self ) : return self.m_Vertices
  def getViewport( self ) : return self.m_Viewport
  def getWindow( self )   : return self.m_Window

#---------#---------#---------#---------#---------#--------#
def constructTransform( w, v, width, height ) :
    #How much world should be shown in the display
    wxmin = w[0]; wymin = w[1]; wxmax = w[2]; wymax = w[3]
    #How much of the canvas the display of the object should take up
    vxmin = v[0]; vymin = v[1]; vxmax = v[2]; vymax = v[3]
    #Parameters for translation to the world coordinate origin
    fx = -1 * wxmin; fy = -1 * wymin
    #Parameters for the translation to the viewport-coordniate-origin parameters
    gx = width * vxmin; gy = height *vymin
    #Scaling factors to transform the scale of the world vertices to viewport
    sx = width * (vxmax-vxmin)/(wxmax-wxmin)
    sy = height * (vymax-vymin)/(wymax-wymin)
    #compute the constants
    ax = fx*sx + gx
    ay = fy*sy + gy
    # return a tuple with four elements
    return ax, ay, sx, sy
#---------#---------#---------#---------#---------#--------#
def _main() :
  # Get the file name to load and the canvas size.
  fName  = sys.argv[1]
  width  = int( sys.argv[2] )
  height = int( sys.argv[3] )

  # Create a ModelData object to hold the model data from
  # the supplied file name.
  model = ModelData( fName )

  # Now that it's loaded, print out a few statistics about
  # the model data that we just loaded.
  print( "%s: %d vert%s, %d face%s" % (
    fName,
    len( model.getVertices() ), 'ex' if len( model.getVertices() ) == 1 else 'ices',
    len( model.getFaces() ), '' if len( model.getFaces() ) == 1 else 's' ))

  print( 'First 3 vertices:' )
  for v in model.getVertices()[0:3] :
    print( '     ', v )

  print( 'First 3 faces:' )
  for f in model.getFaces()[0:3] :
    print( '     ', f )

  w = model.getWindow()
  v = model.getViewport()
  print( 'Window line:', w )
  print( 'Viewport line:', v )

  print('Canvas size:', width, height)
  print( 'Bounding box:', model.getBoundingBox() )

  ( ax, ay, sx, sy ) = constructTransform( w, v, width, height )
  print( f'Transform is {ax} {ay} {sx} {sy}' )

  model.specifyTransform( ax, ay, sx, sy )

  print( 'First 3 transformed vertices:' )
  for vNum in range( 3 ) :
    print( '     ', model.getTransformedVertex( vNum ) )

#---------#
if __name__ == '__main__' :
  _main()

#---------#---------#---------#---------#---------#--------#

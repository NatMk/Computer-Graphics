# Kebede, Natnael M.
# nmk9004
# 2018-10-09

import sys
import numpy as np
#_______________________________________________________________________________________________________________________
class ModelData() :
  def __init__( self, inputFile = None ) :
    self.m_Vertices = []
    self.m_Faces    = []
    self.m_Window   = []
    self.m_Viewport = []
    self.bounding_box = []
    self.object_center = []
    self.Transformation_Matrix = []
    self.Transformed_Vertices =  []
    self.Screen_Transformation = []
    self.Euler_Transformation = []
    self.EulerForPerspective = []
    self.PerspWithEuler = []
    self.m_Patches = []
    self.Euler_with_Perspective = []
    self.ax = 0.0; self.ay = 0.0
    self.sx = 0.0; self.sy = 0.0
    self.distance = 0.0
    self.roll_angle = 0.0
    self.pitch_angle = 0.0
    self.yaw_angle = 0.0

    if inputFile is not None :
    # File name was given.  Read the data from the file.
      self.loadFile( inputFile )
#-----------------------------------------------------------------------------------------------------------------------
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

             elif _char is "p":
                 if len(strVar) == 17:  # save up to 16 ints only
                     try:  # conversion of strings into ints
                         self.m_Patches.append((int(strVar[1]) - 1, int(strVar[2])  - 1,  int(strVar[3]) - 1,
                                                int(strVar[4]) - 1, int(strVar[5])  - 1,  int(strVar[6]) - 1,
                                                int(strVar[7]) - 1, int(strVar[8])  - 1,  int(strVar[9]) - 1,
                                                int(strVar[10])- 1, int(strVar[11]) - 1,  int(strVar[12]) - 1,
                                                int(strVar[13])- 1, int(strVar[14]) - 1, int(strVar[15]) - 1,
                                                int(strVar[16])-1))
                     except:
                         print("Line %d is a malformed patches spec." % index)  # Incase of conversion errors.
                 else:
                     print("Line %d is a malformed patches spec." % index)
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
     xmin = min(map(float, x_Vertices)); xmax = max(map(float, x_Vertices)); ymin = min(map(float, y_Vertices))
     ymax = max(map(float, y_Vertices)); zmin = min(map(float, z_Vertices)); zmax = max(map(float, z_Vertices))

     #save the components of the bounding box
     self.bounding_box = (xmin, xmax, ymin, ymax, zmin, zmax)

     #save the components of the center of the object
     x_center = (xmin + xmax)/ 2; y_center = (ymin + ymax)/ 2; z_center = (zmin + zmax)/ 2
     self.object_center = (x_center, y_center, z_center)
#-----------------------------------------------------------------------------------------------------------------------
     # routine for the bounding box to return a tuple with six elements
  def getBoundingBox( self ): return self.bounding_box
#-----------------------------------------------------------------------------------------------------------------------
    # routine to return the center of the object from the bounding box to return a tuple with six elements
  def getCenter(self): return self.object_center
#-----------------------------------------------------------------------------------------------------------------------
  def specifyEulerAngles(self, roll_angle, pitch_angle, yaw_angle, ax, ay, sx, sy, ):

      self.roll_angle = roll_angle; self.pitch_angle = pitch_angle; self.yaw_angle = yaw_angle
      # The Euler angles, in radians.
      phi,theta, psi = (np.deg2rad(roll_angle), np.deg2rad(pitch_angle), np.deg2rad(yaw_angle))

      # The object center.
      tx, ty, tz = ( self.object_center[0],  self.object_center[1],  self.object_center[2])

      # Step One -- Compute the r00 through r22 values. First, get the cosine and sine values for the Euler angles.
      cosPhi, sinPhi = np.cos(phi), np.sin(phi)
      cosTheta, sinTheta = np.cos(theta), np.sin(theta)
      cosPsi, sinPsi = np.cos(psi), np.sin(psi)

      # Compute the nine r values. These four factors get used twice, so reuse them to save four multiplications.
      cPhiXcPsi = cosPhi * cosPsi
      cPhiXsPsi = cosPhi * sinPsi
      sPhiXcPsi = sinPhi * cosPsi
      sPhiXsPsi = sinPhi * sinPsi

      # The r00 through r22 values.
      r00 = cosPsi * cosTheta
      r01 = -cosTheta * sinPsi
      r02 = sinTheta
      r10 = cPhiXsPsi + sPhiXcPsi * sinTheta
      r11 = cPhiXcPsi - sPhiXsPsi * sinTheta
      r12 = -cosTheta * sinPhi
      r20 = -cPhiXcPsi * sinTheta + sPhiXsPsi
      r21 = cPhiXsPsi * sinTheta + sPhiXcPsi
      r22 = cosPhi * cosTheta

      # Step Two -- Compute the ex, ey, and ez values.
      ex = -r00 * tx - r01 * ty - r02 * tz + tx
      ey = -r10 * tx - r11 * ty - r12 * tz + ty
      ez = -r20 * tx - r21 * ty - r22 * tz + tz

      # Step Three -- Transform the points.
      for i in range(len(self.m_Vertices)) :
         xp = r00* self.m_Vertices[i][0] + r01 * self.m_Vertices[i][1] + r02 * self.m_Vertices[i][2] + ex
         yp = r10 * self.m_Vertices[i][0] + r11 * self.m_Vertices[i][1] + r12 * self.m_Vertices[i][2] + ey
         zp = r20 * self.m_Vertices[i][0] + r21 * self.m_Vertices[i][1] + r22 * self.m_Vertices[i][2] + ez

         xp_trans = ax + sx * float(xp)
         yp_trans = ay + sy * float(yp)

         self.EulerForPerspective.append((xp,yp,zp))

         self.Euler_Transformation.append((xp_trans,yp_trans))
#-----------------------------------------------------------------------------------------------------------------------
  def specifyTransform( self, ax, ay, sx, sy, distance ) :
    #Initialize ModelData Class values
    self.ax = ax; self.ay = ay
    self.sx = sx; self.sy = sy
    self.distance = distance

    #Transformation Matrix to use for each of the vertices
    self.Transformation_Matrix = [ [sx, 0, ax ],[0, sy, ay],[0, 0, 1] ]

    #The transformation of each vertex v in the file
    for i in range(len(self.m_Vertices)):
        x_new = self.Transformation_Matrix[0][0] * self.m_Vertices[i][0] + self.Transformation_Matrix[0][1] * \
                self.m_Vertices[i][1] + self.Transformation_Matrix[0][2] * 1
        y_new = self.Transformation_Matrix[1][0] * self.m_Vertices[i][0] + self.Transformation_Matrix[1][1] * \
                self.m_Vertices[i][1] + self.Transformation_Matrix[1][2] * 1
        z_new = self.Transformation_Matrix[2][0] * self.m_Vertices[i][0] + self.Transformation_Matrix[2][1] * \
                self.m_Vertices[i][1] + self.Transformation_Matrix[2][2] * 1 * 0.0
        self.Transformed_Vertices.append((x_new, y_new, z_new))

        updating_val = 1-((self.m_Vertices[i][2])/(distance))

        if updating_val == 0:
           updating_val = 1
           # perspective projection of the world space
           x_screen = sx * ((self.m_Vertices[i][0])) / (updating_val)  + ax
           y_screen = sy * ((self.m_Vertices[i][1])) / (updating_val) + ay
           self.Screen_Transformation.append((x_screen, y_screen))
        else:
           #perspective projection of the world space
           x_screen = sx *( (self.m_Vertices[i][0])/(1-((self.m_Vertices[i][2])/(distance))) ) + ax
           y_screen = sy *( (self.m_Vertices[i][1])/(1-((self.m_Vertices[i][2])/(distance)))) + ay
           self.Screen_Transformation.append((x_screen,y_screen))
#-----------------------------------------------------------------------------------------------------------------------
  def getTransformedVertex( self, vNum, doPerspective, doEuler) :
      if (doPerspective and doEuler):
          for i in range(len(self.EulerForPerspective)):
              updating_val = 1 - ((self.EulerForPerspective[i][2]) / (self.distance))

              if updating_val == 0:
                  updating_val = 1
                  x_screen = self.sx * ((self.EulerForPerspective[i][0])) / (updating_val) + self.ax
                  y_screen = self.sy * ((self.EulerForPerspective[i][1])) / (updating_val) + self.ay
              else:
                x_screen = self.sx * ((self.EulerForPerspective[i][0]) / (1 - ((self.EulerForPerspective[i][2]) /
                                                                             (self.distance)))) + self.ax
                y_screen = self.sy * ((self.EulerForPerspective[i][1])/  (1 -  ((self.EulerForPerspective[i][2])/
                                                                              (self.distance)))) + self.ay

              self.PerspWithEuler.append((x_screen,y_screen))
          return self.PerspWithEuler[vNum]
      if (doEuler):
          # Return a transformed screen version of vertex n. the return is a tuple with three elements (x', y', z')
          return self.Euler_Transformation[vNum]

      if (doPerspective):
        # Return a transformed screen version of vertex n. the return is a tuple with three elements (x', y', z')
          return self.Screen_Transformation[vNum]

      else:
        #Return a transformed world version of vertex n. the return is a tuple with three elements (x', y', z')
          return self.Transformed_Vertices[vNum]
#-----------------------------------------------------------------------------------------------------------------------
  def Euler_rotate_perspective(self, x, y, z):
      # The Euler angles, in radians.
      phi, theta, psi = (np.deg2rad(self.roll_angle), np.deg2rad(self.pitch_angle), np.deg2rad(self.yaw_angle))

      # The object center.
      tx, ty, tz = (self.object_center[0], self.object_center[1], self.object_center[2])

      # Step One -- Compute the r00 through r22 values. First, get the cosine and sine values for the Euler angles.
      cosPhi, sinPhi = np.cos(phi), np.sin(phi)
      cosTheta, sinTheta = np.cos(theta), np.sin(theta)
      cosPsi, sinPsi = np.cos(psi), np.sin(psi)

      # Compute the nine r values. These four factors get used twice, so reuse them to save four multiplications.
      cPhiXcPsi = cosPhi * cosPsi
      cPhiXsPsi = cosPhi * sinPsi
      sPhiXcPsi = sinPhi * cosPsi
      sPhiXsPsi = sinPhi * sinPsi

      # The r00 through r12 values.
      r00 = cosPsi * cosTheta
      r01 = -cosTheta * sinPsi
      r02 = sinTheta
      r10 = cPhiXsPsi + sPhiXcPsi * sinTheta
      r11 = cPhiXcPsi - sPhiXsPsi * sinTheta
      r12 = -cosTheta * sinPhi
      r20 = -cPhiXcPsi * sinTheta + sPhiXsPsi
      r21 = cPhiXsPsi * sinTheta + sPhiXcPsi
      r22 = cosPhi * cosTheta

      # Step Two -- Compute the ex, ey, and ez values.
      ex = -r00 * tx - r01 * ty - r02 * tz + tx
      ey = -r10 * tx - r11 * ty - r12 * tz + ty
      ez = -r20 * tx - r21 * ty - r22 * tz + tz

      xp = r00 * x + r01 * y + r02 * z + ex
      yp = r10 * x + r11 * y + r12 * z + ey
      self.zp = r20 * x + r21 * y + r22 * z + ez

      return (xp,yp)
#-----------------------------------------------------------------------------------------------------------------------
  def Euler_rotate_patchs(self, x, y, z):
      # The Euler angles, in radians.
      phi, theta, psi = (np.deg2rad(self.roll_angle), np.deg2rad(self.pitch_angle), np.deg2rad(self.yaw_angle))

      # The object center.
      tx, ty, tz = (self.object_center[0], self.object_center[1], self.object_center[2])

      # Step One -- Compute the r00 through r22 values. First, get the cosine and sine values for the Euler angles.
      cosPhi, sinPhi = np.cos(phi), np.sin(phi)
      cosTheta, sinTheta = np.cos(theta), np.sin(theta)
      cosPsi, sinPsi = np.cos(psi), np.sin(psi)

      # Compute the nine r values. These four factors get used twice, so reuse them to save four multiplications.
      cPhiXcPsi = cosPhi * cosPsi
      cPhiXsPsi = cosPhi * sinPsi
      sPhiXcPsi = sinPhi * cosPsi
      sPhiXsPsi = sinPhi * sinPsi

      # The r00 through r12 values.
      r00 = cosPsi * cosTheta
      r01 = -cosTheta * sinPsi
      r02 = sinTheta
      r10 = cPhiXsPsi + sPhiXcPsi * sinTheta
      r11 = cPhiXcPsi - sPhiXsPsi * sinTheta
      r12 = -cosTheta * sinPhi
      r20 = -cPhiXcPsi * sinTheta + sPhiXsPsi
      r21 = cPhiXsPsi * sinTheta + sPhiXcPsi
      r22 = cosPhi * cosTheta

      # Step Two -- Compute the ex, ey, and ez values.
      ex = -r00 * tx - r01 * ty - r02 * tz + tx
      ey = -r10 * tx - r11 * ty - r12 * tz + ty
      ez = -r20 * tx - r21 * ty - r22 * tz + tz

      xp = r00 * x + r01 * y + r02 * z + ex
      yp = r10 * x + r11 * y + r12 * z + ey
      self.zp = r20 * x + r21 * y + r22 * z + ez

      xp_trans = self.ax + self.sx * float(xp)
      yp_trans = self.ay + self.sy * float(yp)

      return (xp_trans,yp_trans)
#-----------------------------------------------------------------------------------------------------------------------
  def Euler_Perspective(self, x,y,z):
      # perspective projection of the world space for the resolved patch values
      x_screen = self.sx * ((x) / (1 - ((z) / (self.distance)))) + self.ax
      y_screen = self.sy * ((y) / (1 - ((z) / (self.distance)))) + self.ay
      return (x_screen, y_screen)
#-----------------------------------------------------------------------------------------------------------------------
  def transformXYZ(self, x, y, z, doEuler, doPerspective):
      #for the verices of the resolved patch we can rotate, do perspective and/or draw in parallel
      xp_trans = self.ax + self.sx * float(x)
      yp_trans = self.ay + self. sy * float(y)

      if (doPerspective and doEuler):
        (x_rotated, y_rotated) = self.Euler_rotate_perspective(x, y, z)
        (x_Euler_perspective, y_Euler_perspective) = self.Euler_Perspective(x_rotated, y_rotated, self.zp)
        return (x_Euler_perspective, y_Euler_perspective)

      if(doEuler):
          (x_rotated,y_rotated) = self.Euler_rotate_patchs(x, y, z)
          return (x_rotated,y_rotated)

      if (doPerspective):
          (x_perspective, y_perspective) = self.Euler_Perspective(x, y, z)
          return (x_perspective, y_perspective)

      else:
          return (xp_trans,yp_trans)
#-----------------------------------------------------------------------------------------------------------------------
  def getFaces( self )    : return self.m_Faces
  def getVertices( self ) : return self.m_Vertices
  def getViewport( self ) : return self.m_Viewport
  def getWindow( self )   : return self.m_Window
  def getPatches(self)    : return self.m_Patches
#-----------------------------------------------------------------------------------------------------------------------
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
#-----------------------------------------------------------------------------------------------------------------------
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
#-----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__' :
  _main()
#_______________________________________________________________________________________________________________________

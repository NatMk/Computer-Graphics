# Natnael Kebede
# nmk9004
# 2018-09-09

import sys

class ModelData() :
  def __init__( self, inputFile = None ) :
    self.m_Vertices = []
    self.m_Faces    = []
    self.m_Window   = []
    self.m_Viewport = []

    if inputFile is not None :
      # File name was given.  Read the data from the file.
      self.loadFile( inputFile )

  def loadFile( self, inputFile ) :

    #Count variable to keep track of s and w occurrences since they can only occur once.
    s_count = 0
    w_count = 0

    # Read each line of the file.
    with open(inputFile, 'r') as fp:
      lines = fp.read().replace('\r', '').split('\n')

    for (index, line) in enumerate(lines, start=1):
      line = line.strip()
      _char = line[:1]

      for x in _char:
        strVar = line.split() #tokenize each line of file w.r.t space
        # Ignore any line that starts with a #.
        if _char =="#":
          continue

        # Ignore any blank line (or line that's only whitespace characters).
        elif line ==" ":
          continue

        # For the remaining lines, if the line starts with:
        #  f -- Append the three integers as a tuple to self.m_Faces.
        #  v -- Append the three floats as a tuple to self.m_Vertices.
        #  w -- Keep the four floats as a tuple in self.m_Window.
        #  s -- Keep the four floats as a tuple in self.m_Viewport.

        # Note that the above comments mention integers and floats.
        # The string representation of the integers
        # and floats have been converted into actual numbers.  There may be formatting
        # errors in the file. This is ensured and catched (and reported)

        # A model file may have any number of f and v lines.  In fact,
        # some model files we will use will have thousands of v and f
        # lines.

        elif _char is "v":
          if len(strVar) == 4: #save up to 3 floats only
            try: #conversion of strings into floats
              self.m_Vertices.append((float(strVar[1]), float(strVar[2]),float(strVar[3])))
            except:
              print("Line %d is a malformed vertex spec."% index) #Incase of conversion errors.
          else:
            print("Line %d is a malformed vertex spec." % index)
            continue

        elif _char is "f":
          if len(strVar) == 4:  # save up to 3 ints only
            try: #conversion of strings into ints
              self.m_Faces.append((int(strVar[1])-1, int(strVar[2])-1, int(strVar[3])-1))
            except:
              print("Line %d is a malformed face spec." % index) #Incase of conversion errors.
          else:
            print("Line %d is a malformed face spec." % index)
            continue

        elif _char is "w":
          w_count = w_count + 1
          if len(strVar) == 5:  # save up to 4 floats only
            try: #conversion of strings into floats
              # temporary storage location to store the first possible tuple
              current_Window = (float(strVar[1]), float(strVar[2]), float(strVar[3]), float(strVar[4]))
              self.m_Window = current_Window #set previous value with the most recent duplicate
              w_flag = 1 #indicates valid data for v
            except: #Incase of conversion errors.
              print("Line %d is a malformed window spec."% index)
              w_flag = -1 #incorrect value for window detected
              w_count = w_count - 1 #Don't add this as a valid w value
          else:
            print("Line %d is a malformed window spec." % index)
            w_flag = -1 #incorrect value for window detected

          # It is an error if the model file has more than one w line.
          # Print an error message for this occurence, but keep going.
          if w_count > 1 and w_flag == 1:
              print("Line %d is a duplicate window spec." % index)
              continue

        elif _char is "s":
          s_count = s_count + 1
          if len(strVar) == 5:  # save up to 4 floats only
            try: #conversion of strings into floats
              # temporary storage location to store the first possible tuple
              current_Viewport = (float(strVar[1]), float(strVar[2]), float(strVar[3]), float(strVar[4]))
              self.m_Viewport = current_Viewport #set previous value with the most recent duplicate
              s_flag = 1  # indicates valid data for v
            except: #Incase of conversion errors.
              print("Line %d is a malformed viewport spec."% index)
              s_flag = -1 #incorrect value for viewport detected
              s_count = s_count - 1 #Don't add this as a valid s value
          else:
            print("Line %d is a malformed viewport spec." % index)
            s_flag = -1
              
          # It is an error if the model file has more than one s line.
          # Print an error message for this occurence, but keep going.
          if s_count > 1 and s_flag == 1:
            print("Line %d is a duplicate viewport spec."% index)
            continue

        # It is an error if a line starts with any other character.
        # Print an error message for that line, but keep going and look
        # at the rest of the lines.
        else:
           print("Line %d is a malformed character." % index)
           continue

  def getFaces( self )    : return self.m_Faces
  def getVertices( self ) : return self.m_Vertices
  def getViewport( self ) : return self.m_Viewport
  def getWindow( self )   : return self.m_Window

#---------#---------#---------#---------#---------#--------#
def _main() :

  # Get the file name to load.
    fName = sys.argv[1]

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

    print( 'Window line:', model.getWindow() )
    print( 'Viewport line:', model.getViewport() )

#---------#
if __name__ == '__main__' :
      _main()
#---------#---------#---------#---------#---------#--------#

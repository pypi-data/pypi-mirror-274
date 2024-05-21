import subprocess

MAX_MEMORY = None

class Jpeg:
    def __init__(self, path, options=None, debug=False, verbose=False):
        self.path = path
        self.options = options if options is not None else []
        self.isDebug = debug
        self.isVerbose = verbose

    def optimize(self):
        ''' Perform optimization of entropy encoding parameters. '''
        return Jpeg(self.path, options = self.options+['-optimize'], 
                    debug=self.isDebug, verbose=self.isVerbose)
    
    def progressive(self):
        ''' Create progressive JPEG file.'''
        return Jpeg(self.path, options = self.options+['-progressive'], 
                    debug=self.isDebug, verbose=self.isVerbose)
    
    def restart(self, N):
        ''' Emit a JPEG restart marker every N MCU rows, or every N MCU blocks if "B" is attached to the number. '''
        return Jpeg(self.path, options = self.options+['-restart', N], 
                    debug=self.isDebug, verbose=self.isVerbose)
    
    def arithmetic(self):
        ''' Use arithmetic coding. '''
        return Jpeg(self.path, options = self.options+['-arithmetic'], 
                    debug=self.isDebug, verbose=self.isVerbose)
    
    def scans(self, file):
        ''' Use the scan script given in the specified text file. '''
        return Jpeg(self.path, options = self.options+['-scans', file], 
                    debug=self.isDebug, verbose=self.isVerbose)
    
    def flip(self, direction):
        ''' Mirror image (horizontally, vertically). '''
        assert direction in ['horizontal', 'vertical']
        return Jpeg(self.path, options = self.options+['-flip', direction], 
                    debug=self.isDebug, verbose=self.isVerbose)
    
    def rotate(self, angle):
        ''' Rotate image (90, 180, 270 degrees). '''
        assert angle in [90, 180, 270]
        return Jpeg(self.path, options = self.options+['-rotate', str(angle)], 
                    debug=self.isDebug, verbose=self.isVerbose)
    
    def transpose(self):
        ''' Transpose image (across UL-to-LR axis). '''
        return Jpeg(self.path, options = self.options+['-transpose'], 
                    debug=self.isDebug, verbose=self.isVerbose)
    
    def transverse(self):
        ''' Transverse transpose image (across UR-to-LL axis). '''
        return Jpeg(self.path, options = self.options+['-transverse'], 
                    debug=self.isDebug, verbose=self.isVerbose)
    
    def trim(self):
        ''' Drop non-transformable edge blocks. '''
        return Jpeg(self.path, options = self.options+['-trim'], 
                    debug=self.isDebug, verbose=self.isVerbose)
    
    def crop(self, width, height, x_offset, y_offset):
        ''' Crop the image to a rectangular region of width W and height H,
        starting at point X,Y. '''
        return Jpeg(self.path, options = self.options+[
            '-crop', width, height, x_offset, y_offset], 
                    debug=self.isDebug, verbose=self.isVerbose)
    
    def grayscale(self):
        ''' Force grayscale output. '''
        return Jpeg(self.path, options = self.options+['-grayscale'], 
                    debug=self.isDebug, verbose=self.isVerbose)
    
    def greyscale(self):
        ''' Force greyscale output. Calls grayscale(). '''
        return self.grayscale()
    
    def copy(self, marker):
        ''' Copy only the specified marker(s). '''
        assert marker in ['none', 'comments', 'all']
        return Jpeg(self.path, options = self.options+['-copy', marker], 
                    debug=self.isDebug, verbose=self.isVerbose)
    
    def verbose(self):
        ''' Activate verbose output. '''
        return Jpeg(self.path, options = self.options, 
                    debug=self.isDebug, verbose=True)
    
    def debug(self):
        ''' Activate debug output. Same as verbose(). '''
        return Jpeg(self.path, options = self.options, 
                    debug=True, verbose=self.isVerbose)

    def save(self, out_path):
        ''' Save the image to a file. '''
        out = subprocess.run(
                self.get_command() + ['-outfile', out_path] + [self.path],
                capture_output=True
            )

        return out

    def get_command(self):
        command = ['jpegtran', *self.options]

        if MAX_MEMORY is not None:
            command += ['-maxmemory', MAX_MEMORY]

        if self.isDebug:
            command += ['-debug']

        if self.isVerbose:
            command += ['-verbose']

        return command

    def __repr__(self) -> str:
        return f'Jpeg({self.path}, {self.options})'
            
def open(path):
    return Jpeg(path)


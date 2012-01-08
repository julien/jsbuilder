from glob import iglob
import shutil
import os
from sys import argv

class JSBuilder(object):
  
  COMPILER_JAR = 'compiler.jar'

  COMPILATION_LEVELS = [
      'WHITESPACE_ONLY',
      'SIMPLE_OPTIMIZATIONS',
      'ADVANCED_OPTIMIZATIONS'
  ]

  JAVA = 'java'
  
  LINE_DELIMITER = '~' * 45

  JAVA_NOT_FOUND = """ 
  %s
  java was not found in your "PATH"
  environment variable. please add it 
  and run the program again.
  %s 
  """ % (LINE_DELIMITER, LINE_DELIMITER)

  def __init__(self, src_path, output_file):
    
    self.__java_path = self.__check_java()
    if self.__java_path is None:
      print(JSBuilder.JAVA_NOT_FOUND)
      return

   
    self.src_path = src_path
    self.output_file = output_file
   
    self.src_dirs = []
    self.src_dirs.append(src_path)
    self.__scan(src_path)
    
    self.src_files = self.__get_source_files()
    self.run()

  """ checks if a program is executable or not """
  def __is_executable(self, program):
    return os.path.exists(program) and os.access(program, os.X_OK)
  
  """ checks if java is available in the PATH environment variable """
  def __check_java(self):
    java = JSBuilder.JAVA
    if os.pathsep == ';':
      java += '.exe'
    
    for path in os.environ['PATH'].split(os.pathsep):
      exe = os.path.join(path, java)
      if self.__is_executable(exe):
        return exe
        break


  def __scan(self, path):
    dir_contents = os.listdir(path)

    for f in dir_contents:
      realpath = os.path.join(self.src_path, f)
      if(os.path.isdir(realpath)):
        self.src_dirs.append(realpath)
      
    return self.src_dirs

  """ concatenates all JS source files [deprecated] """
  #def concatenate(self):
  #  for d in self.src_dirs:
  #    for f in iglob(os.path.join(d, '*.js')):
  #      shutil.copyfileobj(open(f, 'rb'), self.output_file)
  #  self.output_file.close()
  #
  #  return os.path.realpath(self.output_file.name)

  """ Returns the JS source files found under the src_path directory """
  def __get_source_files(self):
    files = []
    for d in self.src_dirs:
      for f in iglob(os.path.join(d, '*.js')):
        files.append(f)

    files.reverse()
    return files
  
  def __get_compiler_options(self):
    s = '--compilation_level ADVANCED_OPTIMIZATIONS ' 
    for f in self.src_files:
      s += '--js %s ' % f

    s += '--js_output_file %s ' % self.output_file
    return s

  def run(self):
    s = '%s -jar compiler.jar %s' % (self.__java_path, self.__get_compiler_options())
    print s
    print(JSBuilder.LINE_DELIMITER)
    os.system(s)
    print(JSBuilder.LINE_DELIMITER)
      
""" prints help """
def print_help():
  print('simple JS build script')
  print('~> usage: ')
  print('[python] build[.py] src_dir output_file')

def main():
  if len(argv) < 3:
    print_help()
  else:
    (script, src_dir, output_file) = argv
    builder = JSBuilder(src_dir, output_file)

if __name__ == '__main__':
  main()





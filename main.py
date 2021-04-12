
import sys
import os
import string
import random
import shutil
import glob

from PyPDF2 import PdfFileReader, PdfFileWriter

def pdf_splitter(path,folder,start = None,end = None):
    fname = os.path.splitext(os.path.basename(path))[0]

    pdf = PdfFileReader(path)
    for page in range(pdf.getNumPages()):
        if start and (page+1 < start):
         continue

        if end and (page+1 > end):
         break

        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))

        output_filename = '{}/{}.pdf'.format(folder,page+1)
        with open(output_filename, 'wb') as out:
            
             pdf_writer.write(out)

def merger(output_path, input_paths):
    pdf_writer = PdfFileWriter()

    for path in input_paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))

    with open(output_path, 'wb') as fh:
        pdf_writer.write(fh)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def main(): 
    input = sys.argv[1]
    ranges = sys.argv[2].split(',')
    
    if ranges[0]:
     start = int(ranges[0])
    else:
     start = None
    if ranges[1]:
     end = int(ranges[1])
    else:
     end = None

    destination = sys.argv[3]
    tmp_folder = id_generator()
    os.mkdir(tmp_folder)

    try:
        if os.path.isfile(input):
         pdf_splitter(input,tmp_folder,start,end)
         paths = glob.glob(tmp_folder + '/*.pdf')
         if len(paths) > 9:
          paths.sort(key=lambda f: int(filter(str.isdigit, f)))

         if paths:
          tmp_file = tmp_folder + "/output.pdf"
          merger(tmp_file,paths)
          os.system('gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook \
-dNOPAUSE -dQUIET -dBATCH -sOutputFile=' + destination +' ' + tmp_file)
          print ("convert successful, look at " + destination)
         else:
          print ("File not exist")
    except Exception as e:
        print ("Something went wrong!")
    finally:
        shutil.rmtree(tmp_folder)
    

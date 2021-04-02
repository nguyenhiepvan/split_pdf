
import sys
import os
import string
import random
import shutil

from PyPDF2 import PdfFileReader, PdfFileWriter

def pdf_splitter(path,folder,start,end):
    fname = os.path.splitext(os.path.basename(path))[0]

    pdf = PdfFileReader(path)
    for page in range(pdf.getNumPages()):
        if (page+1 < start):
         continue

        if (page+1 > end):
         break

        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))

        output_filename = '{}/input_page_{}.pdf'.format(folder,page+1)
        with open(output_filename, 'wb') as out:
            
             pdf_writer.write(out)

        print('Created: {}'.format(output_filename))

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
    start = int(ranges[0])
    end = int(ranges[1])
    tmp_folder = id_generator()
    os.mkdir(tmp_folder)

    if os.path.isfile(input):
     if input.lower().endswith(('.pdf')):
        pdf_splitter(input,tmp_folder,start,end)
        paths = []
        
        for x in range(start,end):
         file = '{}/input_page_{}.pdf'.format(tmp_folder,x)
         if os.path.isfile(file):
          paths.append(file)

        if paths:
          merger('output/output.pdf',paths)
          shutil.rmtree(tmp_folder)

     else:
      print ("File not supported")
    else:
     print ("File not exist")

if __name__=="__main__": 
    main() 
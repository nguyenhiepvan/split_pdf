#Propose

Split pdf file to smaller pdf

#Installation

clone project and run

```shell
python setup.py develop
```
**notice**: maybe need permissions

#Usage

```shell
split_pdf <your-pdf-file> <start-page>,<end-page> <output-pdf>
```
e.g: `split_pdf test.pdf 1,10 output/output.pdf`

#Requirements
- pypdf

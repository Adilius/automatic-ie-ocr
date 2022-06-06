# Automatic Data Enrichment of Optical Recognition Systems on Forms
With OCR technologies the contents of a form can be read, the position of each word and its contents can be extracted, however the relation between the words cannot be understood. This prototype works by feeding an image of an unfilled form and another image of a filled form which contains the data to be enriched to an OCR engine. The output of OCR engine is run through a post-processing step which together with a modified Euclidean and fuzzy string search algorithms is able to cluster field names and field values in the filled in form image.

## Quick start
1. Clone repository: `git clone https://github.com/Adilius/form-ocr-data-enrichment.git`

2. Change directory to repository: `cd form-ocr-data-enrichment/`

3. Install required packages: `pip install -r .\requirements.txt`

4. Run script: `python .\app.py`

## Input files location
In this prototype three different types of forms were tested. Each form type requires both a picture of an unfilled form and filled forms.

    .
    ├── input                   # Contains input images
    │   ├── form_blank          # Images of blank forms
    │       ├── bottom_form 
    │       ├── middle_form 
    │       └── top_form  
    │   └── form_filled         # Images of filled forms
    │       ├── bottom_form 
    │       ├── middle_form 
    │       └── top_form  
    └── ...
    
    
## Input files example

![image](https://user-images.githubusercontent.com/43440295/172223931-8f3d9987-5577-4462-b5dc-ed4add00eef2.png)

![image](https://user-images.githubusercontent.com/43440295/172223974-471a8cb2-80b3-44d5-b767-49e0dce9f9bf.png)


## Output files location
The output files for each form type contain a .csv file and image file for each input image.

    .
    ├── output                # Contains output
    │   ├── top_form          # Output for top form
    │       ├── 1.csv         # Raw output in text
    │       ├── 1.png         # Image containing resulting bounding boxes
    │       └── ...
    │   └── ...               
    └── ...

## Output
Image with bounding boxes draw on the image, original bounding boxes come from the text detection engine, the better the engine the better boxes. Each colour indicates a grouping and thicker border indicates indicates the field value (label):
![image](https://user-images.githubusercontent.com/43440295/172224122-ce641e4f-c316-426a-a651-4eff72e23639.png)

Text recognition run on the boxes (result is very bad, this all depends on the text recognition engine you use, I used a very bad one):
| name            | johyjohy dioe   |
|-----------------|-----------------|
| occupation      | dioecnixt ician |
| hometown        | cnixtustly      |
| favorite animal | ician0q         |

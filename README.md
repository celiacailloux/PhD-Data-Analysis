# PhD-Data-Analysis

PhD-Data-Analysis is a Python library containing objects and modules to read, analyse and visualize data extracted from instruments used for **electrochemistry** and **material characterization**. 

## Purpose

As an physics experimentalist who works with and is in charge of many instruments being able to **automate data analysis** is a time saver like no other and reduces human errors. Moreover, the software that is usually included along your instrument is often cumbersome (because it is capable of many-facetted analysis) and requires a sequence of methods to **prep** and **analyse your data** for your specific purpose. 

Hence, the idea was to use Python to automatically visualize data to help me **get an overview** and **find patterns** to help me progress my research. Especially when calibrating and getting-to-know your instruments, visualizing your results is very helpful.  

## Instrument Software and File Type

The subject of my PhD was *Electrochemical reduction of CO2 to fuels and chemicals* (aka converting gaseous CO2 into ethanol for your car to run on or ethylene to produce plastic in a carbonneutral way). My task was to develop a new catalyst to make the conversion effective, energitetically and selectively.

### Electrochemistry

**Instrument Type | File Type | Link to software/hardware**
- EC-Lab | csv | [About EC-Lab](https://snowhouse.ca/pdf/Biologic%20-%20Ec-Lab.pdf)
- EC-MS  |     | Work from former collegue [:octocat:ScottSoren/EC_MS](https://github.com/ScottSoren/EC_MS)


### Material Characterization

**Instrument Type | File Type | Link to software/hardware**
- GC  | raw   | NB! Requires PyExLabSys read the encoding (raw to csv) [Perkin Elmer Clarus 580](https://www.perkinelmer.com/lab-solutions/resources/docs/GDE_Clarus500-580UserGuide.pdf)
- ICP | excel | [iCAP-QC ICP-MS](https://www.thermofisher.com/order/catalog/product/IQLAAGGAAQFAQKMBIT?ce=E.21CMD.DL107.34553.01&cid=E.21CMD.DL107.34553.01&ef_id=Cj0KCQiAmL-ABhDFARIsAKywVafdhDB3pSLNYfZLbrDsCVPh5PA-6ulw3b8XplKiKTSB_LRYruyXYQ8aAgwhEALw_wcB:G:s&s_kwcid=AL!3652!3!356242366285!e!!g!!icap%20rq%20icp%20ms&gclid=Cj0KCQiAmL-ABhDFARIsAKywVafdhDB3pSLNYfZLbrDsCVPh5PA-6ulw3b8XplKiKTSB_LRYruyXYQ8aAgwhEALw_wcB#/IQLAAGGAAQFAQKMBIT?ce=E.21CMD.DL107.34553.01&cid=E.21CMD.DL107.34553.01&ef_id=Cj0KCQiAmL-ABhDFARIsAKywVafdhDB3pSLNYfZLbrDsCVPh5PA-6ulw3b8XplKiKTSB_LRYruyXYQ8aAgwhEALw_wcB:G:s&s_kwcid=AL!3652!3!356242366285!e!!g!!icap%20rq%20icp%20ms&gclid=Cj0KCQiAmL-ABhDFARIsAKywVafdhDB3pSLNYfZLbrDsCVPh5PA-6ulw3b8XplKiKTSB_LRYruyXYQ8aAgwhEALw_wcB) 
- XPS | excel | [Avantage Data System](https://www.thermofisher.com/order/catalog/product/IQLAADGACKFAKRMAVI#/IQLAADGACKFAKRMAVI)
- XRD | csv   | [HighScore Plus](https://www.malvernpanalytical.com/en/products/category/software/x-ray-diffraction-software/highscore-with-plus-option)

## Folder Structure

PhD-Data-Analysis is split into folders named after each type of instrument (e.g. XRD). Each instrument-folder then contains a main script (*main.py*) and subfolders for figures, modules and other. E.g.
- instrument_type_1
  - main.py
  - figures
  - example
  - *submodules*
  - misc
- instrument_type_2
  - main.py
  - figures
  - example
  - *submodules*
  - misc
- ...

## Usage

Please take a look at *readme.md* in each instrument-type-folder for an introduction to how best to use the library

- [ ] add relative links to the individual readme.md files

## Packages

- pandas
- matplotlib
- lmfit
- scipy
- os
- sys

## Contact and Contribution

Do not hesitate to contact me at *celiacailloux@gmail.com* if you would like an introduction or if maybe you find this inspirational and what to starte coding yourself?

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

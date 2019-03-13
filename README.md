# Webl  Crawler Project

# Project Idea
The project is about crawling websites and extracting image data. The inputs are a url and depth parameter. For each depth, starting with the given url, the crawler extracts all the images and adds them to the images file in `Data` folder, and tracks the hyperlinks which are traversed subsequently in the next step of crawling, depending on the depth param.

Care is taken that external links are not traversed and also the repetion of links and incorrect or invalid links are avoided. Invalid link could be a link to a pdf, which is resource, not a navigational link.
 
Refer reference image for a brief schematic idea.
## How to run

* python version should be 2.7+
* Create virtual environment if possible
* Run pip install -r requirements.txt
* switch to the project directory
* Run python main.py < url>  < depth >

# TO DO
Caching and Database storage is additional thing that can be done to improve performance. 


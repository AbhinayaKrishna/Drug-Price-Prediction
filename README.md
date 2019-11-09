# Drug-Price-Prediction
<h1>Project Map - Pharmaceutical Drug Predictions</h1>

<h3>BACKGROUND:</h3>  
Pharmaceutical drug spending in the U.S. is on a true upward trend.  Not only is the number of drugs being produced on the rise, but the number of Americans taking those drugs is also increasing.  An accurate projection of drug prices enhances transparency of our healthcare system and allows the public, government, and industry to make more informed decisions regarding their health and finances.

<h3>PURPOSE:</h3>
The purpose of the study is to build a machine learning model that can deliver this transparency through the prediction of drug prices.

<h3>ROOT DATA SOURCES:</h3>
Drug price data comes from the Medicaid.gov site, [here][1].  Patent data comes from the FDA’s Orange Book website, (here)[https://www.fda.gov/drugs/drug-approvals-and-databases/orange-book-data-files].

<h3>DATASETS:</h3>
The price dataset has 1M+ rows with 12 columns (though maybe only half of those will be useful).  The Orange Book dataset has roughly 55K rows with 27 columns (half of which could provide predictive power).  As mentioned, the data comes through two (or more) different sources.  While the datasets don’t line up perfectly, I’ve found that drug names in each of the two datasets can be matched reasonably well utilizing Levenshtein distance calculations (via the fuzzywuzzy library).  The Medicaid website does have an API for the dataset.  This will facilitate up-to-date projections of prices in the final product.

<h3>FEASIBILITY ANALYSIS (EDA):</h3>
The following plot, as an example, displays the price of 4 metformin-based drugs (which are widely utilized to manage diabetes).
Next, we see a plot for the price of ibuprofen over time.  Although the correlation is not quite as strong, there is still a clear path that can be followed (not to mention, an interesting upward trend at the end/beginning of 2018/2019.
These are just two examples of drugs whose prices.  Of necessity, the project will continue to evolve, and apply more features to create better predictions; price over time is insufficient.  The datasets mentioned above will add some features.  Those datasets listed below will provide supplementary questions and features as I develop the predictive model.
<h3>NEXT STEPS:</h3>
<ul>
<li> Merge the price and patent datasets.</li> 
  <ul>
  <li> Either by parallel processes or via AWS</li>
  </ul>
</ul>
<ul>
<li>Clean datasets as outlined below/needed</li>
  <ul>
  <li>Further EDA on those below</li>
  <li>Incorporate these datasets with the price and patent datasets</li>
  </ul>
</ul>
<ul>
<li>Set up any APIs in code that can be utilized</li>
<li>Statistical analysis of multicollinearity, heteroscedasticity, bias, etc. (?)</li>
<li>Implementation of Machine Learning model (train v. test datasets?)</li>
<li>Creation of Dashboard (Flask? Bokeh?)</li>
</ul>

<h3>END RESULT:</h3> 
A handful of the datasets have APIs that I can connect to, and the remainder I plan on scraping and importing the data into the model.  The predictions will be output to a dynamic (live) dashboard where the various types of medications can be selected, and their historical and predicted prices viewed.  I also hope to implement several other pieces of information that will either be displayed (i.e. patent expiry dates) or selectable (i.e. drug delivery route, methods).

[1]https://data.medicaid.gov/Drug-Pricing-and-Payment/NADAC-National-Average-Drug-Acquisition-Cost-/a4y5-998d

# Drug-Price-Prediction
<h1>Project Map - Pharmaceutical Drug Predictions</h1>

<h3>BACKGROUND:</h3>  
Pharmaceutical drug spending in the U.S. is on a true upward trend.  Not only is the number of drugs being produced on the rise (see plot???), but the number of Americans taking those drugs is also increasing.  An accurate projection of drug prices enhances transparency of our healthcare system and allows the public, government, and industry to make more informed decisions regarding their health and finances.

<h3>PURPOSE:</h3>
The purpose of the study is to build a machine learning model that can deliver this transparency through the prediction of drug prices.

<h3>ROOT DATA SOURCES:</h3>
Price data comes from the Medicaid.gov site, here.  Patent data comes from the FDA’s Orange Book website, here.

<h3>DATASETS:</h3>
The price dataset has 1M+ rows with 12 columns (though maybe only half of those will be useful).  The Orange Book dataset has roughly 55K rows with 27 columns (half of which could provide predictive power).  As mentioned, the data comes through two (or more) different sources.  While the datasets don’t line up perfectly, I’ve found that drug names in each of the two datasets can be matched reasonably well utilizing Levenshtein distance calculations (via the fuzzywuzzy library).  The caveat is that I’ll need to either do this via a distributed network or using a paralleling system (i.e. Dask).
The Medicaid website does have an API for the dataset.  This will facilitate up-to-date projections of prices in the final product.

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
A handful of the datasets have APIs that I can connect to, and the remainder I plan on scraping and importing the data into the model.  The predictions will be output to a dynamic (live) dashboard where the various types of medications can be selected, and their historical and predicted prices viewed.  I also hope to implement several other pieces of information that will either be displayed (i.e. patent expiry dates) or selectable (i.e. drug delivery route, methods)

<h2>Other Considerations</h2>
<b>QUESTION:</b> What is the effect of a drug’s remaining patent time on the price?
<ul>
  <il><b>DATA REQUIRED:</b> Drug patent information</il>
  <ul>
    <il><b>SOURCE:</b>  FDA Orange Book (listed above)</il>
  </ul>
</ul>
<ul>
  <il><b>PROCESS:</b>  Regress remaining patent time on</il>
  <ul>
    <il><b>CAVEATS:</b> </il>
    <ul>
    <il>There are several different ways that pharmaceutical companies may extend their patent expiry date, so I must be careful to evaluate these dates effectively. 
    <il>Additionally, to date, I’ve yet to be able to merge the patents and prices datasets (via the fuzzywuzzy library – calculating the Levenshtein distance, and Dask)
  </ul>
<il>WHY IT MATTERS:</li> <i>For individuals, elected officials:</i>  
  <ul>
  </il>Pharmaceutical companies argue that patents are a critical incentive for the development of (costly) drugs.  This question sheds light on that statement in the form of regular updates (unlike an academic papers).</li>
  <ul>
•	QUESTION: What is the effect positive/negative news of a drug on the cost of the reported drug?
o	DATA REQUIRED:  News articles (headlines?)
	SOURCE: Google News API (here)
o	PROCESS: Sentiment analysis of news headlines/articles including the name of the drugs.  Inclusion of this analysis as a feature in the prediction of future prices.
	CAVEATS:
•	Accuracy of the sentiment analysis
•	Will its effect (inaccurately) be magnified/reduced when implemented with other features?
o	WHY IT MATTERS: 
	For individuals, insurance companies, pharmacies: In some historical cases, pharmaceutical companies have reduced drug prices based on media attention (particularly to price hikes).
	For pharmaceutical companies: It could be helpful to quantify the amount of “heat” a drug can take as an understanding of how to manage a PR situation as it evolves.
 
•	QUESTION:  Are pharmaceutical companies pricing their drugs on the percentage of the population that require them, or based on the cost of development?
o	DATA REQUIRED: Proportion of the U.S. population with particular diseases (i.e. diabetes), and their location
o	SOURCE(S): Chronic diseases by county – CDC (here), and U.S. population by county (here).  Combining these two will give us the actual number of people estimated with each type of disease.  A friend of mine, a healthcare professional, will help me create a dictionary of the most common disease and the drugs used for treatment (also, potentially data here).
	  Also, I could look at balance sheets (10-Q) from the SEC for each pharmaceutical company in the dataset to obtain revenue/R&D/profit figures
	  Stock share prices could also be considered in place of revenue figures
o	PROCESS:  Join population dataset with chronic disease percentages at the county level.  Then use that to derive a ‘count with disease’ feature.
o	  CAVEATS: 
	Unless I find a dataset correlating the use of specific drugs for specific diseases, I’ll need to cut back on the number of drugs
•	WHY IT MATTERS:
•	This question identifies whether companies interested in the pricing of pharmaceutical drugs should be looking at company revenue, the population needing the drugs, or both.

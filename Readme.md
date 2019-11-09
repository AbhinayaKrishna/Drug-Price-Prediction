<h1><b>Drug Pricing Prediction Model</b></h1> 

In this notebook, we'll aggregate and clean the data for the following notebooks, with the intent to create predictions of pharmaceutical drug prices.

Pharmaceutical companies are not required to publish prices, therefore, we'll be drawing on a dataset from Medicare, who does publish prices.
Articles: 
* [Forbes - Price Transparency: Why are Drug Prices Such a Bitter Pill to Swallow]('https://www.forbes.com/sites/joeharpaz/2019/05/17/price-transparency-why-are-drug-prices-such-a-bitter-pill-to-swallow/#61c45298396d')
* [NADAC pricing in the real world]('https://us.milliman.com/uploadedFiles/insight/2018/NADAC-plus.pdf')

* <b>national_average_drug_acquisition_cost.csv</b>: This dataset comes from surveys produced by the U.S. government to chain and independent pharmacies.  The surveys record the prices paid by retail pharmacies to purchase drug products.  The dataset is updated monthly, with weekly price changes.

    * A data dicationary can be found [here]('https://www.medicaid.gov/medicaid-chip-program-information/by-topics/prescription-drugs/ful-nadac-downloads/nadacdatadefinitions.pdf')
    
    * [Source data]('https://healthdata.gov/dataset/nadac-national-average-drug-acquisition-cost')

The following three files come are gathered from the Orange Book (the FDA's dataset on drug approvals).  Source data & the accompanying dictionary can be found [here]('https://www.fda.gov/drugs/drug-approvals-and-databases/orange-book-data-files').
* <b>products.txt</b>: specific information regarding products registered with the FDA
    * Trade name
    * Applicant
    * New Drug Application (NDA) Number
    * Product Number
    * <b>Approval Date</b>
    * Type
* <b>patent.txt</b>: patent data as available for each drug ([note]('https://www.fda.gov/drugs/development-approval-process-drugs/frequently-asked-questions-patents-and-exclusivity#What_is_the_difference_between_patents_a'), this is different from exclusivity).  Columns of interest:
    * New Drug Application (NDA) Number
    * Product Number
    * Patent Number
    * <b>Patent Expire Date</b>
* <b>exclusivity.txt</b>: data particular to the exclusive marketing rights granted by the FDA to the drug company for a particular drug.  Columns of interest:
    * New Drug Application (NDA) Number
    * Product Number
    * Exclusivity Code
    * <b>Exclusivity Date</b>

Those in bold are of peak interest.  Although the identified columns are those of clear interest, I'll leave the remaining columns in the datasets as I continue exploring.  

I'll use the New Drug Application (NDA) Number to join the information from these three files and then begin cleaning and exploring the data.

As you'll learn later, I'll combine the prices and patent/products/exclusivity datasets via a fuzzy string matching function.

<h1><b>Update on Patent Data</b></h1>

Because I only have 1779 entries for patent dates, I figure I'll need more data for my predictive model.  As it turns out, [patents issued after 1995]('http://www.drugsdb.com/blog/how-long-is-a-drug-patent-good-for.html') are valid for 20 years from the patent application filing (assuming maintenance fees are paid every 3.5, 7.5, and 11.5 years after the patent is granted).  From this, I can extrapolate two things: 

* I should be able to populate the 'Patent_Expire_Date_Text' column based on 'Patent_Submission_Date'.  I'll add this information to a third column instead of filling in the NaN values of the 'Patent_Submission_Date' so I can identify any deviations  the results with the actual 'Patent_Expire_Date_Text' information that I imported earlier.
    * Additional factors to consider: 
        * Hatch-Waxman extension: A drug can obtain a patent extension of 5 years to make up the length of the FDA approval process.
        * Pediatric exclusivity extension: drugs tested on children can gain an extra 6 months of patent protection (this can be used twice)
        * Drug reformulations: i.e. turning an drug taken by injection into a nasal spray version, or modifying dosages, can extend a patent for an additional up to 5 years
        * New uses: Drugs whose new uses are discovered can obtain another 3 years of patent protection
        * Orphan drugs (those treating rare diseases) gain an additional 7 years of patent protection (and the FDA can't approve any competing generics during the time)
        * 30-Month Stays: Generics often issue a competing patent, and are sued by the brand-name company.  This initiates a 30-month stay on the FDA approval of the generic.
            * Few drug companies can take advantage of this
        * Most of the methods above can be combined to secure a longer patent
* Any drugs with patent issue dates before 1995 may not be valid for prediction as the law governing these patents apparently changed

I'll evaluate the dates we currently have to see if a pattern is evident, before combining them with new estimations based on the factors above.



<h1><b>Other datasets:</b></h1>
* [Pharmaceutical Preparation Manufacturing - Producer Price Index by Industry]('https://fred.stlouisfed.org/series/PCU325412325412')
    * [Breakdown of the above]('https://fred.stlouisfed.org/release/tables?rid=46&eid=135301#snid=135309')
    
* [Producer Price Index by Industry: Pharmacies and Drug Stores: Retailing of Prescription Drugs]('https://fred.stlouisfed.org/series/PCU4461104461101')
* SEC 10-k/10-q data --> pharma companies' financial data (R&D, Profits, Revenue)
* Pharma stock prices over time (proxy for SEC data?)
* Number of pieces of legislation pertaining to pharmaceuticals (may need sentiment analysis for these to determine if they're pro/contra pharma)
* Number of news stories regarding pharmaceuticals
* Pharmacy Benefit Manager (PBM) stock prices (proxy with pharma stock prices for the cost of pharmaceuticals to consumers)?

<h1><b>Other Information:</b></h1>
## A few definitions:
* A __drug product__ is a finished dosage form, e.g., tablet, capsule, or solution, that contains a drug substance, generally, but not necessarily, in association with one or more other ingredients. 
    * e.g. formulation and composition
* A __drug substance__ is an active ingredient that is intended to furnish pharmacological activity or other direct effect in the diagnosis, cure, mitigation, treatment, or prevention of disease or to affect the structure or any function of the human body, but does not include intermediates used in the synthesis of such ingredient. 
    * e.g. active ingredient
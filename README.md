# NFL Draft Scouting Reports and Predictions

# **Author**: Josh Palgon

![Combine](./Images/Combine.png)

[my Jupyter Notebooks](https://github.com/jpalgon/Draft_Stats)

## Overview

The NFL Draft is the most important process in acquiring talented players. 

I am going to give any prespective team insight into when players will be selected.

The combine and college stats data was web scraped from sports-reference.com. The scouting reports and draft grades were taken from ESPN.

The length of the scouting report is a decent indicator of where in the draft a player will be taken.

Overall player rank and draft grade were by far the most important features in determining where a player will get selected. This not surprising at all as teams are trying to pick the best players. 

My model was better at predicting the first round of the draft than any other round.

## Business Problem

Any NFL team is always looking for any minor edge to build a better football team. With the NFL Draft being the best way to improve a team, being able to know which day a player will be drafted or if they will be drafted at all would be extremely valuable. I am offering my skills, services, and research on the draft to any team who is interested.

While there are several applications to classifying which day a player will get drafted. The primary application would be using a players' expected draft round as a tie-breaker. By selecting the player who is likely to get drafted earlier, there is a chance that they can select the other player later in the draft.

## Data

The combine and college stats data was web scraped from sports-reference.com. One major obstacle in scraping sports-reference is the secondary statistics for a player appear to be unscrapable. For example for QBs I only have their passing data but not their rushing information. While this is obviously not ideal, the addition of the combine testing data and scouting reports should help offset the loss of secondary information.

I used a sleep-timer of 3.15 to adhere to sports-references web scraping restrictions. They do update their page so I proved the link here https://www.sports-reference.com/bot-traffic.html in case anyone trying to replicate this process runs into any 429 HTTP Error requests.

To get 

Additionally, I supplemented the sportsreference data with the NFL_data Python package for a few extra features.

## Modeling

Knowing that not all athletic testing results are the same across positions and body types. I did feature engineering to create 3 scores (speed, cone agility, and shuttle agility) that factors weight into the 40 yard dash, 3 cone drill, and shuttle run. The speed score was created by Bill Barnwell in 2008. Since shuttle run times were on a similar scale to the 40 yard dash I just replaced the 40 yard dash time of his equation with the shuttle run times. 3 cone drill was slightly larger so I slightly tinkered with the formula to try and put 3 cone drill on the same scale as the 40 year dash and shuttle run. 

For my modeling I separated my numeric columns from my categorical columns. On my categorical columns, I OneHotEncoded them. On my numerical columns, I used a simple imputer to handle the NaNs and impute 0 as any NaN should be 0 anyway based on how I scraped my data. Additionally, I used a StandardScaler on the numerical data. I had a very balanced class dataset so StandardScaler was appropriate.

I ran 6 different models:
- GaussianMixture
- Decision Tree
- Random Forest
- KNN
- XGBoost
- Sequential Neural Network

### TSNE of GaussianMixture Model
![TSNE](./Images/TSNE.png)

For my first model, I did some unsupervised learning in an attempt to see how the model would group my data and what patterns it may find. It did a pretty good job of sorting the data into positions and even kept similar positions together like (OL, DL, DE, and DT), (WR, TE, and FB), (DB, CB, and S), and (K and P). However just using the four features groups it created did not lead to a good model result. The Sequential Neural Network returnedd similar poor results.

### Random Forest Matrix
![Matrix](./Images/matrix.png)

The Random Forest, Decision Tree, XGBoost, and KNN models all performed fairly well with an accuracy range of .55 to .63 and all did very well at classifying undrafted players. The Random Forest had the second best recall score for class 0 but the highest f1, recall, and precision scores for every other class metric combination along with the best accuracy so it was the clear winner.

## Evaluation

### Top Correlated Features with Round
![Corr](./Images/Corr.png)

All 3 features I engineered were towards the top including speed being the top metric. More top offensive than defensive stats. Final season stats appeared instead of career stats except for QB stats.

### QB Athletic Testing
![QB Bench Reps](./Images/qbbench.png)
![QB Speed](./Images/qbspeed.png)

While bench reps wasn't actually super important overall it did help distinguish between drafted and undrafted players for QBs. However the speed score helped separate the round 1-3 QBs from the rest of the group.

### OL Athletic Testing
![OL Speed](./Images/olspeed.png)
![OL Agility](./Images/olagility.png)

Even though OL do not have any college statistics I could use, it did have some very important athletic testing scores. Both the speed shuttle agility scores were the best for the day 1 picks, the worst for undrafted OL and in the middle but still separated from both for the day 3 OL.

## Conclusions

Combine athletic testing can be a very good separator for the day a player will be drafted especially when weight is combined with a speed or agility test.

Offensive college stats bear more weight than defensive stats while the final year of a college career is more important than the career college statistics with QBs being an exception.

My model can be very useful for predicting whether a player will be drafted or not which would be of great interest to NFL teams in day 3 of the draft.

## Next steps:

Get more data
- Advanced stats
- Non Primary Stats
- More bio information
- Medical information? (not sure how well good medical data for college prospects would be)

Use NLP on scouting reports.

## What I learned

You can never spend too much time cleaning and doing EDA. While I don't think my results would have been drastically different, there were a few areas I wish I had more time to spend on (college conference had missing values I could have gotten had I not needed to keep pushing on). Additionally, I would have loved to spend more time thinking about and trying feature engineering especially considering the success I had with the 3 ones I used in this project.

## For More Information

Please look at my full analysis in [my Jupyter Notebooks](https://github.com/jpalgon/draft_scouting) or my [presentation](./ScoutingCombine.pdf).

For any additional questions, please contact:

<ul>
    <li>Josh Palgon (jopalgon@gmail.com)</li>
</ul>

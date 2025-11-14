The dataset used for this project (IPL matches data) is stored in Google Drive.
You can access it using the following link: https://drive.google.com/file/d/1n5jwqfNTPrPEYFyHTEjlOLodVKCLcwQh/view?usp=drive_link

# Smart Cricket Score Predictor (DS)

**Short description**  
I built a simple, beginner-friendly project that uses IPL ball-by-ball data to display match insights and predict final innings totals based on the first 10 overs. This is a small data-science experiment using linear regression and a few visualizations.

**Motivation / why I made it**  
I made this to practice basic feature engineering and regression modeling on sports data. Cricket has lots of interesting time-series-like events (overs/balls), so I wanted to see how much the first 10 overs can tell us about the final total. It's also useful for learning how to clean ball-by-ball datasets and present quick match insights.

**Key features / what it does**
- Loads ball-by-ball IPL-style data (CSV)
- Computes inning-level features at the 10-over mark (runs, wickets, powerplay, last-5-overs)
- Trains a simple Linear Regression model to predict final innings total
- Prints evaluation metrics (MAE, R²) and some sample predictions
- Shows feature importance using model coefficients
- Draws a few visualizations (histogram of totals, predicted vs actual scatter, run progression, top batsmen bar chart)

**Tech stack and versions**
- Python 3.10+ (I used 3.11 locally) — works with 3.8+ generally
- pandas (>=1.3)
- numpy
- scikit-learn (>=1.0)
- matplotlib (for plots)
- pathlib (standard library)
- No additional libraries required

**How to run**
1. Put the dataset CSV in the project folder.

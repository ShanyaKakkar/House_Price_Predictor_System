# 🏛️ Estate Valuation — House Price Prediction System
**AIML Summer Internship 2026 | IIHMF, MNNIT Allahabad**

An AI-powered house price prediction system with a luxury real-estate themed
web app (white / charcoal / gold palette), built using Python, scikit-learn,
XGBoost, and Streamlit.

---

## 📁 Folder Structure
```
house_price_app/
│
├── Dataset/
│   └── housing.csv
├── Notebook/
│   ├── generate_dataset.py     # creates the dataset
│   └── train_model.py          # trains & evaluates 3 models
├── Model/
│   ├── house_price_model.pkl   # best trained pipeline (auto-selected)
│   ├── best_model_name.pkl
│   └── feature_info.pkl
├── Streamlit_App/
│   └── app.py                  # the web app
├── Documentation/
│   └── model_comparison.csv    # MAE/MSE/RMSE/R2 for all 3 models
├── requirements.txt
└── README.md
```

## ⚙️ Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Optional) Regenerate dataset — or replace house_prices.csv with your
#    own Kaggle dataset (keep the same column names, or edit train_model.py)
python Notebook/generate_dataset.py

# 3. Train models (creates the .pkl files used by the app)
python Notebook/train_model.py

# 4. Run the app
cd Streamlit_App
streamlit run app.py
```

## 🧠 Models Trained
| Model | Purpose |
|---|---|
| Linear Regression | Baseline |
| Random Forest Regressor | Non-linear, handles interactions |
| XGBoost Regressor | Best performing (gradient boosting) |

The best model (by R² Score) is auto-selected and saved as
`Model/house_price_model.pkl`.

## 📊 Evaluation Metrics
MAE, MSE, RMSE, R² Score — saved in `Documentation/model_comparison.csv`.

## 🎨 UI Theme — Luxury Real Estate
- Dominant: `#FFFFFF` (Pure White)
- Secondary: `#1A1A1A` (Charcoal Black)
- Accent: `#D4AF37` (Muted Gold)

## 🔁 Using Your Own Dataset
Replace `Dataset/house_prices.csv` with your Kaggle dataset. Make sure it has
these columns (or rename in `train_model.py` and `app.py` accordingly):
`area_sqft, bedrooms, bathrooms, age_years, location, parking_spaces, furnishing, price`

## 👤 Author
Shanya Kakkar — B.Tech CSE, United College of Engineering and Research

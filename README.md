# BreastAI — Breast Cancer Prediction Platform
### Multi-Model Clinical Decision Support Prototype

A machine learning platform that analyses 30 diagnostic measurements from 
fine needle aspirate (FNA) imaging to classify breast tumours as benign or 
malignant — with live model switching across 5 classifiers and 
SHAP-powered interpretability.

![Home Dashboard](screenshots/home.png)

---

## Why This Project

Most classification projects stop at "here's my accuracy score." This one 
asks a more clinically relevant question: **in a cancer diagnosis context, 
what should the model actually be optimising for?**

False negatives (missing a malignant tumour) carry far higher risk than 
false positives — so model selection here prioritises **recall first**, 
then ROC-AUC, then accuracy. SVM was selected as the best-performing model 
under this priority order, not simply the one with the highest accuracy.

---

## Live Demo

🔗 **[Try the app here](#)** *(add your Streamlit Cloud link once deployed)*

Or run it locally:
```bash
pip install -r requirements.txt
streamlit run app.py
```
Opens at `http://localhost:8501`

---

## How It Works

| Page | What It Does |
|---|---|
| **Home** | Platform overview and key stats |
| **Assessment** | Input 30 diagnostic measurements (mean, standard error, worst values) |
| **Results** | Prediction, confidence score, probability breakdown, and clinical interpretation |
| **About** | Dataset info, model comparison, and evaluation metrics |

![Clinical Assessment Input](screenshots/assessment.png)

![Diagnosis Results Dashboard](screenshots/results-dashboard.png)

Users can switch between all 5 trained models from the sidebar and see 
predictions update instantly — useful for comparing how different 
algorithms weigh the same case.

![Feature Values Table](screenshots/feature-values.png)

---

## Model Performance

| Model | Recall | ROC-AUC | Accuracy | Rank |
|---|---|---|---|---|
| **SVM** | **0.97** | 0.99 | 0.97 | **Best** |
| Random Forest | 0.95 | 0.99 | 0.96 | 2nd |
| Logistic Regression | 0.95 | 0.99 | 0.95 | 3rd |
| KNN | 0.94 | 0.98 | 0.95 | 4th |
| Decision Tree | 0.90 | 0.93 | 0.92 | 5th |

**Selection priority:** Recall → ROC-AUC → Accuracy — chosen deliberately 
to minimise missed malignant cases.

---

## Interpretability

The underlying notebook includes SHAP (SHapley Additive exPlanations) 
analysis — summary plots, feature importance, and individual prediction 
waterfalls — so the model's reasoning isn't a black box. This matters in 
any clinical or health-adjacent context, where "the model said so" isn't 
a sufficient explanation.

---

## Dataset

**Breast Cancer Wisconsin (Diagnostic) Dataset** — UCI Machine Learning Repository
- 569 samples, 30 numeric features
- Target: Malignant (212) / Benign (357)

Dataset not included in this repo — the app runs entirely from pre-trained 
models in the `models/` folder. See `notebooks/` for the full training 
pipeline if you want to retrain from scratch.

---

## Tech Stack
`Python` · `scikit-learn` · `Streamlit` · `SHAP` · `pandas` · `NumPy` · `Plotly`

---

## Disclaimer
This is a decision-support prototype for educational and portfolio 
purposes. It is not a certified medical device and must not be used as a 
sole basis for clinical diagnosis.

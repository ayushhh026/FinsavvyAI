"""
FinSavvy AI — Query Intent Classifier
======================================
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
import pickle
import os
import sys

TRAINING_DATA = [
    # TAX
    ("What is Section 80C?", "tax"),
    ("How much can I save under 80D?", "tax"),
    ("What is the tax slab for 10 lakhs income?", "tax"),
    ("Explain HRA exemption rules", "tax"),
    ("What is TDS and how is it calculated?", "tax"),
    ("Can I claim deduction on home loan interest?", "tax"),
    ("What is the standard deduction for salaried employees?", "tax"),
    ("How to save tax on capital gains?", "tax"),
    ("What is advance tax and who should pay it?", "tax"),
    ("Explain new tax regime vs old tax regime", "tax"),
    ("What are the GST slabs in India?", "tax"),
    ("How to file ITR online?", "tax"),
    ("What is Form 16 and how to use it?", "tax"),
    ("Tax benefits on NPS contribution", "tax"),
    ("What is surcharge on income tax?", "tax"),
    ("How is long term capital gain taxed?", "tax"),
    ("What is presumptive taxation scheme?", "tax"),
    ("Deductions allowed under section 80G", "tax"),
    ("What is the tax on FD interest?", "tax"),
    ("How to claim LTA exemption?", "tax"),
    ("What is the difference between TDS and TCS?", "tax"),
    ("Section 44AD for small business", "tax"),
    ("How much tax do I pay on salary of 8 lakhs?", "tax"),
    ("Is life insurance premium tax deductible?", "tax"),
    ("What is professional tax?", "tax"),
    ("Income tax on rental income rules", "tax"),
    ("How to avoid double taxation?", "tax"),
    ("What is AMT in income tax?", "tax"),
    ("Can I claim both HRA and home loan?", "tax"),
    ("ELSS tax saving mutual funds", "tax"),
    ("What is the last date to file ITR?", "tax"),
    ("How to calculate taxable income?", "tax"),
    ("What is section 87A rebate?", "tax"),
    ("How much tax on 15 lakh salary?", "tax"),
    ("What is LTCG and STCG?", "tax"),
    ("How to file revised ITR?", "tax"),
    ("What is exempt income in India?", "tax"),
    ("Tax on dividend income in India", "tax"),
    ("What is the penalty for late ITR filing?", "tax"),
    ("How to claim 80C deduction for ELSS?", "tax"),
    ("What is section 10 exemptions?", "tax"),
    ("How is freelancer income taxed in India?", "tax"),
    ("What is agricultural income tax rule?", "tax"),
    ("How to save tax for self employed person?", "tax"),
    ("What is Form 26AS?", "tax"),
    ("How to download AIS from income tax portal?", "tax"),
    ("What is the basic exemption limit in India?", "tax"),
    ("Can I claim 80C and 80CCD both?", "tax"),
    ("What is the tax on EPF withdrawal?", "tax"),
    ("How is house property income calculated for tax?", "tax"),

    # DOCUMENT
    ("What does my ITR say?", "document"),
    ("Summarize my uploaded salary slip", "document"),
    ("What is written in the document I uploaded?", "document"),
    ("Read my PDF", "document"),
    ("What are the values in my form?", "document"),
    ("Check my uploaded file", "document"),
    ("What income is shown in my document?", "document"),
    ("Extract data from my file", "document"),
    ("What does the first page say?", "document"),
    ("Show me details from the uploaded document", "document"),
    ("What is the total in my statement?", "document"),
    ("Analyse my bank statement", "document"),
    ("What transactions are in my uploaded file?", "document"),
    ("Read the document and tell me my tax liability", "document"),
    ("From the file I uploaded what is my gross salary?", "document"),
    ("What does my form 16 show?", "document"),
    ("Check my investment statement", "document"),
    ("What is my net salary from the document?", "document"),
    ("My uploaded PDF has details about my loan", "document"),
    ("Tell me what my capital gains statement says", "document"),
    ("Based on my document how much tax do I owe?", "document"),
    ("The file I shared earlier what does it contain?", "document"),
    ("Check my uploaded image", "document"),
    ("What numbers are in my statement?", "document"),
    ("Read the receipt I uploaded", "document"),
    ("What is my PF balance from the document?", "document"),
    ("Summarize the file I just uploaded", "document"),
    ("What is written on page 2 of my document?", "document"),
    ("Find the total deductions in my uploaded payslip", "document"),
    ("What is the date on my uploaded document?", "document"),
    ("Extract my PAN number from the uploaded file", "document"),
    ("What does the image I uploaded say?", "document"),
    ("Read my uploaded invoice", "document"),
    ("What are the line items in my uploaded bill?", "document"),
    ("Check my uploaded tax document", "document"),
    ("What is my employer name in the document?", "document"),
    ("How much is the EMI shown in my loan document?", "document"),
    ("What is the account number in my statement?", "document"),
    ("Tell me the closing balance from my bank statement", "document"),
    ("What is written in the scanned document?", "document"),
    ("Read the PDF I shared", "document"),
    ("Extract text from my uploaded image", "document"),
    ("What does my uploaded form contain?", "document"),
    ("Show the data from my uploaded file", "document"),
    ("Analyse the document I provided", "document"),

    # GENERAL FINANCE
    ("What is a mutual fund?", "general_finance"),
    ("How does SIP work?", "general_finance"),
    ("What is the difference between stocks and bonds?", "general_finance"),
    ("How to start investing in India?", "general_finance"),
    ("What is an emergency fund?", "general_finance"),
    ("How does compound interest work?", "general_finance"),
    ("What is a fixed deposit?", "general_finance"),
    ("Explain CIBIL score and how to improve it", "general_finance"),
    ("What is term insurance?", "general_finance"),
    ("How to plan for retirement in India?", "general_finance"),
    ("What is the difference between savings and investment?", "general_finance"),
    ("What is PPF and how to open an account?", "general_finance"),
    ("How does UPI work?", "general_finance"),
    ("What is a credit card and how to use it wisely?", "general_finance"),
    ("How to budget monthly expenses?", "general_finance"),
    ("What is inflation and how does it affect savings?", "general_finance"),
    ("Explain portfolio diversification", "general_finance"),
    ("What is NAV in mutual funds?", "general_finance"),
    ("What is an index fund?", "general_finance"),
    ("How to open a demat account?", "general_finance"),
    ("What is the repo rate set by RBI?", "general_finance"),
    ("Explain home loan EMI calculation", "general_finance"),
    ("What is a nominee in insurance?", "general_finance"),
    ("How does gold investment work in India?", "general_finance"),
    ("What is a balance sheet?", "general_finance"),
    ("What is a recurring deposit?", "general_finance"),
    ("How to close a credit card?", "general_finance"),
    ("What is the difference between term and whole life insurance?", "general_finance"),
    ("How does stock market work in India?", "general_finance"),
    ("What is SEBI and what does it do?", "general_finance"),
    ("How to calculate EMI manually?", "general_finance"),
    ("What is a sovereign gold bond?", "general_finance"),
    ("How to invest in real estate in India?", "general_finance"),
    ("What is the difference between NEFT RTGS and IMPS?", "general_finance"),
    ("What is a health insurance policy?", "general_finance"),
    ("How does credit score affect loan eligibility?", "general_finance"),
    ("What is NSC National Savings Certificate?", "general_finance"),
    ("How to track expenses and save money?", "general_finance"),
    ("What is the difference between growth and dividend mutual fund?", "general_finance"),
    ("How to invest in US stocks from India?", "general_finance"),
    ("What is dollar cost averaging?", "general_finance"),
    ("Explain the concept of net worth", "general_finance"),
    ("What is a pension plan in India?", "general_finance"),
    ("How does cashback on credit card work?", "general_finance"),
    ("What is the difference between liquid fund and savings account?", "general_finance"),

    # MEMORY
    ("What did I ask earlier?", "memory"),
    ("What was my previous question?", "memory"),
    ("What did we discuss before?", "memory"),
    ("Remind me what you said about my tax", "memory"),
    ("What was the answer you gave me before?", "memory"),
    ("Go back to what we talked about", "memory"),
    ("What did you tell me earlier about 80C?", "memory"),
    ("Repeat your last answer", "memory"),
    ("What was the first question I asked?", "memory"),
    ("Summarize our conversation so far", "memory"),
    ("What have we discussed in this session?", "memory"),
    ("Earlier you mentioned something about HRA", "memory"),
    ("What was my question about capital gains?", "memory"),
    ("Can you recall what I said about my salary?", "memory"),
    ("Look at our chat history and answer", "memory"),
    ("What did you explain to me earlier?", "memory"),
    ("I forgot what you said please repeat", "memory"),
    ("Based on our earlier discussion", "memory"),
    ("You told me something about tax earlier", "memory"),
    ("What was the calculation you did before?", "memory"),
    ("Go through our previous messages", "memory"),
    ("What was the last thing we talked about?", "memory"),
    ("Earlier in this chat you mentioned", "memory"),
    ("Recall my previous query", "memory"),
    ("What questions have I asked so far?", "memory"),
    ("From our earlier conversation what was the answer?", "memory"),
    ("You gave me a number earlier what was it?", "memory"),
    ("What did we conclude about my investment?", "memory"),
    ("Based on what we discussed before", "memory"),
    ("Can you go back to the previous answer?", "memory"),

    # MIXED
    ("Based on tax rules how much deduction can I claim from my document?", "mixed"),
    ("Using my salary slip calculate my tax liability", "mixed"),
    ("My document shows income of 12 lakhs what tax should I pay?", "mixed"),
    ("Explain the deductions in my uploaded Form 16", "mixed"),
    ("From my investment statement which are tax saving?", "mixed"),
    ("What tax can I save based on my uploaded document?", "mixed"),
    ("My ITR shows capital gains can you explain the tax on it?", "mixed"),
    ("Check my uploaded file and tell me which section applies", "mixed"),
    ("Based on my bank statement and tax rules am I eligible for refund?", "mixed"),
    ("Analyse my salary slip for tax planning", "mixed"),
    ("From my payslip calculate my tax saving under 80C", "mixed"),
    ("My document shows FD interest can you tell me the tax on it?", "mixed"),
    ("Using my uploaded form 16 tell me my net tax payable", "mixed"),
    ("Check my investment statement and explain which ones save tax", "mixed"),
    ("My salary slip shows HRA how much exemption can I claim?", "mixed"),
    ("Calculate tax on the income shown in my document", "mixed"),
    ("From my uploaded ITR what deductions have I already claimed?", "mixed"),
    ("Based on my bank statement am I paying correct advance tax?", "mixed"),
    ("My uploaded document shows capital gains which ITR should I file?", "mixed"),
    ("From my payslip and tax rules how much refund will I get?", "mixed"),
    ("Explain the tax implications of what is shown in my document", "mixed"),
    ("Using my uploaded statement plan my tax saving investments", "mixed"),
    ("My document shows home loan details what tax benefit do I get?", "mixed"),
    ("From my salary slip calculate take home after all deductions", "mixed"),
    ("Based on my uploaded form 16 am I in which tax slab?", "mixed"),
]

TEXTS = [t for t, _ in TRAINING_DATA]
LABELS = [l for _, l in TRAINING_DATA]

MODEL_PATH = "intent_classifier.pkl"


def train_classifier():
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),     
            max_features=3000,       # changed from 5000
            sublinear_tf=False       
        )),
        ("clf", LogisticRegression(
            max_iter=1000,
            C=5.0,                   
            class_weight=None        
        ))
    ])
    pipeline.fit(TEXTS, LABELS)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(pipeline, f)
    print(f"[Classifier] Trained and saved to {MODEL_PATH}")
    return pipeline


def load_classifier():
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    return train_classifier()


_classifier = load_classifier()


def classify_intent(query: str) -> str:
    if not query or not query.strip():
        return "general_finance"
    intent = _classifier.predict([query.strip()])[0]
    confidence = max(_classifier.predict_proba([query.strip()])[0])
    print(f"[Classifier] Query: '{query[:60]}...' → Intent: {intent} (confidence: {confidence:.2f})")
    if confidence < 0.45:
        print(f"[Classifier] Low confidence ({confidence:.2f}), falling back to mixed")
        return "mixed"
    return intent


INTENT_SOURCE_MAP = {
    "tax":             ["ca_books"],
    "document":        ["documents"],
    "general_finance": ["txt_knowledge"],
    "memory":          ["memory"],
    "mixed":           ["ca_books", "txt_knowledge", "documents"],
}


def get_sources_for_intent(intent: str) -> list:
    return INTENT_SOURCE_MAP.get(intent, ["ca_books", "txt_knowledge"])


def retrain():
    global _classifier
    _classifier = train_classifier()
    print("[Classifier] Retrained successfully.")


def tune_classifier():
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", LogisticRegression(max_iter=1000))
    ])
    param_grid = {
        "tfidf__ngram_range":  [(1, 1), (1, 2), (1, 3)],
        "tfidf__max_features": [3000, 5000, 8000],
        "tfidf__sublinear_tf": [True, False],
        "clf__C":              [0.1, 1.0, 5.0, 10.0],
        "clf__class_weight":   ["balanced", None],
    }
    grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring="f1_weighted", verbose=1)
    grid_search.fit(TEXTS, LABELS)
    print("\n=== BEST PARAMETERS ===")
    print(grid_search.best_params_)
    print(f"\nBest F1 Score: {grid_search.best_score_:.4f}")
    best_model = grid_search.best_estimator_
    predictions = best_model.predict(TEXTS)
    print("\n=== CLASSIFICATION REPORT ===")
    print(classification_report(LABELS, predictions))
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(best_model, f)
    print(f"\n[Classifier] Best model saved to {MODEL_PATH}")
    return best_model


if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1] == "tune":
        print("Running hyperparameter tuning... this takes 1-2 minutes\n")
        tune_classifier()

    else:
        test_queries = [
            "What is Section 80C?",
            "Summarize my uploaded salary slip",
            "How does SIP work?",
            "What did I ask earlier?",
            "Using my form 16 calculate my tax",
            "What is the last date to file ITR?",
            "Read the PDF I shared",
            "What is a recurring deposit?",
            "Based on our earlier discussion",
            "From my payslip calculate my 80C saving",
        ]
        print("\n=== Intent Classifier Test ===\n")
        for q in test_queries:
            intent = classify_intent(q)
            sources = get_sources_for_intent(intent)
            print(f"Query   : {q}")
            print(f"Intent  : {intent}")
            print(f"Sources : {sources}")
            print()
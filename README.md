# 💰 My Tax Diary — AUS Personal Tax & Finance Prep Tool

> **This tool does not provide tax advice. It helps organise records for tax return preparation.**

🌐 **Live web app:** https://tinasitu.github.io/week4-tax-tool

---

## What is this?

A daily expense and income tracker for Australian PAYG employees with investment properties. Record every transaction throughout the year — the tool automatically categorises what's tax-deductible and what's not, so when tax time comes, everything is already organised.

**Solves a real problem:** Every year I spend hours hunting through bank statements and receipts to prepare for my tax return. This tool lets me record expenses as they happen, already mapped to ATO categories, so lodgement is fast.

---

## Who is it for?

- Australian residents earning **PAYG salary/wages**
- People with an **investment property** (rental income + expenses)
- Anyone who wants to stay on top of **tax deductions** throughout the year

---

## How to use

### Option 1 — Web app (recommended)
Open https://tinasitu.github.io/week4-tax-tool in any browser. No installation needed. Data saves automatically in your browser.

**Three tabs:**
- **Daily Log** — record any expense or income, auto-tagged as deductible or personal
- **Rental** — record rent received and all property expenses (14 ATO categories)
- **Tax Summary** — full ATO breakdown, export CSV for your tax agent

### Option 2 — Python CLI
```bash
python3 tax_prep.py
```
Requires Python 3.8+. No third-party packages needed.

---

## ATO categories covered

| Section | ATO Reference | Details |
|---|---|---|
| Work deductions | D1–D15 | Car, travel, clothing, education, donations, super, tax affairs |
| Rental income | IITR Item 20 | Gross rent received |
| Rental expenses | Item 20 | 14 categories: interest, agent fees, rates, insurance, repairs, depreciation, and more |
| PAYG income | Label 1, 12 | Salary, tax withheld |

---

## Technical requirements

| Requirement | Where |
|---|---|
| ≥ 3 custom functions | `calculate_payg_summary()`, `calculate_rental_income()`, `calculate_deductions()`, `generate_tax_summary()`, `export_summary_csv()` in `tax_prep.py` |
| Loop + conditional | `for` loops + `if` checks in every calculate function |
| Dictionary for data storage | `ato_deduction_labels`, `ato_expense_categories`, `options` menu dict |
| try/except error handling | `load_json()`, `save_json()`, all calculate functions |
| Save to local JSON + CSV | `data/` folder for JSON, `records/` for CSV exports |
| Git branch development | `feature/income`, `feature/rental`, `feature/deductions` — all merged to `main` |

---

## File structure

```
week4-tax-tool/
├── index.html          # Web app (Daily Log + Rental + Tax Summary)
├── tax_prep.py         # Python CLI version
├── README.md
├── .gitignore
└── data/               # Sample JSON data (local use)
    ├── income_2024-25_sample.json
    ├── property_2024-25_sample.json
    └── deductions_2024-25_sample.json
```

---

## ATO record-keeping reminder

ATO requires rental property records to be kept for **5 years** from the date you lodge your return. Export your data regularly using the CSV export button.

---

## Disclaimer

This tool does not provide tax advice. It helps organise records for tax return preparation. Always consult a registered tax agent or visit [ato.gov.au](https://ato.gov.au) for advice on your specific situation.

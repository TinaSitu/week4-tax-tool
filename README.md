# 🇦🇺 AUS Personal Tax & Finance Prep Tool

> **This tool does not provide tax advice. It helps organise records for tax return preparation.**

---

## What is this?

A Python CLI tool that helps PAYG employees with investment properties organise their tax records before visiting a tax agent or filing through myTax. It mirrors the structure of the ATO's Individual Income Tax Return (IITR) and Rental Schedule.

**Solves a real problem:** Every year I spend hours hunting through bank statements, invoices, and emails to pull together numbers for my tax return. This tool provides one place to record everything throughout the year — structured exactly how the ATO wants it.

---

## Who is it for?

- Australian residents who earn **PAYG salary/wages** (one or more employers)
- People who also have an **investment property** (rental income + expenses)
- Anyone who wants to **stay organised** with deductions throughout the year

---

## Features

| Section | ATO Reference | What it tracks |
|---|---|---|
| PAYG Income | IITR Label 1, 12 | Gross income, tax withheld, super per employer |
| Rental Schedule | IITR Item 20 | Gross rent, 17 ATO expense categories |
| Deductions | IITR Labels D1–D15 | Work car, travel, clothing, education, donations, etc. |
| Summary | All of above | Estimated taxable income, exportable CSV |

---

## Technical requirements met

| Requirement | Where |
|---|---|
| ≥ 3 custom functions | `calculate_payg_summary()`, `calculate_rental_income()`, `calculate_deductions()`, `generate_tax_summary()`, `export_summary_csv()` |
| Loop + conditional | `for emp in employers` / `if label in ato_deduction_labels` in every calculate function |
| Dictionary for data storage | `ato_deduction_labels`, `ato_expense_categories`, `options` menu dict |
| try/except error handling | All calculate functions + `load_json()` + `save_json()` |
| Save to local JSON + CSV | `save_json()` → `data/`, `export_summary_csv()` → `records/` |
| Git branch development | See Git history — features developed on `feature/income`, `feature/rental`, `feature/deductions`, merged back to `main` |

---

## How to run

### Prerequisites
- Python 3.8 or higher
- No third-party packages required (standard library only)

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/aus-tax-prep.git
cd aus-tax-prep

# 2. Run the tool
python tax_prep.py

# 3. Follow the menu prompts
#    1. Add PAYG income
#    2. Add rental property income/expenses
#    3. Add deductions
#    4. View & export summary (generates data/summary_YYYY-YY.json and records/summary_YYYY-YY.csv)
```

### File structure after use

```
aus-tax-prep/
├── tax_prep.py              # Main program
├── README.md
├── data/                    # JSON records (auto-created)
│   ├── income_2024-25.json
│   ├── property_2024-25.json
│   ├── deductions_2024-25.json
│   └── summary_2024-25.json
└── records/                 # CSV exports (auto-created)
    └── summary_2024-25.csv
```

---

## ATO compliance notes

- **Record keeping**: ATO requires rental property records to be kept for **5 years** from the date you lodge your tax return. This tool reminds you of this requirement.
- **Rental expenses**: All 17 ATO-recognised rental expense categories are included (per ATO Rental properties guide).
- **Deductions**: Labels match ATO IITR deduction labels D1–D15.
- **myDeductions compatibility**: Category structure mirrors ATO's myDeductions app for easy cross-reference.

---

## Disclaimer

This tool does not provide tax advice. It helps organise records for tax return preparation. Always consult a registered tax agent or the ATO (ato.gov.au) for advice on your specific situation.

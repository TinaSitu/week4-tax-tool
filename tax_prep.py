"""
Australian Personal Tax & Finance Prep Tool
For PAYG employees with investment properties.
Organises records for ATO tax return preparation (ATO forms: IITR, rental schedule).

DISCLAIMER: This tool does not provide tax advice.
It helps organise records for tax return preparation.
"""

import json
import csv
import os
from datetime import datetime, date

DATA_DIR = "data"
RECORDS_DIR = "records"


# ─── Data storage helpers ────────────────────────────────────────────────────

def load_json(filename: str) -> dict:
    """Load a JSON file; return empty dict if not found."""
    path = os.path.join(DATA_DIR, filename)
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        print(f"  [Warning] Could not parse {filename}: {e}")
        return {}


def save_json(filename: str, data: dict) -> None:
    """Save data to a JSON file (creates DATA_DIR if needed)."""
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, filename)
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2, default=str)
        print(f"  ✓ Saved to {path}")
    except OSError as e:
        print(f"  [Error] Could not save {filename}: {e}")


def export_summary_csv(summary: dict, filename: str) -> None:
    """Export a flat summary dict to CSV for easy viewing in Excel/Sheets."""
    os.makedirs(RECORDS_DIR, exist_ok=True)
    path = os.path.join(RECORDS_DIR, filename)
    try:
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Field", "Value"])
            for k, v in summary.items():
                writer.writerow([k, v])
        print(f"  ✓ CSV exported to {path}")
    except OSError as e:
        print(f"  [Error] Could not export CSV: {e}")


# ─── Core domain functions ───────────────────────────────────────────────────

def get_financial_year() -> str:
    """Return the current ATO financial year string, e.g. '2024-25'."""
    today = date.today()
    if today.month >= 7:
        return f"{today.year}-{str(today.year + 1)[-2:]}"
    else:
        return f"{today.year - 1}-{str(today.year)[-2:]}"


def calculate_payg_summary(income_data: dict) -> dict:
    """
    Calculate PAYG income totals from employer records.
    Returns summary dict matching ATO Individual Income Tax Return fields.
    """
    total_gross = 0.0
    total_tax_withheld = 0.0
    total_super = 0.0

    employers = income_data.get("employers", [])
    for emp in employers:
        try:
            total_gross += float(emp.get("gross_income", 0))
            total_tax_withheld += float(emp.get("tax_withheld", 0))
            total_super += float(emp.get("super_contributions", 0))
        except (ValueError, TypeError) as e:
            print(f"  [Warning] Skipping malformed employer entry: {e}")
            continue

    # ATO label 1: Salary or wages
    # ATO label 12: Total tax withheld
    return {
        "ato_label_1_salary_wages": round(total_gross, 2),
        "ato_label_12_tax_withheld": round(total_tax_withheld, 2),
        "employer_super_contributions": round(total_super, 2),
        "employer_count": len(employers),
    }


def calculate_rental_income(property_data: dict) -> dict:
    """
    Calculate net rental income/loss for ATO Rental Schedule (Form I).
    Categories match ATO rental property worksheet fields.
    Records should be kept for 5 years per ATO requirements.
    """
    # ATO allowable expense categories for rental properties
    ato_expense_categories = {
        "advertising": 0.0,
        "body_corporate_fees": 0.0,
        "borrowing_expenses": 0.0,
        "cleaning": 0.0,
        "council_rates": 0.0,
        "depreciation": 0.0,
        "gardening": 0.0,
        "insurance": 0.0,
        "interest_on_loans": 0.0,
        "land_tax": 0.0,
        "legal_expenses": 0.0,
        "pest_control": 0.0,
        "property_agent_fees": 0.0,
        "repairs_and_maintenance": 0.0,
        "stationery_phone_postage": 0.0,
        "travel": 0.0,
        "water_charges": 0.0,
        "other": 0.0,
    }

    total_gross_rent = 0.0
    properties = property_data.get("properties", [])
    all_expenses = dict(ato_expense_categories)

    for prop in properties:
        try:
            total_gross_rent += float(prop.get("gross_rent_received", 0))
            expenses = prop.get("expenses", {})
            for category in all_expenses:
                all_expenses[category] += float(expenses.get(category, 0))
        except (ValueError, TypeError) as e:
            print(f"  [Warning] Skipping malformed property entry: {e}")
            continue

    total_expenses = sum(all_expenses.values())
    net_rental = total_gross_rent - total_expenses

    result = {
        "ato_item_20_gross_rent": round(total_gross_rent, 2),
        "total_allowable_expenses": round(total_expenses, 2),
        "ato_net_rental_income_loss": round(net_rental, 2),
        "expense_breakdown": {k: round(v, 2) for k, v in all_expenses.items() if v > 0},
        "property_count": len(properties),
    }
    return result


def calculate_deductions(deductions_data: dict) -> dict:
    """
    Total work-related deductions matching ATO IITR deduction labels.
    ATO myDeductions categories replicated here for compatibility.
    """
    # ATO deduction labels (D1-D15)
    ato_deduction_labels = {
        "D1_work_related_car": 0.0,
        "D2_work_related_travel": 0.0,
        "D3_clothing_laundry_dry_cleaning": 0.0,
        "D4_self_education": 0.0,
        "D5_other_work_related": 0.0,
        "D6_low_value_pool": 0.0,
        "D7_interest_dividends": 0.0,
        "D8_gifts_donations": 0.0,
        "D9_cost_of_managing_tax_affairs": 0.0,
        "D10_decline_in_value_depreciating_assets": 0.0,
        "D11_project_pool": 0.0,
        "D12_personal_super_contributions": 0.0,
        "D15_other_deductions": 0.0,
    }

    entries = deductions_data.get("entries", [])
    skipped = 0

    for entry in entries:
        try:
            label = entry.get("ato_label", "D15_other_deductions")
            amount = float(entry.get("amount", 0))
            if label in ato_deduction_labels:
                ato_deduction_labels[label] += amount
            else:
                ato_deduction_labels["D15_other_deductions"] += amount
        except (ValueError, TypeError):
            skipped += 1
            continue

    if skipped:
        print(f"  [Warning] Skipped {skipped} malformed deduction entries.")

    total = sum(ato_deduction_labels.values())
    active = {k: round(v, 2) for k, v in ato_deduction_labels.items() if v > 0}

    return {
        "total_deductions": round(total, 2),
        "by_ato_label": active,
        "entry_count": len(entries),
    }


def generate_tax_summary(fy: str) -> dict:
    """
    Load all data files and generate a consolidated ATO tax return summary.
    This is the main assembly function.
    """
    print(f"\n  Loading records for FY {fy}...")

    income_data = load_json(f"income_{fy}.json")
    property_data = load_json(f"property_{fy}.json")
    deductions_data = load_json(f"deductions_{fy}.json")

    payg = calculate_payg_summary(income_data)
    rental = calculate_rental_income(property_data)
    deductions = calculate_deductions(deductions_data)

    # Estimate taxable income (simplified — does not account for all offsets)
    gross_income = payg["ato_label_1_salary_wages"]
    net_rental = rental["ato_net_rental_income_loss"]
    total_deductions = deductions["total_deductions"]
    estimated_taxable = gross_income + net_rental - total_deductions

    summary = {
        "financial_year": fy,
        "generated_at": datetime.now().isoformat(),
        "disclaimer": "This tool does not provide tax advice. It helps organise records for tax return preparation.",
        "ato_keep_records_years": 5,
        "payg_summary": payg,
        "rental_schedule": rental,
        "deductions_summary": deductions,
        "estimated_taxable_income": round(estimated_taxable, 2),
        "tax_withheld_fy": payg["ato_label_12_tax_withheld"],
    }

    return summary


# ─── CLI interface ────────────────────────────────────────────────────────────

def menu_add_income(fy: str) -> None:
    """Interactive prompt to add PAYG income from an employer."""
    income_data = load_json(f"income_{fy}.json")
    if "employers" not in income_data:
        income_data["employers"] = []

    print("\n  Add PAYG Income (from your Payment Summary / Income Statement)")
    try:
        employer_name = input("  Employer name: ").strip()
        gross = float(input("  Gross income ($): "))
        tax = float(input("  Tax withheld ($): "))
        super_amt = float(input("  Super contributions ($, or 0): "))
    except ValueError:
        print("  [Error] Invalid amount entered. Please use numbers only.")
        return

    income_data["employers"].append({
        "employer": employer_name,
        "gross_income": gross,
        "tax_withheld": tax,
        "super_contributions": super_amt,
        "added_at": datetime.now().isoformat(),
    })
    save_json(f"income_{fy}.json", income_data)


def menu_add_rental(fy: str) -> None:
    """Interactive prompt to add a rental property income/expense record."""
    prop_data = load_json(f"property_{fy}.json")
    if "properties" not in prop_data:
        prop_data["properties"] = []

    print("\n  Add Rental Property (ATO Rental Schedule fields)")
    print("  Note: ATO requires rental records to be kept for 5 years.")
    try:
        address = input("  Property address: ").strip()
        gross_rent = float(input("  Total gross rent received ($): "))
        interest = float(input("  Loan interest ($): "))
        agent_fees = float(input("  Property agent fees ($): "))
        rates = float(input("  Council rates ($): "))
        insurance = float(input("  Insurance ($): "))
        repairs = float(input("  Repairs & maintenance ($): "))
        depreciation = float(input("  Depreciation ($, or 0): "))
        other = float(input("  Other allowable expenses ($, or 0): "))
    except ValueError:
        print("  [Error] Invalid amount. Please use numbers only.")
        return

    prop_data["properties"].append({
        "address": address,
        "gross_rent_received": gross_rent,
        "expenses": {
            "interest_on_loans": interest,
            "property_agent_fees": agent_fees,
            "council_rates": rates,
            "insurance": insurance,
            "repairs_and_maintenance": repairs,
            "depreciation": depreciation,
            "other": other,
        },
        "added_at": datetime.now().isoformat(),
    })
    save_json(f"property_{fy}.json", prop_data)


def menu_add_deduction(fy: str) -> None:
    """Interactive prompt to add a work-related deduction."""
    deductions_data = load_json(f"deductions_{fy}.json")
    if "entries" not in deductions_data:
        deductions_data["entries"] = []

    ato_labels = {
        "1": "D1_work_related_car",
        "2": "D2_work_related_travel",
        "3": "D3_clothing_laundry_dry_cleaning",
        "4": "D4_self_education",
        "5": "D5_other_work_related",
        "8": "D8_gifts_donations",
        "9": "D9_cost_of_managing_tax_affairs",
        "12": "D12_personal_super_contributions",
        "15": "D15_other_deductions",
    }

    print("\n  Add Deduction")
    print("  ATO Labels: 1=Car 2=Travel 3=Clothing 4=Education 5=Other Work")
    print("              8=Donations 9=Tax Affairs 12=Super 15=Other")

    try:
        label_key = input("  ATO label number: ").strip()
        ato_label = ato_labels.get(label_key, "D15_other_deductions")
        description = input("  Description: ").strip()
        amount = float(input("  Amount ($): "))
        receipt = input("  Receipt/reference number (optional): ").strip()
    except ValueError:
        print("  [Error] Invalid amount. Please use numbers only.")
        return

    deductions_data["entries"].append({
        "ato_label": ato_label,
        "description": description,
        "amount": amount,
        "receipt_ref": receipt,
        "added_at": datetime.now().isoformat(),
    })
    save_json(f"deductions_{fy}.json", deductions_data)


def menu_view_summary(fy: str) -> None:
    """Display and export a full tax summary for the given FY."""
    summary = generate_tax_summary(fy)

    print(f"\n  ══════════════════════════════════════════════")
    print(f"  ATO Tax Return Summary — FY {fy}")
    print(f"  ══════════════════════════════════════════════")
    print(f"  PAYG Salary/Wages (Label 1):    ${summary['payg_summary']['ato_label_1_salary_wages']:>12,.2f}")
    print(f"  Tax Withheld (Label 12):         ${summary['payg_summary']['ato_label_12_tax_withheld']:>12,.2f}")
    print(f"  Net Rental Income/Loss:          ${summary['rental_schedule']['ato_net_rental_income_loss']:>12,.2f}")
    print(f"  Total Deductions:                ${summary['deductions_summary']['total_deductions']:>12,.2f}")
    print(f"  ──────────────────────────────────────────────")
    print(f"  Est. Taxable Income:             ${summary['estimated_taxable_income']:>12,.2f}")
    print(f"  ══════════════════════════════════════════════")
    print(f"\n  ⚠  {summary['disclaimer']}")
    print(f"  ℹ  ATO requires records to be kept for {summary['ato_keep_records_years']} years.")

    # Save full summary JSON + flat CSV
    save_json(f"summary_{fy}.json", summary)

    flat = {
        "financial_year": fy,
        "salary_wages": summary["payg_summary"]["ato_label_1_salary_wages"],
        "tax_withheld": summary["payg_summary"]["ato_label_12_tax_withheld"],
        "gross_rent": summary["rental_schedule"]["ato_item_20_gross_rent"],
        "rental_expenses": summary["rental_schedule"]["total_allowable_expenses"],
        "net_rental": summary["rental_schedule"]["ato_net_rental_income_loss"],
        "total_deductions": summary["deductions_summary"]["total_deductions"],
        "estimated_taxable_income": summary["estimated_taxable_income"],
        "generated_at": summary["generated_at"],
    }
    export_summary_csv(flat, f"summary_{fy}.csv")


def main():
    """Main CLI loop."""
    fy = get_financial_year()
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(RECORDS_DIR, exist_ok=True)

    print("\n  ╔══════════════════════════════════════════════╗")
    print("  ║  AUS Tax & Finance Prep Tool                ║")
    print("  ║  For PAYG + Investment Property             ║")
    print("  ╚══════════════════════════════════════════════╝")
    print(f"\n  Current financial year: {fy}")
    print("  This tool does not provide tax advice.")
    print("  It helps organise records for tax return preparation.\n")

    options = {
        "1": ("Add PAYG income", menu_add_income),
        "2": ("Add rental property income/expenses", menu_add_rental),
        "3": ("Add deduction", menu_add_deduction),
        "4": ("View & export tax summary", menu_view_summary),
        "5": ("Exit", None),
    }

    while True:
        print("\n  ── Menu ──────────────────────────────────────")
        for key, (label, _) in options.items():
            print(f"  {key}. {label}")

        choice = input("\n  Select option: ").strip()

        if choice == "5":
            print("\n  Records saved. Remember to keep them for 5 years (ATO requirement).\n")
            break
        elif choice in options:
            _, fn = options[choice]
            if fn:
                fn(fy)
        else:
            print("  [Error] Invalid option. Please enter 1–5.")


if __name__ == "__main__":
    main()

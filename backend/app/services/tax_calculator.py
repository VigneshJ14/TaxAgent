from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum

class FilingStatus(Enum):
    SINGLE = "single"
    MARRIED = "married"
    HEAD_OF_HOUSEHOLD = "head_of_household"

@dataclass
class TaxBracket:
    rate: float
    min_income: float
    max_income: float

@dataclass
class TaxCalculationResult:
    filing_status: FilingStatus
    total_income: float
    adjusted_gross_income: float
    standard_deduction: float
    taxable_income: float
    tax_liability: float
    total_payments: float
    refund_or_amount_owed: float
    breakdown: Dict[str, Any]

class TaxCalculator:
    def __init__(self):
        # 2024 Tax Brackets (Single)
        self.single_brackets = [
            TaxBracket(0.10, 0, 11600),
            TaxBracket(0.12, 11600, 47150),
            TaxBracket(0.22, 47150, 100525),
            TaxBracket(0.24, 100525, 191950),
            TaxBracket(0.32, 191950, 243725),
            TaxBracket(0.35, 243725, 609350),
            TaxBracket(0.37, 609350, float('inf'))
        ]
        
        # 2024 Tax Brackets (Married Filing Jointly)
        self.married_brackets = [
            TaxBracket(0.10, 0, 23200),
            TaxBracket(0.12, 23200, 94300),
            TaxBracket(0.22, 94300, 201050),
            TaxBracket(0.24, 201050, 383900),
            TaxBracket(0.32, 383900, 487450),
            TaxBracket(0.35, 487450, 731200),
            TaxBracket(0.37, 731200, float('inf'))
        ]
        
        # 2024 Tax Brackets (Head of Household)
        self.hoh_brackets = [
            TaxBracket(0.10, 0, 16550),
            TaxBracket(0.12, 16550, 63100),
            TaxBracket(0.22, 63100, 100500),
            TaxBracket(0.24, 100500, 191950),
            TaxBracket(0.32, 191950, 243700),
            TaxBracket(0.35, 243700, 609350),
            TaxBracket(0.37, 609350, float('inf'))
        ]
        
        # 2024 Standard Deductions
        self.standard_deductions = {
            FilingStatus.SINGLE: 14600,
            FilingStatus.MARRIED: 29200,
            FilingStatus.HEAD_OF_HOUSEHOLD: 21900
        }

    def get_brackets_for_status(self, filing_status: FilingStatus) -> List[TaxBracket]:
        """Get tax brackets for the given filing status"""
        if filing_status == FilingStatus.SINGLE:
            return self.single_brackets
        elif filing_status == FilingStatus.MARRIED:
            return self.married_brackets
        elif filing_status == FilingStatus.HEAD_OF_HOUSEHOLD:
            return self.hoh_brackets
        else:
            return self.single_brackets

    def calculate_tax_for_bracket(self, income: float, bracket: TaxBracket) -> float:
        """Calculate tax for a specific bracket"""
        if income <= bracket.min_income:
            return 0
        
        taxable_in_bracket = min(income - bracket.min_income, bracket.max_income - bracket.min_income)
        return taxable_in_bracket * bracket.rate

    def calculate_marginal_tax(self, taxable_income: float, filing_status: FilingStatus) -> float:
        """Calculate marginal tax using progressive tax brackets"""
        brackets = self.get_brackets_for_status(filing_status)
        total_tax = 0
        
        for bracket in brackets:
            if taxable_income > bracket.min_income:
                tax_for_bracket = self.calculate_tax_for_bracket(taxable_income, bracket)
                total_tax += tax_for_bracket
        
        return total_tax

    def calculate_standard_deduction(self, filing_status: FilingStatus, age: int = 0) -> float:
        """Calculate standard deduction (with age-based adjustments)"""
        base_deduction = self.standard_deductions[filing_status]
        
        # Additional deduction for age 65+ (simplified)
        if age >= 65:
            if filing_status == FilingStatus.SINGLE:
                base_deduction += 1850
            elif filing_status == FilingStatus.MARRIED:
                base_deduction += 1500
            elif filing_status == FilingStatus.HEAD_OF_HOUSEHOLD:
                base_deduction += 1850
        
        return base_deduction

    def calculate_tax(self, 
                     filing_status: str,
                     wages: float = 0,
                     interest_income: float = 0,
                     nonemployee_compensation: float = 0,
                     federal_income_tax_withheld: float = 0,
                     dependents: int = 0,
                     age: int = 0) -> TaxCalculationResult:
        """Main method to calculate tax liability"""
        
        # Convert string to enum
        status_enum = FilingStatus(filing_status.lower())
        
        # Calculate total income
        total_income = wages + interest_income + nonemployee_compensation
        
        # Adjusted Gross Income (AGI) - simplified for this prototype
        agi = total_income
        
        # Calculate standard deduction
        standard_deduction = self.calculate_standard_deduction(status_enum, age)
        
        # Calculate taxable income
        taxable_income = max(0, agi - standard_deduction)
        
        # Calculate tax liability
        tax_liability = self.calculate_marginal_tax(taxable_income, status_enum)
        
        # Calculate total payments (federal tax withheld)
        total_payments = federal_income_tax_withheld
        
        # Calculate refund or amount owed
        refund_or_amount_owed = total_payments - tax_liability
        
        # Create detailed breakdown
        breakdown = {
            'income_breakdown': {
                'wages': wages,
                'interest_income': interest_income,
                'nonemployee_compensation': nonemployee_compensation,
                'total_income': total_income
            },
            'deductions': {
                'standard_deduction': standard_deduction,
                'agi': agi,
                'taxable_income': taxable_income
            },
            'tax_calculation': {
                'tax_liability': tax_liability,
                'total_payments': total_payments,
                'refund_or_amount_owed': refund_or_amount_owed
            },
            'bracket_breakdown': self.get_bracket_breakdown(taxable_income, status_enum)
        }
        
        return TaxCalculationResult(
            filing_status=status_enum,
            total_income=total_income,
            adjusted_gross_income=agi,
            standard_deduction=standard_deduction,
            taxable_income=taxable_income,
            tax_liability=tax_liability,
            total_payments=total_payments,
            refund_or_amount_owed=refund_or_amount_owed,
            breakdown=breakdown
        )

    def get_bracket_breakdown(self, taxable_income: float, filing_status: FilingStatus) -> Dict[str, Any]:
        """Get detailed breakdown of tax by bracket"""
        brackets = self.get_brackets_for_status(filing_status)
        breakdown = []
        
        for bracket in brackets:
            if taxable_income > bracket.min_income:
                tax_for_bracket = self.calculate_tax_for_bracket(taxable_income, bracket)
                breakdown.append({
                    'bracket': f"{bracket.rate * 100}%",
                    'income_range': f"${bracket.min_income:,.0f} - ${bracket.max_income:,.0f}" if bracket.max_income != float('inf') else f"${bracket.min_income:,.0f}+",
                    'taxable_in_bracket': min(taxable_income - bracket.min_income, bracket.max_income - bracket.min_income),
                    'tax_for_bracket': tax_for_bracket
                })
        
        return breakdown

    def validate_inputs(self, **kwargs) -> Dict[str, Any]:
        """Validate tax calculation inputs"""
        errors = []
        warnings = []
        
        # Check for negative values
        for key, value in kwargs.items():
            if isinstance(value, (int, float)) and value < 0:
                errors.append(f"{key} cannot be negative")
        
        # Check filing status
        valid_statuses = [status.value for status in FilingStatus]
        if 'filing_status' in kwargs and kwargs['filing_status'] not in valid_statuses:
            errors.append(f"Invalid filing status. Must be one of: {valid_statuses}")
        
        # Check dependents
        if 'dependents' in kwargs and kwargs['dependents'] < 0:
            errors.append("Number of dependents cannot be negative")
        
        # Check age
        if 'age' in kwargs and (kwargs['age'] < 0 or kwargs['age'] > 120):
            warnings.append("Age seems unusual, please verify")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        } 
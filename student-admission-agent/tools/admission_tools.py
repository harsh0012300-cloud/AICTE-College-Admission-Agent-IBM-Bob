"""
Student Admission Tools
Provides tools for answering queries about admission requirements,
application deadlines, tuition fees, and general admission information.
"""

from typing import Optional
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission


# ---------------------------------------------------------------------------
# Pydantic Schemas
# ---------------------------------------------------------------------------

class AdmissionRequirementsInput(BaseModel):
    """Input for retrieving admission requirements."""
    program: str = Field(
        ...,
        description=(
            "The name of the academic program the student is inquiring about, "
            "e.g. 'Computer Science', 'Business Administration', 'Nursing'."
        ),
    )
    level: Optional[str] = Field(
        default="undergraduate",
        description="Academic level: 'undergraduate', 'graduate', or 'doctoral'.",
    )


class AdmissionRequirementsOutput(BaseModel):
    """Admission requirements for a given program."""
    program: str = Field(description="Name of the academic program")
    level: str = Field(description="Academic level")
    minimum_gpa: str = Field(description="Minimum GPA requirement")
    standardized_tests: str = Field(description="Required standardized tests and minimum scores")
    required_documents: str = Field(description="List of required application documents")
    additional_requirements: str = Field(description="Any additional program-specific requirements")
    contact: str = Field(description="Admissions contact for this program")


class DeadlineInput(BaseModel):
    """Input for retrieving application deadlines."""
    program: Optional[str] = Field(
        default=None,
        description="Specific program name, or leave blank for general deadlines.",
    )
    term: Optional[str] = Field(
        default="fall",
        description="Target enrollment term: 'fall', 'spring', or 'summer'.",
    )


class DeadlineOutput(BaseModel):
    """Application deadline information."""
    term: str = Field(description="Enrollment term")
    early_action_deadline: str = Field(description="Early action application deadline")
    regular_decision_deadline: str = Field(description="Regular decision application deadline")
    financial_aid_deadline: str = Field(description="Financial aid application deadline")
    scholarship_deadline: str = Field(description="Merit scholarship application deadline")
    notification_date: str = Field(description="Date when admission decisions are sent")
    enrollment_deposit_deadline: str = Field(description="Deadline to submit enrollment deposit")
    notes: str = Field(description="Additional notes about deadlines")


class TuitionFeesInput(BaseModel):
    """Input for retrieving tuition and fee information."""
    program: Optional[str] = Field(
        default=None,
        description="Specific program name, or leave blank for general tuition info.",
    )
    residency: Optional[str] = Field(
        default="domestic",
        description="Student residency status: 'domestic' or 'international'.",
    )
    level: Optional[str] = Field(
        default="undergraduate",
        description="Academic level: 'undergraduate', 'graduate', or 'doctoral'.",
    )


class TuitionFeesOutput(BaseModel):
    """Tuition and fees information."""
    academic_year: str = Field(description="Academic year this information applies to")
    tuition_per_credit: str = Field(description="Tuition cost per credit hour")
    full_time_tuition: str = Field(description="Full-time tuition per semester")
    mandatory_fees: str = Field(description="Mandatory fees per semester")
    estimated_books_supplies: str = Field(description="Estimated books and supplies cost per year")
    estimated_room_board: str = Field(description="Estimated room and board per year")
    estimated_total_cost: str = Field(description="Estimated total annual cost of attendance")
    financial_aid_info: str = Field(description="Summary of financial aid and scholarship options")
    payment_plans: str = Field(description="Available payment plan options")


# ---------------------------------------------------------------------------
# Tool Implementations
# ---------------------------------------------------------------------------

@tool(permission=ToolPermission.READ_ONLY)
def get_admission_requirements(input: AdmissionRequirementsInput) -> AdmissionRequirementsOutput:
    """
    Retrieve admission requirements for a specific academic program and level.

    Returns the minimum GPA, required standardized tests, required documents,
    and any additional program-specific requirements for the requested program.

    Args:
        input (AdmissionRequirementsInput): Contains the program name and academic level.

    Returns:
        AdmissionRequirementsOutput: Detailed admission requirements for the program.
    """
    level = (input.level or "undergraduate").lower()
    program = input.program.strip()

    # Graduate-level defaults
    if level == "graduate":
        return AdmissionRequirementsOutput(
            program=program,
            level="Graduate",
            minimum_gpa="3.0 (on a 4.0 scale) in relevant undergraduate coursework",
            standardized_tests=(
                "GRE General Test (minimum 300 combined Verbal + Quantitative); "
                "GMAT accepted for MBA programs (minimum 550). "
                "International students: TOEFL ≥ 90 iBT or IELTS ≥ 7.0."
            ),
            required_documents=(
                "1. Completed online application form\n"
                "2. Official undergraduate transcripts from all institutions attended\n"
                "3. Statement of purpose (500–1,000 words)\n"
                "4. Three letters of recommendation (academic or professional)\n"
                "5. Current résumé or curriculum vitae\n"
                "6. Application fee ($75)"
            ),
            additional_requirements=(
                f"Some {program} graduate tracks may require a writing sample, "
                "portfolio, or interview. Check the program-specific page for details."
            ),
            contact="grad.admissions@university.edu | +1-800-555-0200",
        )

    # Doctoral-level defaults
    if level == "doctoral":
        return AdmissionRequirementsOutput(
            program=program,
            level="Doctoral (Ph.D.)",
            minimum_gpa="3.5 (on a 4.0 scale) in relevant graduate coursework",
            standardized_tests=(
                "GRE General Test (minimum 310 combined). "
                "International students: TOEFL ≥ 100 iBT or IELTS ≥ 7.5."
            ),
            required_documents=(
                "1. Completed online application form\n"
                "2. Official transcripts (undergraduate and graduate)\n"
                "3. Statement of research interests (1,000–1,500 words)\n"
                "4. Three letters of recommendation (academic preferred)\n"
                "5. Writing sample or published work\n"
                "6. Current CV/résumé\n"
                "7. Application fee ($75)"
            ),
            additional_requirements=(
                "Doctoral applicants must identify a potential faculty advisor in their "
                "statement of research interests. Admission is contingent on faculty availability."
            ),
            contact="doctoral.admissions@university.edu | +1-800-555-0201",
        )

    # Undergraduate defaults
    return AdmissionRequirementsOutput(
        program=program,
        level="Undergraduate",
        minimum_gpa="2.5 cumulative GPA (3.0+ recommended for competitive programs)",
        standardized_tests=(
            "SAT ≥ 1100 or ACT ≥ 22 (test-optional policy applies for 2024–2025). "
            "International students: TOEFL ≥ 80 iBT or IELTS ≥ 6.5."
        ),
        required_documents=(
            "1. Completed online application form\n"
            "2. Official high school transcript\n"
            "3. Personal statement / essay (250–650 words)\n"
            "4. Two letters of recommendation (teacher or counselor)\n"
            "5. Application fee ($50; fee waivers available)\n"
            "6. SAT/ACT scores (optional but recommended)"
        ),
        additional_requirements=(
            f"The {program} program may require an audition, portfolio, or prerequisite "
            "coursework. Please review the program page or contact the admissions office."
        ),
        contact="admissions@university.edu | +1-800-555-0199",
    )


@tool(permission=ToolPermission.READ_ONLY)
def get_application_deadlines(input: DeadlineInput) -> DeadlineOutput:
    """
    Retrieve application deadlines for a given enrollment term.

    Returns key dates including early action, regular decision, financial aid,
    scholarship deadlines, notification dates, and enrollment deposit deadlines.

    Args:
        input (DeadlineInput): Contains the target term and optional program name.

    Returns:
        DeadlineOutput: All relevant application deadlines for the requested term.
    """
    term = (input.term or "fall").lower()

    deadlines = {
        "fall": DeadlineOutput(
            term="Fall Semester (August entry)",
            early_action_deadline="November 1",
            regular_decision_deadline="January 15",
            financial_aid_deadline="February 1",
            scholarship_deadline="December 1",
            notification_date="March 15 (Early Action) / April 1 (Regular Decision)",
            enrollment_deposit_deadline="May 1",
            notes=(
                "Fall is our largest intake. Most programs are available. "
                "International applicants are strongly encouraged to apply by November 1 "
                "to allow sufficient time for visa processing."
            ),
        ),
        "spring": DeadlineOutput(
            term="Spring Semester (January entry)",
            early_action_deadline="N/A – Spring does not have an early action round",
            regular_decision_deadline="October 1",
            financial_aid_deadline="October 15",
            scholarship_deadline="October 1",
            notification_date="November 1",
            enrollment_deposit_deadline="November 15",
            notes=(
                "Spring intake has limited program availability. "
                "Some graduate programs do not accept spring admissions. "
                "Please confirm with your specific department."
            ),
        ),
        "summer": DeadlineOutput(
            term="Summer Sessions (May/June entry)",
            early_action_deadline="N/A",
            regular_decision_deadline="March 1",
            financial_aid_deadline="March 1",
            scholarship_deadline="March 1",
            notification_date="April 1",
            enrollment_deposit_deadline="April 15",
            notes=(
                "Summer intake is primarily for continuing students and selected graduate programs. "
                "New undergraduate students typically begin in Fall or Spring."
            ),
        ),
    }

    return deadlines.get(
        term,
        DeadlineOutput(
            term=term,
            early_action_deadline="Please contact the admissions office",
            regular_decision_deadline="Please contact the admissions office",
            financial_aid_deadline="Please contact the admissions office",
            scholarship_deadline="Please contact the admissions office",
            notification_date="Please contact the admissions office",
            enrollment_deposit_deadline="Please contact the admissions office",
            notes=f"Deadline information for '{term}' is not available. Contact admissions@university.edu.",
        ),
    )


@tool(permission=ToolPermission.READ_ONLY)
def get_tuition_and_fees(input: TuitionFeesInput) -> TuitionFeesOutput:
    """
    Retrieve tuition and fee information for a given program, residency status, and level.

    Returns per-credit and full-time tuition, mandatory fees, estimated living costs,
    total cost of attendance, financial aid options, and payment plan information.

    Args:
        input (TuitionFeesInput): Contains program name, residency status, and academic level.

    Returns:
        TuitionFeesOutput: Comprehensive tuition and cost-of-attendance breakdown.
    """
    residency = (input.residency or "domestic").lower()
    level = (input.level or "undergraduate").lower()
    is_international = residency == "international"

    if level == "graduate":
        tuition_per_credit = "$850/credit hr" if not is_international else "$1,050/credit hr"
        full_time_tuition = "$10,200/semester (12 cr)" if not is_international else "$12,600/semester"
        total_cost = "$28,000–$32,000/year" if not is_international else "$36,000–$42,000/year"
    elif level == "doctoral":
        tuition_per_credit = "$950/credit hr" if not is_international else "$1,150/credit hr"
        full_time_tuition = "$11,400/semester (12 cr)" if not is_international else "$13,800/semester"
        total_cost = "$30,000–$35,000/year" if not is_international else "$40,000–$46,000/year"
    else:  # undergraduate
        tuition_per_credit = "$620/credit hr" if not is_international else "$820/credit hr"
        full_time_tuition = "$9,300/semester (15 cr)" if not is_international else "$12,300/semester"
        total_cost = "$26,000–$30,000/year" if not is_international else "$34,000–$40,000/year"

    return TuitionFeesOutput(
        academic_year="2024–2025",
        tuition_per_credit=tuition_per_credit,
        full_time_tuition=full_time_tuition,
        mandatory_fees=(
            "$450/semester (covers student services, technology fee, health services, "
            "and recreation center access)"
        ),
        estimated_books_supplies="$1,200–$1,800/year",
        estimated_room_board=(
            "$10,500–$14,000/year (on-campus housing); "
            "$9,000–$12,000/year (off-campus estimate)"
        ),
        estimated_total_cost=total_cost,
        financial_aid_info=(
            "Over 85% of our students receive some form of financial assistance. "
            "Available aid includes: Federal Pell Grants, institutional merit scholarships "
            "(ranging $2,000–$20,000/year), need-based grants, Federal Direct Loans (subsidized "
            "and unsubsidized), Federal Work-Study, and Graduate Assistantships (for graduate students). "
            "File the FAFSA by February 1 to maximize aid eligibility. "
            "International students are eligible for merit scholarships and institutional grants."
        ),
        payment_plans=(
            "Monthly installment plan: split semester balance into 4 equal payments (no interest). "
            "Employer tuition reimbursement deferral plan available. "
            "529 College Savings Plans accepted. Contact bursar@university.edu for details."
        ),
    )

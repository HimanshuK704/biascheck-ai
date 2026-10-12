import re

# A small, explainable starter ruleset. Matches are prompts for review, not conclusions.
RULES = [
    {
        "pattern": r"\byoung and dynamic\b",
        "issue": "Age-coded wording",
        "category": "Age-related assumptions",
        "suggestion": "adaptable, motivated, and comfortable working in a changing environment (if accurate)",
        "reason": "The phrase may suggest an age preference rather than describing job-related skills.",
        "review_level": "Review",
    },
    {
        "pattern": r"\bstrong young man\b",
        "issue": "Gender and age assumption",
        "category": "Gendered language",
        "suggestion": "describe the essential tasks and required capabilities",
        "reason": "The phrase specifies gender and age instead of focusing on job-related requirements.",
        "review_level": "Review",
    },
    {
        "pattern": r"\brecent graduates? only\b",
        "issue": "Potential age proxy",
        "category": "Age-related assumptions",
        "suggestion": "state the actual experience or qualification requirements",
        "reason": "An 'only' restriction may unnecessarily narrow the candidate pool if graduation date is not essential.",
        "review_level": "Review",
    },
    {
        "pattern": r"\bnative english speaker\b",
        "issue": "Potentially unnecessary language criterion",
        "category": "Language requirements",
        "suggestion": "specify the required English proficiency and the job tasks that need it",
        "reason": "Native-speaker status may not be necessary when the actual requirement is a particular level of language proficiency.",
        "review_level": "Review",
    },
    {
        "pattern": r"\bable-bodied\b",
        "issue": "Potentially exclusionary wording",
        "category": "Accessibility",
        "suggestion": "describe the essential functions of the role and any specific requirements",
        "reason": "A broad label may exclude people unnecessarily; focus on essential job functions and reasonable accommodations.",
        "review_level": "Review",
    },
    {
        "pattern": r"\bdigital natives?\b",
        "issue": "Age-coded wording",
        "category": "Age-related assumptions",
        "suggestion": "proficient with the specific digital tools required",
        "reason": "The term can make assumptions about technical ability based on age or generation.",
        "review_level": "Review",
    },
    {
        "pattern": r"\bphysically fit\b",
        "issue": "Vague physical requirement",
        "category": "Physical requirements",
        "suggestion": "describe the specific essential task or capability, if genuinely required",
        "reason": "This phrase is broad. Specific job-related duties are clearer and help avoid unnecessary exclusion.",
        "review_level": "Review",
    },
    {
        "pattern": r"\bsalesman\b",
        "issue": "Gendered job title",
        "category": "Gendered language",
        "suggestion": "sales representative",
        "reason": "A gender-neutral job title can communicate that the role is open to candidates of all genders.",
        "review_level": "Review",
    },
    {
        "pattern": r"\bchairman\b",
        "issue": "Gendered job title",
        "category": "Gendered language",
        "suggestion": "chairperson or chair",
        "reason": "A neutral title avoids implying that the role belongs to a particular gender.",
        "review_level": "Review",
    },
    {
        "pattern": r"\bmanpower\b",
        "issue": "Gendered wording",
        "category": "Gendered language",
        "suggestion": "staffing, workforce, or personnel",
        "reason": "A gender-neutral term is often clearer and more inclusive.",
        "review_level": "Review",
    },
    {
        "pattern": r"\bhe should\b",
        "issue": "Gendered assumption",
        "category": "Gendered language",
        "suggestion": "the candidate should / they should",
        "reason": "Generic use of 'he' can imply that the role-holder is expected to be male.",
        "review_level": "Review",
    },
    {
        "pattern": r"\bshe should\b",
        "issue": "Gendered assumption",
        "category": "Gendered language",
        "suggestion": "the candidate should / they should",
        "reason": "A generic gendered pronoun can imply that the role-holder is expected to be a particular gender.",
        "review_level": "Review",
    },
    {
        "pattern": r"\bculture fit\b",
        "issue": "Vague cultural expectation",
        "category": "Workplace culture",
        "suggestion": "describe the specific collaboration, communication, or work practices needed",
        "reason": "The phrase can be interpreted subjectively and may encourage similarity-based hiring rather than job-related evaluation.",
        "review_level": "Review",
    },
    {
        "pattern": r"\baggressive\b",
        "issue": "Ambiguous behavioral wording",
        "category": "Workplace culture",
        "suggestion": "results-oriented, proactive, or assertive, if that reflects the intended behavior",
        "reason": "The word can mean different things in different contexts. A specific behavior or outcome is easier to evaluate fairly.",
        "review_level": "Consider",
    },
    {
        "pattern": r"\brockstar\b",
        "issue": "Potentially exclusionary idiom",
        "category": "Vague workplace language",
        "suggestion": "high-performing, experienced, or collaborative, depending on the intended meaning",
        "reason": "Informal labels can be vague; stating the actual skills or outcomes makes expectations more transparent.",
        "review_level": "Consider",
    },
    {
        "pattern": r"\bninja\b",
        "issue": "Vague role description",
        "category": "Vague workplace language",
        "suggestion": "name the relevant skill, such as Python developer or data analyst",
        "reason": "Metaphorical job labels can obscure the actual responsibilities and skills required.",
        "review_level": "Consider",
    },
    {
        "pattern": r"\bwork hard play hard\b",
        "issue": "Unclear workplace expectation",
        "category": "Workplace culture",
        "suggestion": "describe expected working hours, team activities, and work-life expectations clearly",
        "reason": "The phrase is vague and may hide expectations around overtime or after-hours socializing.",
        "review_level": "Consider",
    },
    {
        "pattern": r"\byoung\b",
        "issue": "Age-related wording",
        "category": "Age-related assumptions",
        "suggestion": "describe the relevant skill, experience level, or working requirement",
        "reason": "Describing applicants as 'young' may imply an age preference unrelated to essential job duties.",
        "review_level": "Review",
    },
]

def analyze_text(text: str):
    candidates = []
    for rule in RULES:
        for match in re.finditer(rule["pattern"], text, flags=re.IGNORECASE):
            candidates.append({
                "start": match.start(),
                "end": match.end(),
                "phrase": match.group(0),
                "issue": rule["issue"],
                "category": rule["category"],
                "suggestion": rule["suggestion"],
                "reason": rule["reason"],
                "review_level": rule["review_level"],
            })

    # Prefer the longest match when multiple rules overlap, e.g. "young and dynamic"
    candidates.sort(key=lambda item: (item["start"], -(item["end"] - item["start"])))
    selected = []
    for candidate in candidates:
        if any(candidate["start"] < existing["end"] and candidate["end"] > existing["start"] for existing in selected):
            continue
        selected.append(candidate)

    selected.sort(key=lambda item: item["start"])
    return selected

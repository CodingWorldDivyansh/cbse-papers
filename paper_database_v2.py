"""
CBSE Previous Year Papers Database (2015-2025)
Comprehensive database with multiple mirror sources
Subjects: Mathematics, Accountancy, Economics, Business Studies, English Core, Data Science
Includes: Question Papers, Marking Schemes, Sample Papers, Compartment Papers
All Sets and Regions covered
"""

# Mirror base URLs
MIRRORS = {
    "supercop": "https://files.supercop.in/cbse-board-papers/class12",
    "selfstudy": "https://www.selfstudys.com/books/cbse-previous-year-paper/class-12th",
    "cbse_academic": "https://cbseacademic.nic.in/web_material/SQP",
    "cbse_pyp": "https://cbse.gov.in/cbsenew/documents",
    "mycbseguide": "https://mycbseguide.com/exams/cbse/class-12",
}

# Subject configuration with codes and mirror patterns
# Verified working patterns for supercop.in
SUBJECT_CONFIG = {
    "Mathematics": {
        "code": "65",
        "supercop_folder": "maths",
        "supercop_subfolder": "maths",
        "supercop_qp": "m",
        "supercop_ms": "ans_m",
        "selfstudy_name": "mathematics",
        "cbse_code": "065",
        "alt_codes": ["65(B)"],  # Compartment code
    },
    "Accountancy": {
        "code": "67",
        "supercop_folder": "accoutancy",  # Note: typo in supercop URL
        "supercop_subfolder": "account",
        "supercop_qp": "a",
        "supercop_ms": "ans_a",
        "selfstudy_name": "accountancy",
        "cbse_code": "067",
        "alt_codes": ["67(B)"],
    },
    "Economics": {
        "code": "58",
        "supercop_folder": "economics",
        "supercop_subfolder": "economics",
        "supercop_qp": "eco",
        "supercop_ms": "ans_eco",
        "selfstudy_name": "economics",
        "cbse_code": "058",
        "alt_codes": ["58(B)"],
    },
    "Business Studies": {
        "code": "66",
        "supercop_folder": "bussiness",  # Note: typo in supercop URL
        "supercop_subfolder": "bus_",
        "supercop_qp": "bs",
        "supercop_ms": "ans_bs",
        "selfstudy_name": "business-studies",
        "cbse_code": "066",
        "alt_codes": ["66(B)"],
    },
    "English Core": {
        "code": "301",
        "supercop_folder": "english",
        "supercop_subfolder": "english_core",
        "supercop_qp": "ec",
        "supercop_ms": "ans_ec",
        "selfstudy_name": "english-core",
        "cbse_code": "301",
        "alt_codes": ["301(B)"],
    },
    "Data Science": {
        "code": "844",
        "supercop_folder": "data-science",
        "supercop_subfolder": "ds",
        "supercop_qp": "ds",
        "supercop_ms": "ans_ds",
        "selfstudy_name": "data-science",
        "cbse_code": "844",
        "alt_codes": [],
    },
}

SUBJECTS = list(SUBJECT_CONFIG.keys())
YEARS = [str(y) for y in range(2025, 2014, -1)]  # 2025 to 2015
PAPER_TYPES = ["question_paper", "marking_scheme", "sample_paper", "compartment"]

# Region/Series mapping
REGION_MAP = {
    "1": "Delhi",
    "2": "Outside Delhi", 
    "3": "All India",
    "4": "Foreign Set 1",
    "5": "Foreign Set 2",
    "B": "Compartment",
    "C": "Compartment",
}

# Sets available per series
SETS = ["1", "2", "3"]


def generate_mirror_urls(subject, year, paper_code, is_marking_scheme=False, is_compartment=False, is_sample=False):
    """Generate URLs from multiple mirrors for fallback"""
    config = SUBJECT_CONFIG.get(subject)
    if not config:
        return []
    
    urls = []
    subject_code = config["code"]
    folder = config["supercop_folder"]
    subfolder = config["supercop_subfolder"]
    prefix = config["supercop_ms"] if is_marking_scheme else config["supercop_qp"]
    
    # Primary supercop URL pattern (verified working)
    # Pattern: https://files.supercop.in/cbse-board-papers/class12/{folder}/{subfolder}_{year}/{prefix}_{year}_{code}.pdf
    supercop_url = f"{MIRRORS['supercop']}/{folder}/{subfolder}_{year}/{prefix}_{year}_{paper_code}.pdf"
    urls.append(("supercop", supercop_url))
    
    # Alternative supercop pattern without year in prefix
    alt_url1 = f"{MIRRORS['supercop']}/{folder}/{subfolder}_{year}/{prefix}_{paper_code}.pdf"
    urls.append(("supercop_alt1", alt_url1))
    
    # Alternative with different folder structure
    alt_url2 = f"{MIRRORS['supercop']}/{folder}/{year}/{prefix}_{year}_{paper_code}.pdf"
    urls.append(("supercop_alt2", alt_url2))
    
    # For compartment papers, try B suffix patterns
    if is_compartment:
        comp_code = f"{subject_code}(B)"
        comp_url = f"{MIRRORS['supercop']}/{folder}/{subfolder}_{year}/{prefix}_{year}_{comp_code}.pdf"
        urls.append(("supercop_comp", comp_url))
    
    # CBSE Academic for sample papers
    if is_sample:
        cbse_code = config["cbse_code"]
        # Sample Question Paper
        cbse_sqp = f"{MIRRORS['cbse_academic']}/{year}/{cbse_code}_SQP.pdf"
        urls.append(("cbse_sqp", cbse_sqp))
        # Marking Scheme
        cbse_ms = f"{MIRRORS['cbse_academic']}/{year}/{cbse_code}_MS.pdf"
        urls.append(("cbse_ms", cbse_ms))
        # Alternative CBSE patterns
        cbse_alt = f"{MIRRORS['cbse_academic']}/SQP_{year}/{cbse_code}.pdf"
        urls.append(("cbse_alt", cbse_alt))
    
    # Selfstudy patterns (as backup)
    selfstudy_name = config["selfstudy_name"]
    selfstudy_url = f"{MIRRORS['selfstudy']}/{selfstudy_name}/{year}/{paper_code}.pdf"
    urls.append(("selfstudy", selfstudy_url))
    
    return urls


def generate_paper_list():
    """Generate comprehensive list of all papers with multiple mirror URLs"""
    papers = []
    paper_id = 1
    
    # Paper codes structure by year
    # Format: series -> list of sets
    standard_series = {
        "1": SETS,  # Delhi
        "2": SETS,  # Outside Delhi
        "3": SETS,  # All India
        "4": SETS,  # Foreign Set 1
        "5": SETS,  # Foreign Set 2
    }
    
    compartment_series = {
        "B": [],  # Compartment (no sets)
        "C": [],  # Compartment alternate
    }
    
    for year in YEARS:
        for subject in SUBJECTS:
            config = SUBJECT_CONFIG.get(subject)
            if not config:
                continue
            
            subject_code = config["code"]
            
            # Regular papers (Question Papers and Marking Schemes)
            for series, sets in standard_series.items():
                region = REGION_MAP.get(series, f"Series {series}")
                
                for set_num in sets:
                    paper_code = f"{subject_code}-{series}-{set_num}"
                    
                    # Question Paper
                    papers.append({
                        "id": paper_id,
                        "year": year,
                        "subject": subject,
                        "subject_code": subject_code,
                        "type": "question_paper",
                        "series": series,
                        "set": f"Set {set_num}",
                        "paper_code": paper_code,
                        "region": region,
                        "filename": f"CBSE_{year}_{subject.replace(' ', '_')}_{paper_code}_QP.pdf",
                        "display_name": f"{subject} {year} {region} Set {set_num} - Question Paper",
                        "urls": generate_mirror_urls(subject, year, paper_code, False),
                    })
                    paper_id += 1
                    
                    # Marking Scheme
                    papers.append({
                        "id": paper_id,
                        "year": year,
                        "subject": subject,
                        "subject_code": subject_code,
                        "type": "marking_scheme",
                        "series": series,
                        "set": f"Set {set_num}",
                        "paper_code": paper_code,
                        "region": region,
                        "filename": f"CBSE_{year}_{subject.replace(' ', '_')}_{paper_code}_MS.pdf",
                        "display_name": f"{subject} {year} {region} Set {set_num} - Marking Scheme",
                        "urls": generate_mirror_urls(subject, year, paper_code, True),
                    })
                    paper_id += 1
            
            # Compartment papers
            for series in compartment_series.keys():
                paper_code = f"{subject_code}-{series}"
                
                # Compartment Question Paper
                papers.append({
                    "id": paper_id,
                    "year": year,
                    "subject": subject,
                    "subject_code": subject_code,
                    "type": "compartment",
                    "series": series,
                    "set": "Compartment",
                    "paper_code": paper_code,
                    "region": "Compartment",
                    "filename": f"CBSE_{year}_{subject.replace(' ', '_')}_{paper_code}_Compartment_QP.pdf",
                    "display_name": f"{subject} {year} Compartment - Question Paper",
                    "urls": generate_mirror_urls(subject, year, paper_code, False, True),
                })
                paper_id += 1
                
                # Compartment Marking Scheme
                papers.append({
                    "id": paper_id,
                    "year": year,
                    "subject": subject,
                    "subject_code": subject_code,
                    "type": "compartment",
                    "series": series,
                    "set": "Compartment MS",
                    "paper_code": paper_code,
                    "region": "Compartment",
                    "filename": f"CBSE_{year}_{subject.replace(' ', '_')}_{paper_code}_Compartment_MS.pdf",
                    "display_name": f"{subject} {year} Compartment - Marking Scheme",
                    "urls": generate_mirror_urls(subject, year, paper_code, True, True),
                })
                paper_id += 1
            
            # Sample Papers (one per subject per year)
            sample_code = f"{subject_code}-SQP"
            papers.append({
                "id": paper_id,
                "year": year,
                "subject": subject,
                "subject_code": subject_code,
                "type": "sample_paper",
                "series": "SQP",
                "set": "Sample",
                "paper_code": sample_code,
                "region": "Sample Paper",
                "filename": f"CBSE_{year}_{subject.replace(' ', '_')}_Sample_Paper.pdf",
                "display_name": f"{subject} {year} - Sample Question Paper",
                "urls": generate_mirror_urls(subject, year, sample_code, False, False, True),
            })
            paper_id += 1
            
            # Sample Paper Marking Scheme
            papers.append({
                "id": paper_id,
                "year": year,
                "subject": subject,
                "subject_code": subject_code,
                "type": "sample_paper",
                "series": "SQP",
                "set": "Sample MS",
                "paper_code": sample_code,
                "region": "Sample Paper",
                "filename": f"CBSE_{year}_{subject.replace(' ', '_')}_Sample_MS.pdf",
                "display_name": f"{subject} {year} - Sample Marking Scheme",
                "urls": generate_mirror_urls(subject, year, sample_code, True, False, True),
            })
            paper_id += 1
    
    return papers


# Pre-generate the paper list
ALL_PAPERS = generate_paper_list()


def get_all_papers():
    """Get all papers"""
    return ALL_PAPERS


def get_paper_by_id(paper_id):
    """Get a specific paper by ID"""
    for paper in ALL_PAPERS:
        if paper["id"] == paper_id:
            return paper
    return None


def filter_papers(year=None, subject=None, paper_type=None, region=None, search=None):
    """Filter papers based on criteria"""
    papers = ALL_PAPERS.copy()
    
    if year:
        papers = [p for p in papers if p["year"] == year]
    if subject:
        papers = [p for p in papers if p["subject"] == subject]
    if paper_type:
        papers = [p for p in papers if p["type"] == paper_type]
    if region:
        papers = [p for p in papers if p["region"] == region]
    if search:
        search_lower = search.lower()
        papers = [p for p in papers if (
            search_lower in p["display_name"].lower() or 
            search_lower in p.get("paper_code", "").lower() or
            search_lower in p.get("subject", "").lower()
        )]
    
    return papers


def get_filter_options():
    """Get available filter options"""
    regions = sorted(list(set(p["region"] for p in ALL_PAPERS)))
    return {
        "years": YEARS,
        "subjects": SUBJECTS,
        "types": PAPER_TYPES,
        "regions": regions
    }


def get_paper_count():
    """Get total paper count"""
    return len(ALL_PAPERS)


if __name__ == "__main__":
    print(f"Total papers in database: {get_paper_count()}")
    print(f"Subjects: {SUBJECTS}")
    print(f"Years: {YEARS}")
    print(f"Sample paper entry:")
    sample = get_paper_by_id(1)
    if sample:
        print(f"  {sample['display_name']}")
        print(f"  URLs: {sample['urls'][:2]}")

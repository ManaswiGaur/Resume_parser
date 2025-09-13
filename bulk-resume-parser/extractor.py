import re
import docx
import PyPDF2
import io
import spacy
from utils import read_pdf, read_docx

nlp = spacy.load("en_core_web_sm")

# Predefined lists
skill_list = [
    'python', 'java', 'c++', 'sql', 'html', 'css', 'javascript', 'react', 'node',
    'machine learning', 'deep learning', 'docker', 'flask', 'fastapi', 'excel',
    'pandas', 'numpy', 'kafka', 'aws', 'hibernate', 'spring', 'spring boot',
    'tensorflow', 'git', 'angular', 'angularjs', 'jenkins', 'mockito', 'sonar cloud'
]

company_blacklist = [
    'Java', 'Spring Boot', 'Spring JDBC', 'Hibernate', 'SQL', 'AWS', 'India',
    'Python', 'Docker', 'Kafka', 'Excel', 'Pandas', 'Oracle', 'Jenkins', 'Git',
    'AngularJs', 'Mockito', 'Sonar Cloud', 'GitHub', 'Node', 'HTML', 'CSS',
    'MySQL', 'REST', 'JSON', 'JavaScript', 'Linux'
]

def extract_name(text):
    lines = text.splitlines()
    job_keywords = ['developer', 'engineer', 'lead', 'manager', 'consultant', 'intern', 'analyst', 'architect']

    for line in lines[:5]:
        line = line.strip()
        if not line or ',' in line or ':' in line or len(line.split()) > 3 or len(line.split()) < 2:
            continue
        if any(j in line.lower() for j in job_keywords):
            continue
        if all(w[0].isupper() for w in line.split() if w.isalpha()):
            return line

    doc = nlp(text[:300])
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text

    return "Not Found"

def extract_skills(text):
    found = [skill for skill in skill_list if skill.lower() in text.lower()]
    return ", ".join(sorted(set(found), key=found.index))

def extract_experience(text):
    match = re.search(r'(\d+)\+?\s*(years|yrs)[\s\w]*experience', text.lower())
    return match.group(1) + " years" if match else "Not Found"

def extract_companies(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    job_entries = []
    # Date formats like: 2021 - Present, Oct 2021 to till date, etc.
    date_pattern = re.compile(
        r'\b(?:\d{4}|\bJan|\bFeb|\bMar|\bApr|\bMay|\bJun|\bJul|\bAug|\bSep|\bOct|\bNov|\bDec)[^\n]{0,30}?(?:Current|Present|till date|\d{4})',
        re.IGNORECASE
    )

    i = 0
    while i < len(lines):
        line = lines[i]

        # Likely company name line
        if (
            re.match(r'^[A-Z][\w &().,-]{2,}$', line)
            and not any(x.lower() in line.lower() for x in ['role', 'title', 'responsibility', 'project', 'duration'])
            and len(line.split()) <= 5
            and not re.search(r'\d{4}', line)
            and line not in company_blacklist
        ):
            # Check next 1–2 lines for date range
            next_lines = lines[i+1:i+3]
            date_line = next((nl for nl in next_lines if date_pattern.search(nl)), None)
            if date_line:
                job_entries.append({"company": line, "date": date_line})
                i += 2
                continue

        i += 1

    if not job_entries:
        return "Not Found", "Not Found"

    current = job_entries[0]["company"]
    last = job_entries[1]["company"] if len(job_entries) > 1 else "Not Found"

    return current, last

def extract_location(text):
    doc = nlp(text)
    priority_cities = ['Hyderabad', 'Bangalore', 'Pune', 'Mumbai', 'Chennai', 'Delhi', 'Kolkata']
    gpes = [ent.text for ent in doc.ents if ent.label_ == "GPE"]

    for city in priority_cities:
        if city in gpes:
            return city
    for loc in gpes:
        if loc.lower() != "india":
            return loc
    return "India" if "india" in text.lower() else "Not Found"

def parse_resume(filename, content):
    if filename.endswith(".pdf"):
        text = read_pdf(io.BytesIO(content))
    elif filename.endswith(".docx"):
        text = read_docx(io.BytesIO(content))
    else:
        return {"error": "Unsupported file format"}

    current_company, last_company = extract_companies(text)

    return {
        "name": extract_name(text),
        "skills": extract_skills(text),
        "experience": extract_experience(text),
        "current_company": current_company,
        "last_company": last_company,
        "location": extract_location(text),
    }

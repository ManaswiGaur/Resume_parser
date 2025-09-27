# Bulk Resume Parser

A FastAPI-based web application that extracts structured information from multiple resume files (PDF and DOCX) and exports the parsed data to CSV or JSON format. The system uses natural language processing with spaCy to intelligently extract candidate details including names, skills, experience, company history, and location information.

## Features

- **Multi-format Support**: Parse both PDF (.pdf) and Word (.docx) resume files
- **Batch Processing**: Upload and process multiple resumes simultaneously
- **Intelligent Extraction**: Uses spaCy NLP for accurate information extraction
- **Flexible Output**: Export results as CSV or JSON files
- **Web Interface**: Simple HTML upload interface with drag-and-drop functionality
- **RESTful API**: FastAPI backend with automatic API documentation
- **CORS Enabled**: Cross-origin resource sharing for web integration

## Extracted Information

The parser extracts the following key information from each resume:

- **Name**: Candidate's full name using NER and pattern matching
- **Skills**: Technical skills matching predefined skill categories
- **Experience**: Years of professional experience
- **Current Company**: Most recent employer
- **Last Company**: Previous employer (if available)
- **Location**: Geographic location (city/state/country)
- **Filename**: Original resume file name for reference

## Technology Stack

- **Backend**: FastAPI (Python web framework)
- **NLP Processing**: spaCy with English language model
- **File Processing**: PyPDF2 for PDFs, python-docx for Word documents
- **Data Export**: Pandas for CSV/JSON generation
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Server**: Uvicorn ASGI server

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd bulk-resume-parser
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download spaCy language model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Usage

### Starting the Server

1. **Run the FastAPI server**:
   ```bash
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

2. **Access the web interface**:
   - Open `upload.html` in your browser using a local server (e.g., Live Server extension in VS Code)
   - Or visit: `http://127.0.0.1:5500/upload.html`

### Using the Web Interface

1. **Select Resume Files**: Click "Choose Files" and select multiple PDF or DOCX files
2. **Choose Output Format**: Select either CSV or JSON from the dropdown
3. **Upload**: Click "Upload" to process the resumes
4. **Download Results**: The processed file will automatically download

### API Endpoints

#### Upload Resumes
```http
POST /upload-resumes/
```

**Parameters**:
- `files`: List of resume files (multipart/form-data)
- `format`: Output format ("csv" or "json")

**Response**: File download containing parsed resume data

**Example using curl**:
```bash
curl -X POST "http://127.0.0.1:8000/upload-resumes/?format=csv" \
     -F "files=@resume1.pdf" \
     -F "files=@resume2.docx"
```

## Configuration

### Skill Categories

The parser recognizes the following technical skills (defined in `extractor.py`):

- **Programming Languages**: Python, Java, C++, JavaScript
- **Web Technologies**: HTML, CSS, React, Node, Angular
- **Databases**: SQL, MySQL, Oracle
- **Frameworks**: Spring, Spring Boot, Flask, FastAPI
- **DevOps**: Docker, Jenkins, Git, AWS
- **Data Science**: Machine Learning, Deep Learning, Pandas, NumPy, TensorFlow
- **Testing**: Mockito
- **Other**: Kafka, Hibernate, Excel, Sonar Cloud

### Company Blacklist

The system filters out common technical terms that might be misidentified as company names:

```python
company_blacklist = [
    'Java', 'Spring Boot', 'Spring JDBC', 'Hibernate', 'SQL', 'AWS', 'India',
    'Python', 'Docker', 'Kafka', 'Excel', 'Pandas', 'Oracle', 'Jenkins', 'Git',
    'AngularJs', 'Mockito', 'Sonar Cloud', 'GitHub', 'Node', 'HTML', 'CSS',
    'MySQL', 'REST', 'JSON', 'JavaScript', 'Linux'
]
```

## File Structure

```
bulk-resume-parser/
├── main.py              # FastAPI application and endpoints
├── extractor.py         # Core parsing logic and NLP functions
├── utils.py            # File reading utilities
├── upload.html         # Web interface
├── requirements.txt    # Python dependencies
└── parsed_output_*.csv # Generated output files
```

## Sample Output

### CSV Format
```csv
name,skills,experience,current_company,last_company,location,filename
Sreekar SRS,"python, java, sql, docker, kafka, aws, hibernate, spring, spring boot, git",7 years,Mockito,Jenkins,Telangana,Sreekar SRS.pdf
Saikumari Naidu,"java, sql, excel, kafka, aws, hibernate, spring, spring boot, git",7 years,Code,Sonar Cloud,Hyderabad,Saikumari Naidu.pdf
```

### JSON Format
```json
[
  {
    "name": "Sreekar SRS",
    "skills": "python, java, sql, docker, kafka, aws, hibernate, spring, spring boot, git",
    "experience": "7 years",
    "current_company": "Mockito",
    "last_company": "Jenkins",
    "location": "Telangana",
    "filename": "Sreekar SRS.pdf"
  }
]
```

## Troubleshooting

### Common Issues

1. **spaCy Model Not Found**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **CORS Errors**:
   - Ensure you're serving `upload.html` from `http://127.0.0.1:5500`
   - Check that FastAPI server is running on `http://127.0.0.1:8000`

3. **File Upload Errors**:
   - Verify file formats are PDF or DOCX
   - Check file size limits
   - Ensure files are not corrupted

4. **Parsing Accuracy Issues**:
   - Review and update skill lists in `extractor.py`
   - Adjust company blacklist for your domain
   - Consider training custom NER models for better accuracy

### Performance Optimization

- **Large File Processing**: Consider implementing async file processing for large batches
- **Memory Usage**: Monitor memory consumption with large PDF files
- **Caching**: Implement caching for frequently processed resume formats

## Customization

### Adding New Skills
Edit the `skill_list` in `extractor.py`:
```python
skill_list = [
    'python', 'java', 'c++', 'sql', 'html', 'css', 'javascript',
    # Add your custom skills here
    'kubernetes', 'terraform', 'scala'
]
```

### Modifying Extraction Logic
- **Name Extraction**: Update `extract_name()` function for different name patterns
- **Experience Parsing**: Modify regex patterns in `extract_experience()`
- **Company Detection**: Adjust company extraction logic in `extract_companies()`

### UI Customization
- Modify `upload.html` for custom styling and branding
- Add progress bars and upload status indicators
- Implement drag-and-drop functionality

## API Documentation

When the server is running, visit:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check existing GitHub issues
2. Create a new issue with detailed problem description
3. Include sample resume files (anonymized) for debugging

## Future Enhancements

- **Contact Information**: Extract phone numbers and email addresses
- **Education Details**: Parse educational background and degrees
- **Certifications**: Identify professional certifications
- **Machine Learning**: Implement ML-based classification for resume categories
- **Database Integration**: Store parsed data in databases
- **Advanced NLP**: Use transformer models for better accuracy
- **Duplicate Detection**: Identify and merge duplicate candidate profiles

# Career Avatar Data Directory

This directory contains user-specific data files that are required to run the Career Avatar application. These files are **not included in the repository** for privacy and security reasons.

## Required Files

### 1. `linkedin.pdf`
**Description:** Export of your LinkedIn profile

**How to prepare:**
1. Log into your LinkedIn account
2. Go to your profile (click on your photo)
3. Click "More" → "Save to PDF"
4. Save the file as `linkedin.pdf` in this directory

**Purpose:** The system extracts text from this PDF to provide context about your professional background, skills, and experience when responding to visitor inquiries.

**Size:** typically 2-5 MB

---

### 2. `summary.txt`
**Description:** A professional summary of your career and background

**How to prepare:**
1. Create a new text file named `summary.txt`
2. Write a clear, professional overview of your career
3. Save it in this directory

**Example content:**
```
Senior Software Engineer with 10+ years of experience in cloud infrastructure 
and distributed systems. Expertise in Python, Go, Kubernetes, and AWS. 

Currently seeking full-time and contract opportunities in backend engineering, 
DevOps, and cloud architecture roles. Available for immediate engagement.

Key Skills:
- Backend Development (Python, Go, Node.js)
- Cloud Platforms (AWS, GCP, Azure)
- Container Orchestration (Kubernetes)
- System Design and Architecture
```

**Tips:**
- Keep it between 100-300 words for optimal performance
- Include your key skills, experience level, and current goals
- Be specific about your expertise areas
- Mention what types of opportunities you're interested in
- This will be injected into the AI system prompt, so clarity is important

**Purpose:** Provides quick context to the AI about your professional background, which it uses to answer visitor questions and maintain authentic representation.

---

## Directory Structure After Setup

Once you've added the required files, your data directory should look like:

```
career_avatar/data/
├── README.md              (this file)
├── linkedin.pdf           (your LinkedIn profile export)
└── summary.txt            (your career summary)
```

## Security Notes

- ⚠️ These files are **never committed to git** (see .gitignore)
- 📄 Both files are only loaded into memory when the application starts
- 🔒 Information is only used locally (sent to OpenAI API for inference)
- 🗝️ Ensure your `.env` file with API keys is also not tracked

## Troubleshooting

**"File not found" errors on startup:**
- Verify both `linkedin.pdf` and `summary.txt` exist in this directory
- Check file names are exactly as specified (case-sensitive on Linux/Mac)
- Ensure read permissions are set on the files

**Application not loading your data:**
- Restart the application after placing files in this directory
- Check logs for any PDF parsing errors
- Verify the summary.txt file is valid UTF-8 text

**PDF extraction issues:**
- Ensure your LinkedIn PDF is a standard PDF file
- Try re-exporting from LinkedIn if the file seems corrupted
- Some older PDF formats may have parsing issues

## Next Steps

1. Export your LinkedIn profile as PDF
2. Create your summary.txt file  
3. Place both files in this directory (alongside this README)
4. Run `python -m career_avatar.app` to start the application

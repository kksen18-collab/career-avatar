# Career Avatar

An intelligent AI-powered chatbot system that serves as your professional representative on your personal website, engaging with visitors through contextually aware conversations about your career, background, and expertise.

## Overview

Career Avatar is a production-grade Python application that leverages OpenAI's GPT-4o-mini language model to create an automated professional persona. The system:

- Represents your professional profile on your personal website
- Provides intelligent responses to inquiries about your career and expertise
- Integrates your LinkedIn profile and personal career summary for context
- Captures visitor contact information and qualification data
- Logs unanswerable questions for manual review
- Delivers real-time notifications via Pushover integration

This solution is designed to streamline professional networking, improve recruiter engagement, and automate preliminary inquiry handling on your personal website.

## Features

**AI-Powered Conversational Interface**

- Leverages OpenAI's GPT-4o-mini for sophisticated natural language processing
- Context-aware responses informed by your LinkedIn profile and career summary
- Maintains professional tone aligned with recruiter and employer expectations
- Implements function calling for intelligent tool integration

**Visitor Engagement and Lead Capture**

- Automated extraction and storage of visitor contact information
- Question logging and analytics for unaddressed topics
- Real-time notifications via Pushover API
- Professional conversation steering towards direct contact channels

**Web-Based User Interface**

- Built with Gradio for accessible, responsive chat experience
- Zero-configuration deployment model
- Cross-platform compatibility and mobile responsiveness

**Data-Driven Intelligence**

- Integration of LinkedIn profile data in PDF format
- Custom career summary contextualization
- Consistent and authentic professional representation

## Installation

### System Requirements

- Python 3.13 or higher
- OpenAI API account with active API key
- Pushover account for notification services
- PDF export capability from LinkedIn profile

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd career-avatar
   ```

2. **Install dependencies**
   ```bash
   pip install -e .
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the `career_avatar/` directory:
   ```
   OPENAI_API_KEY=sk-your-openai-key-here
   PUSHOVER_USER_KEY=your-pushover-user-key
   PUSHOVER_API_TOKEN=your-pushover-api-token
   PUSHOVER_URL=https://api.pushover.net/1/messages.json
   NAME=Your Full Name
   MODEL=gpt-4o-mini
   ```

4. **Prepare required data files**
   - Export your LinkedIn profile as PDF and place at `career_avatar/data/linkedin.pdf`
   - Create a career summary file at `career_avatar/data/summary.txt`
   
   Example summary:
   ```
   Senior Software Engineer with 7+ years of experience in distributed systems 
   and cloud infrastructure. Expertise in Python, Go, AWS, and Kubernetes. 
   Currently available for contract and full-time opportunities.
   ```

## Usage

### Starting the Application

Execute the following command to launch the Career Avatar service:

```bash
python -m career_avatar.app
```

The application will initialize a Gradio web interface accessible at `http://localhost:7860`.

### System Behavior

Upon launch, the system:

1. Loads your LinkedIn profile and career summary into memory
2. Initializes OpenAI API connection and tool handlers
3. Establishes Pushover notification channel
4. Deploys web interface for visitor interactions

Visitors can then:
- Submit inquiries regarding your background and expertise
- Provide contact information when relevant
- Receive contextually accurate responses informed by your professional data

The system automatically:
- Extracts and persists contact information when provided
- Records questions that fall outside its knowledge base
- Sends notifications to your Pushover account for each visitor interaction
- Maintains conversation history for each session

## Configuration

### Environment Variables

The following environment variables must be configured in the `.env` file:

| Variable | Description | Required | Format |
|----------|-------------|----------|--------|
| `OPENAI_API_KEY` | OpenAI API authentication key | Yes | Must start with `sk-` |
| `PUSHOVER_USER_KEY` | Pushover account user key | Yes | String (typically 30 chars) |
| `PUSHOVER_API_TOKEN` | Pushover application API token | Yes | String (typically 30 chars) |
| `PUSHOVER_URL` | Pushover API endpoint | Yes | `https://api.pushover.net/1/messages.json` |
| `NAME` | Your full name (used in system prompts) | Yes | String |
| `MODEL` | OpenAI model identifier | No | Default: `gpt-4o-mini` |
| `LINKEDIN_PDF_PATH` | Path to LinkedIn PDF export | No | Default: `data/linkedin.pdf` |
| `SUMMARY_PATH` | Path to career summary file | No | Default: `data/summary.txt` |

### Prompt Customization

The system prompt can be customized by modifying [career_avatar/prompt.py](career_avatar/prompt.py). The PromptBuilder class constructs the instruction set used by the language model:

```python
prompt = f"You are acting as {self.name}. Your role is to represent..."
```

### Model Selection

The OpenAI model can be configured via the `MODEL` environment variable. The default is `gpt-4o-mini`, which provides a good balance of cost and capability. Alternative options include:

- `gpt-4o` — Larger model with enhanced reasoning
- `gpt-4-turbo` — Previous generation with specialized capabilities
- Any other OpenAI model available in your organization

Simply set `MODEL=gpt-4o` in your `.env` file to switch models without code changes.

### Extending Functionality

New tools can be added by:
1. Creating a new module in `career_avatar/tools/`
2. Defining the tool JSON schema in `tools.py`
3. Implementing handler logic in the `Tools.handle_tool_calls()` method

## Project Structure

```
career-avatar/
├── career_avatar/
│   ├── app.py                          Main application entry point
│   ├── avatar.py                       Avatar orchestration logic
│   ├── prompt.py                       System prompt building
│   ├── loader.py                       File I/O operations
│   ├── parameters.py                   Configuration validation
│   ├── client/
│   │   ├── openai.py                   OpenAI API wrapper
│   │   └── pushover.py                 Pushover integration
│   ├── tools/
│   │   ├── tools.py                    Tool handler
│   │   ├── record_user_details.py      Visitor information capture
│   │   └── record_unknown_question.py  Question logging
│   └── data/
│       ├── linkedin.pdf                LinkedIn profile (add this)
│       └── summary.txt                 Career summary (add this)
├── pyproject.toml                      Project metadata and dependencies
├── LICENSE                             License terms
└── README.md                           This file
```

## Architecture

The application implements a modular, layered architecture:

**Core Components**

- **Avatar** — Primary orchestration class managing chat logic and multi-turn conversations
- **PromptBuilder** — Generates system prompts from your professional data
- **OpenAIClient** — Encapsulates OpenAI API interactions with function calling support
- **Tools** — Manages AI-invoked tool calls and integrations
- **PushoverClient** — Handles notification delivery
- **Loader** — Handles PDF and text file I/O operations

**Request Flow**

```
1. User submits inquiry via web interface
2. Avatar constructs system prompt from stored professional data
3. OpenAI processes query with available tool definitions
4. Language model selects appropriate tools based on response logic
5. Avatar executes tool calls and passes results back to model
6. Process iterates until final response is generated
7. Response delivered to user; notifications sent to account owner
```

## API Integration Requirements

### OpenAI Configuration

1. Create account at https://platform.openai.com
2. Generate API key from https://platform.openai.com/api-keys
3. Ensure account has sufficient credits
4. Add key to `.env` with format: `OPENAI_API_KEY=sk-...`

### Pushover Configuration

1. Register account at https://pushover.net
2. Retrieve user key from account dashboard
3. Create or obtain API token for application
4. Configure both values in `.env`

## Dependencies

The following packages are required and will be installed with `pip install -e .`:

| Package | Version | Purpose |
|---------|---------|----------|
| pydantic | ≥2.12.5 | Data validation and type checking |
| openai | ≥2.26.0 | OpenAI API client library |
| python-dotenv | ≥1.2.2 | Environment variable management |
| pydantic-settings | 2.13.1 | Configuration management |
| requests | 2.32.5 | HTTP client library |
| pypdf | 6.7.5 | PDF text extraction |
| gradio | 6.9.0 | Web interface framework |
| pathlib | 1.0.1 | Path handling utilities |

All versions are pinned in `pyproject.toml` for reproducibility.

## Troubleshooting

### OpenAI API Key Validation Error

**Symptom:** "Invalid OpenAI API key" error on startup

**Resolution:**
- Verify API key format (must begin with `sk-`)
- Confirm entire key is accurately transcribed in `.env`
- Validate key has not expired or been revoked
- Check account has active credits

### File Not Found Errors

**Symptom:** "File not found: linkedin.pdf" or "File not found: summary.txt"

**Resolution:**
- Verify files exist in `career_avatar/data/` directory
- Confirm correct file paths in `.env` if using custom locations
- Ensure file permissions allow read access

### Port Availability Issues

**Symptom:** "Address already in use" on port 7860

**Resolution:**
- Identify process using port 7860
- Terminate conflicting process or configure alternative port
- Gradio configuration can be modified in `app.py`

## License

See [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or feature requests, please refer to the Troubleshooting section above or consult the project documentation.

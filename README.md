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
- Includes automated quality evaluation of responses using AI

This solution is designed to streamline professional networking, improve recruiter engagement, and automate preliminary inquiry handling on your personal website.

## Technology & Implementation Approach

Career Avatar is built using **bare-bones OpenAI API calls** with **custom tool orchestration**, rather than relying on agent SDKs or high-level frameworks. This approach provides:

**Core Technology Choices:**
- **Direct OpenAI API**: Raw `chat.completions.create()` calls with function calling support
- **Structured Output Parsing**: Uses `client.responses.parse()` with Pydantic models for deterministic validation
- **Custom Tool Definitions**: Tools defined as JSON schemas from scratch, not auto-generated
- **Manual Orchestration**: Explicit control over request/response loops and tool execution
- **Function Calling**: Native OpenAI function calling mechanism for AI-invoked tool integration
- **Gradio UI**: Lightweight web interface without complex abstraction layers

**Why This Approach:**
- **Full Control**: Complete visibility into API calls, prompts, and tool handling
- **No Dependencies**: Avoids agent SDK limitations and abstraction overhead
- **Flexible & Transparent**: Easy to modify behavior, inspect execution, and add custom logic
- **Cost Efficient**: Direct API usage without middleware frameworks
- **Educational**: Clear implementation of how AI agents work at a fundamental level

**Architecture Highlights:**
- Manual management of conversation history and context
- Custom JSON schemas for `record_user_details` and `record_unknown_question` tools
- Explicit iteration loops for handling tool calls and response evaluation
- Direct error handling and logging without framework conventions

This implementation is ideal for developers who want to understand exactly how their system works and need fine-grained control over AI interactions.

## Features

**AI-Powered Conversational Interface**

- Leverages OpenAI's GPT-4o-mini for sophisticated natural language processing
- Context-aware responses informed by your LinkedIn profile and career summary
- Maintains professional tone aligned with recruiter and employer expectations
- Implements function calling for intelligent tool integration
- Quality control evaluation of responses before delivery

**Visitor Engagement and Lead Capture**

- Automated extraction and storage of visitor contact information via `record_user_details` tool
- Question logging and analytics for unaddressed topics via `record_unknown_question` tool
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
- Multi-turn conversation history tracking

## Project Structure

```
career-avatar/
├── README.md
├── LICENSE (MIT License)
├── pyproject.toml
├── career_avatar/
│   ├── __init__.py
│   ├── app.py                 # Main application entry point with Gradio interface
│   ├── avatar.py              # Core Avatar class handling conversations
│   ├── evaluation.py          # Quality evaluation logic
│   ├── loader.py              # Data file loaders for PDF and text files
│   ├── logger.py              # Logging configuration
│   ├── parameters.py          # Settings and configuration management
│   ├── prompt.py              # System prompt builders for Avatar and Evaluator
│   ├── data/
│   │   ├── linkedin.pdf       # LinkedIn profile PDF (exported from LinkedIn)
│   │   └── summary.txt        # Career summary text file
│   ├── client/
│   │   ├── __init__.py
│   │   ├── openai.py          # OpenAI API client wrapper
│   │   └── pushover.py        # Pushover notification client
│   └── tools/
│       ├── __init__.py
│       ├── tools.py           # Tool handler and dispatcher
│       ├── record_user_details.py    # Schema for recording user contact info
│       └── record_unknown_question.py # Schema for logging unanswered questions
└── .env                       # Environment variables (not in repo, user creates)
```

## Installation

### System Requirements

- Python 3.13 or higher
- OpenAI API account with active API key (GPT-4o-mini model)
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
   
   This installs the following key dependencies:
   - `openai>=2.26.0` - OpenAI API client
   - `gradio==6.9.0` - Web UI framework
   - `pydantic>=2.12.5` - Data validation
   - `pydantic-settings==2.13.1` - Settings management
   - `requests==2.32.5` - HTTP client for Pushover
   - `pypdf==6.7.5` - PDF text extraction
   - `python-dotenv>=1.2.2` - Environment variable management

3. **Configure environment variables**
   
   Create a `.env` file in the `career_avatar/` directory:
   ```
   OPENAI_API_KEY=sk-your-openai-key-here
   PUSHOVER_USER_KEY=your-pushover-user-key
   PUSHOVER_API_TOKEN=your-pushover-api-token
   PUSHOVER_URL=https://api.pushover.net/1/messages.json
   NAME=Your Full Name
   MODEL=gpt-4o-mini
   LINKEDIN_PDF_PATH=career_avatar/data/linkedin.pdf
   SUMMARY_PATH=career_avatar/data/summary.txt
   ```

4. **Prepare required data files**
   
   **LinkedIn Profile PDF:**
   - Export your LinkedIn profile as PDF
   - Place at `career_avatar/data/linkedin.pdf`
   - The system will extract text from this PDF to provide career context
   
   **Career Summary File:**
   - Create a career summary file at `career_avatar/data/summary.txt`
   - This should be a clear, professional overview of your background
   
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

The Gradio interface will start and typically open in your default browser at `http://localhost:7860/`

### How It Works

1. **Visitor Interaction**: Visitors access your personal website and interact with the chatbot
2. **Context Loading**: The Avatar loads your LinkedIn profile and career summary
3. **Message Processing**: User messages are processed through the OpenAI API
4. **Tool Integration**: The Avatar can call tools to:
   - Record user contact information when they express interest
   - Log questions that couldn't be answered
5. **Quality Evaluation**: Responses are evaluated for quality before delivery
6. **Notifications**: Important interactions trigger Pushover notifications to your phone

## Architecture

### Core Components

**Avatar Class** (`avatar.py`)
- Main conversation handler
- Manages message history and context
- Integrates with OpenAI client and Tools
- Handles multi-turn conversations
- Uses PromptBuilder to create contextual system prompts

**OpenAI Client** (`client/openai.py`)
- Wrapper around OpenAI Python library
- Handles chat completions with function calling
- Supports structured output parsing
- Manages API communication and error handling

**Evaluator** (`evaluation.py`)
- Quality control for generated responses
- Uses separate AI evaluation logic
- Can trigger response regeneration if quality is insufficient
- Provides feedback on response appropriateness

**Tools System** (`tools/`)
- `record_user_details`: Captures visitor contact information and context
- `record_unknown_question`: Logs questions the Avatar cannot answer
- Tool dispatcher handles function calling results

**Prompt Builder** (`prompt.py`)
- Constructs system prompts with context injection
- Creates Avatar system prompt with name, summary, and LinkedIn data
- Creates Evaluator system prompt for quality assessment
- Maintains consistent professional representation

**Settings Management** (`parameters.py`)
- Centralized configuration using Pydantic Settings
- Loads environment variables from `.env` file
- Validates API keys and model settings
- Type-safe configuration access

**Data Loader** (`loader.py`)
- Extracts text from LinkedIn PDF files
- Loads career summary from text files
- Handles file encoding and error management

**Pushover Client** (`client/pushover.py`)
- Real-time notification delivery
- Sends alerts for user interactions and unknown questions
- Integrates with Pushover notification service

### Conversation Flow

```
User Message
    ↓
Avatar receives message + history
    ↓
PromptBuilder injects context (name, summary, LinkedIn)
    ↓
OpenAI generates response with tool definitions
    ↓
Tool calls are detected and processed:
  ├─ record_user_details → sends Pushover notification
  └─ record_unknown_question → sends Pushover notification
    ↓
Evaluator assesses response quality
    ↓
If quality rejected → Avatar regenerates response
    ↓
Response returned to user
```

## Available Tools

### `record_user_details`

Records visitor contact information and engagement context.

**Parameters:**
- `email` (string, required): The visitor's email address
- `name` (string, optional): The visitor's name
- `notes` (string, optional): Additional conversation context

**Example Usage:**
Avatar automatically calls this when a visitor expresses interest and provides their email.

```python
# When called, triggers Pushover notification:
# "Recording interest from John Doe with email john@example.com and notes ..."
```

### `record_unknown_question`

Logs questions that the Avatar cannot answer.

**Parameters:**
- `question` (string, required): The question that couldn't be answered

**Example Usage:**
Avatar automatically calls this for out-of-scope questions like technical support issues unrelated to your career.

```python
# When called, triggers Pushover notification:
# "Recording [question] asked that I couldn't answer"
```

## Configuration Details

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | - | OpenAI API key (must start with `sk-`) |
| `PUSHOVER_USER_KEY` | Yes | - | Your Pushover user key |
| `PUSHOVER_API_TOKEN` | Yes | - | Pushover API token for your app |
| `PUSHOVER_URL` | Yes | https://api.pushover.net/1/messages.json | Pushover API endpoint |
| `NAME` | Yes | - | Your full name for the Avatar |
| `MODEL` | No | `gpt-4o-mini` | OpenAI model to use |
| `LINKEDIN_PDF_PATH` | No | `career_avatar/data/linkedin.pdf` | Path to LinkedIn PDF |
| `SUMMARY_PATH` | No | `career_avatar/data/summary.txt` | Path to career summary |

### Settings Validation

- OpenAI API key must start with `sk-` prefix
- All required environment variables must be present
- File paths are validated at startup

## Development

### Logging

The application uses Python's logging module with configurable levels. Logs include:
- API interactions with OpenAI
- Tool calls and execution
- Pushover notifications
- System prompts and evaluated responses

### Error Handling

- Invalid API keys are caught at startup
- File loading errors are logged
- OpenAI API errors are propagated with context
- Tool execution failures trigger fallback responses

## Advanced Configuration

### Prompt Customization

The system prompt can be customized by modifying [career_avatar/prompt.py](career_avatar/prompt.py). The PromptBuilder class constructs the instruction set used by the language model:

```python
prompt = f"You are acting as {self.name}. Your role is to represent..."
```

### Model Selection

The OpenAI model can be configured via the `MODEL` environment variable. The default is `gpt-4o-mini`, which provides a good balance of cost and capability. Alternative options include:

- `gpt-4o` — Larger model with enhanced reasoning
- `gpt-4-turbo` — Previous generation with specialized capabilities

Simply set `MODEL=gpt-4o` in your `.env` file to switch models without code changes.

### Extending Functionality

New tools can be added by:
1. Creating a new module in `career_avatar/tools/`
2. Defining the tool JSON schema in `tools.py`
3. Implementing handler logic in the `Tools.handle_tool_calls()` method

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

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

MIT License (c) 2026 Kaushik Kumar Sen

## License

See [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or feature requests, please refer to the Troubleshooting section above or consult the project documentation.

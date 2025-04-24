# MCP MoP Uploader

## Purpose

This application is built to automate the generation and storage of **Method of Procedure (MoP)** documents using a Large Language Model (LLM) from OpenAI, integrated with **AWS S3** via a custom [Model Context Protocol (MCP)] tool.  
The goal is to reduce manual effort in creating MoP documents and streamline their delivery to cloud storage systems.

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/adhika28/MCP-AWS-S3Upload.git
cd MCP-AWS-S3Upload
```

### 2. Create a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set environment variables
You can set them via terminal or create a `.env` file:
```bash
export OPENAI_API_KEY="your-openai-api-key"
export AWS_ACCESS_KEY_ID="your-aws-access-key-id"
export AWS_SECRET_ACCESS_KEY="your-aws-secret-key"
export S3_BUCKET="your-s3-bucket-name"
```

---

## Usage

Run the main script:
```bash
python run_mop.py
```

You will be prompted to enter a scenario:
```
MoP apa yang ingin kamu buat? provisioning EC2 with Amazon Linux
```

The app will:
1. Generate a MoP document using OpenAI's GPT-4.
2. Save it locally as `Generated_MoP.docx`.
3. Upload the file to `s3://test-mcp-bucket/MoP/Generated_MoP.docx`.

---

## Project Structure
```
.
├── run_mop.py                # Main application
├── requirements.txt          # Python dependencies
├── mcp/tools/base.py         # Simulated MCP toolbase
└── examples/tools/s3_uploader.py  # Custom S3 uploader tool
```

---

## imitations and Known Issues

- No input validation or prompt quality check is implemented.
- Document approval workflow or versioning is **not included**.
- S3 permissions must be correctly configured; otherwise, upload will fail with `AccessDenied`.

---

## Future Improvements

- Add web UI for user input
- Implement version tracking and metadata tagging for MoP files
- Add approval flow

---

Made with 💻 by Putu

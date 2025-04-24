# Import standar library dan third-party libraries
import os
import sys
import asyncio
import nest_asyncio         
from docx import Document 
import openai

# Menambahkan path ke modul internal proyek (mcp tools dan uploader tool)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "mcp", "tools"))
sys.path.append(os.path.join(BASE_DIR, "examples", "tools"))

# Mengimpor uploader tool untuk S3 (custom MCP tool)
from s3_uploader import S3Uploader

# Mock kelas MCPServer
class MCPServer:
    def __init__(self, tools): pass
    async def serve_background(self): pass

# Mock kelas MCPClient
class MCPClient:
    async def get_tool(self, name): return S3Uploader()
    async def run(self, args): return type('Result', (), {'content': 'Simulated Upload'})()

# Mengaktifkan event loop 
nest_asyncio.apply()

# Inisialisasi API key dan AWS
openai.api_key = os.getenv("OPENAI_API_KEY")
os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID")
os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY")
os.environ["AWS_DEFAULT_REGION"] = "ap-southeast-3"
S3_BUCKET = os.getenv("S3_BUCKET", "test-mcp-bucket")

# Fungsi untuk generate isi dokumen MoP dari OpenAI Chat API
def generate_mop(prompt_text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a Cloud Engineer expert."},
            {"role": "user", "content": f"Buatkan dokumen MoP berdasarkan skenario berikut dengan bahasa yang profesional:\n{prompt_text}"}
        ]
    )
    return response['choices'][0]['message']['content']


# Fungsi untuk menyimpan hasil MoP ke file .docx
def save_to_docx(text, filename):
    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)
    doc.save(filename)

# Fungsi asynchronous untuk meng-upload file ke S3 menggunakan MCP tool
async def upload_with_mcp(filename, bucket, key):
    client = MCPClient()
    tool = await client.get_tool("s3_uploader")
    result = tool.run({
        "filename": filename,
        "bucket": bucket,
        "key": key
    })
    return result.content

# Fungsi utama yang akan dijalankan secara asynchronous
async def main():
    server = MCPServer([S3Uploader()])
    await server.serve_background()

    prompt = input("MoP apa yang ingin kamu buat? ")
    mop_text = generate_mop(prompt)

    filename = "Generated_MoP.docx"
    save_to_docx(mop_text, filename)
    print(f"MoP saved to {filename}")

    result = await upload_with_mcp(filename, S3_BUCKET, f"MoP/{filename}")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())

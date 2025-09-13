from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List
from extractor import parse_resume
import pandas as pd
import uuid

app = FastAPI()

# ✅ CORS setup for Live Server (http://127.0.0.1:5500)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve upload.html through FastAPI (optional)
app.mount("/static", StaticFiles(directory="."), name="static")


@app.post("/upload-resumes/")
async def upload_resumes(files: List[UploadFile] = File(...), format: str = "csv"):
    all_data = []

    for file in files:
        try:
            contents = await file.read()
            data = parse_resume(file.filename, contents)
            data["filename"] = file.filename
            all_data.append(data)
        except Exception as e:
            print(f"\n Error processing file {file.filename}:\n{e}\n")
            return {
                "error": f"Failed to process {file.filename}",
                "details": str(e)
            }

    df = pd.DataFrame(all_data)
    output_file = f"parsed_output_{uuid.uuid4()}.{format}"

    try:
        if format == "csv":
            df.to_csv(output_file, index=False)
        else:
            df.to_json(output_file, orient="records", indent=2)

        return FileResponse(output_file, filename=output_file)
    except Exception as e:
        print(f"\n Failed to write output file:\n{e}\n")
        return {"error": "Output generation failed", "details": str(e)}

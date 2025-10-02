from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Bio.Blast import NCBIWWW, NCBIXML
import os

app = FastAPI(title="BLAST API for GammaFold")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BlastSubmitRequest(BaseModel):
    query: str
    database: str = "nr"
    program: str = "blastp"
    expect: float = 10.0
    hitlistSize: int = 100

@app.get("/")
def root():
    return {"status": "BLAST API is running", "service": "GammaFold"}

@app.post("/blast-submit")
async def blast_submit(req: BlastSubmitRequest):
    try:
        api_key = os.getenv("NCBI_API_KEY")
        
        result_handle = NCBIWWW.qblast(
            program=req.program,
            database=req.database,
            sequence=req.query,
            expect=req.expect,
            hitlist_size=req.hitlistSize,
            format_type="XML",
            api_key=api_key
        )
        
        xml_result = result_handle.read()
        result_handle.close()
        
        blast_records = NCBIXML.parse(xml_result)
        record = next(blast_records)
        
        results_text = f"BLAST Results for {req.program}\n"
        results_text += f"Database: {req.database}\n"
        results_text += f"Query: {req.query[:50]}...\n\n"
        
        if record.alignments:
            results_text += f"Found {len(record.alignments)} hits\n\n"
            for i, alignment in enumerate(record.alignments[:10]):
                results_text += f"\n>Hit {i+1}: {alignment.title}\n"
                hsp = alignment.hsps[0]
                results_text += f"  Length: {alignment.length}\n"
                results_text += f"  E-value: {hsp.expect}\n"
                results_text += f"  Score: {hsp.score}\n"
                results_text += f"  Identities: {hsp.identities}/{hsp.align_length}\n"
        else:
            results_text += "No significant hits found.\n"
        
        return {
            "status": "completed",
            "results": results_text,
            "rid": "immediate",
            "rtoe": 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"BLAST error: {str(e)}")

@app.get("/health")
def health():
    return {"healthy": True}


import os
import time
import hashlib
import json
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="TraceGraph Sovereign Engine API", version="3.2.0")

# Broad CORS configuration for Vercel production and local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=86400,
)

@app.middleware("http")
async def cors_preflight_override(request: Request, call_next):
    if request.method == "OPTIONS":
        response = Response(status_code=200)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, HEAD, PATCH"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Max-Age"] = "86400"
        return response

    try:
        response = await call_next(request)
    except Exception as exc:
        response = JSONResponse(
            status_code=500,
            content={"detail": f"Internal Engine Error: {str(exc)}"}
        )

    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.get("/")
@app.get("/health")
def health():
    return {
        "status": "HEALTHY",
        "service": "TraceGraph Sovereign Engine",
        "version": "v3.2.0"
    }

class TraceIncidentRequest(BaseModel):
    victim_identifier: Optional[str] = "VICTIM-9988776655"
    defrauded_amount: float = Field(..., gt=0)
    utr_reference: str
    source_bank_acc: str

@app.post("/api/v1/forensics/trace-incident")
async def trace_incident(payload: TraceIncidentRequest):
    siphoned = float(payload.defrauded_amount)
    
    mock_nodes = [
        {
            "id": payload.source_bank_acc,
            "name": f"Victim Account ({payload.victim_identifier})",
            "bank": "State Bank of India",
            "type": "ORIGIN_VICTIM",
            "layer": 0,
            "status": "DEPLETED",
            "balance": 12500.0,
            "allocated_lien": 0.0,
            "risk_score": 0.02
        },
        {
            "id": "MULE-L1-CANARA-991",
            "name": "Alok Traders (Primary Mule L1)",
            "bank": "Canara Bank",
            "type": "LAYER_1_MULE",
            "layer": 1,
            "status": f"LIEN_INR_{int(siphoned)}",
            "balance": siphoned,
            "allocated_lien": siphoned,
            "risk_score": 0.96
        },
        {
            "id": "MULE-L2-PAYTM-402",
            "name": "FastPay Reseller (Mule L2)",
            "bank": "Paytm Payments Bank",
            "layer": 2,
            "status": f"LIEN_INR_{int(siphoned * 0.54)}",
            "balance": round(siphoned * 0.54, 2),
            "allocated_lien": round(siphoned * 0.54, 2),
            "risk_score": 0.89
        },
        {
            "id": "MULE-L2-ICICI-118",
            "name": "Vortex Logistics Prop. (Mule L2)",
            "bank": "ICICI Bank",
            "layer": 2,
            "status": f"LIEN_INR_{int(siphoned * 0.46)}",
            "balance": round(siphoned * 0.46, 2),
            "allocated_lien": round(siphoned * 0.46, 2),
            "risk_score": 0.84
        },
        {
            "id": "ATM-ROHINI-SEC18",
            "name": "Terminal Cash-Out (Rohini Sector-18)",
            "bank": "National Switch Terminal",
            "type": "TERMINAL_CASH_OUT",
            "layer": 3,
            "status": "FIELD_DISPATCH_NOTIFIED",
            "balance": 0.0,
            "allocated_lien": 0.0,
            "risk_score": 0.99
        }
    ]

    mock_hops = [
        {
            "utr": payload.utr_reference,
            "from": payload.source_bank_acc,
            "to": "MULE-L1-CANARA-991",
            "amount": siphoned,
            "channel": "IMPS/FAST",
            "timestamp": int(time.time() - 3600)
        },
        {
            "utr": "UPI/2026/891022/PAYTM",
            "from": "MULE-L1-CANARA-991",
            "to": "MULE-L2-PAYTM-402",
            "amount": round(siphoned * 0.54, 2),
            "channel": "UPI/SMURF",
            "timestamp": int(time.time() - 3200)
        },
        {
            "utr": "RTGS/2026/891023/ICIC",
            "from": "MULE-L1-CANARA-991",
            "to": "MULE-L2-ICICI-118",
            "amount": round(siphoned * 0.46, 2),
            "channel": "RTGS/SPLIT",
            "timestamp": int(time.time() - 2800)
        },
        {
            "utr": "ATM/ROHINI/99201",
            "from": "MULE-L2-PAYTM-402",
            "to": "ATM-ROHINI-SEC18",
            "amount": round(siphoned * 0.54, 2),
            "channel": "CARDLESS_ATM_EXIT",
            "timestamp": int(time.time() - 2100)
        }
    ]

    hasher = hashlib.sha256()
    hasher.update(json.dumps({"case": payload.utr_reference, "volume": siphoned}).encode())

    return {
        "case_id": f"CFCFRMS-1930-{payload.utr_reference[-6:]}",
        "victim_account": payload.source_bank_acc,
        "siphoned_volume": siphoned,
        "lienable_volume": round(siphoned * 0.884, 2),
        "traversal_time_ms": 6.4,
        "sec_65b_digest": f"SHA256:{hasher.hexdigest()}",
        "nodes": mock_nodes,
        "hops": mock_hops
    }

@app.post("/api/v1/forensics/upload-statement")
async def upload_bank_statement():
    return {
        "records_parsed": 18,
        "message": "Annexure processed successfully. Multi-hop ledger synthesized.",
        "siphoned_identified": 850000.0
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
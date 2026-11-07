"""Fake eCourtsIndia server returning the response shapes documented at
ecourtsindia.com/api/docs (fields as listed there). For local tests only."""
from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse

app = FastAPI()
CNR = "DLCT010012342025"
CASE = {
    "courtCaseData": {
        "cnr": CNR, "caseNumber": "CS SCJ 1234/2025", "caseType": "CS", "caseTypeRaw": "CS SCJ - CIVIL SUIT (SENIOR CIVIL JUDGE)",
        "caseStatus": "PENDING", "disposalType": None, "decisionDate": None,
        "filingNumber": "5678/2025", "filingDate": "2025-02-10", "registrationNumber": "1234/2025", "registrationDate": "2025-02-14",
        "firstHearingDate": "2025-03-05", "lastHearingDate": "2026-10-08", "nextHearingDate": "2026-12-03",
        "purpose": "Plaintiff/Petitioner Evidence",
        "petitioners": ["Priya Sharma"], "respondents": ["Ramesh Gowda"],
        "petitionerAdvocates": ["A. K. Verma"], "respondentAdvocates": [],
        "judges": ["Senior Civil Judge, Saket"],
        "courtName": "Senior Civil Judge cum Rent Controller, Saket", "courtNo": "12", "district": "South", "state": "Delhi",
        "actsAndSections": "Code of Civil Procedure, 1908 Order 37",
        "historyOfCaseHearings": [
            {"judge": "Senior Civil Judge, Saket", "businessOnDate": "2025-03-05", "hearingDate": "2025-03-05", "purposeOfListing": "Appearance"},
            {"judge": "Senior Civil Judge, Saket", "businessOnDate": "2026-10-08", "hearingDate": "2026-10-08", "purposeOfListing": "Framing of issues"},
        ],
        "interimOrders": [{"orderDate": "2026-10-08", "description": "Order on framing of issues", "orderUrl": "order-2.pdf"},
                          {"orderDate": "2025-03-05", "description": "Summons issued", "orderUrl": "order-1.pdf"}],
        "judgmentOrders": [],
        "hasOrders": True, "hasJudgments": False,
    },
    "entityInfo": {"nextDateOfHearing": "2026-12-03"},
}
ORDER = """IN THE COURT OF SENIOR CIVIL JUDGE CUM RENT CONTROLLER, SAKET, NEW DELHI

CS SCJ No. 1234/2025
Priya Sharma ... Plaintiff
versus
Ramesh Gowda ... Defendant

ORDER
08.10.2026

Present: Counsel for the plaintiff. Defendant in person.

The defendant has filed his written statement. Arguments on framing of issues heard. From the pleadings, the following issues are framed:
1. Whether the plaintiff is entitled to recovery of Rs. 60,000/- towards the security deposit? OPP
2. Whether the defendant was entitled to deduct Rs. 25,000/- towards painting and damages? OPD
3. Relief.

The plaintiff is directed to file the list of witnesses within 15 days. Put up for plaintiff's evidence on 03.12.2026.

(Senior Civil Judge)"""


@app.get("/api/partner/case/{cnr}")
def case(cnr: str, authorization: str = Header("")):
    if not authorization.startswith("Bearer "):
        return JSONResponse({"error": {"code": "INVALID_TOKEN", "message": "bad"}}, status_code=401)
    if cnr == "XSSX010000012025":
        evil = "<img src=x onerror=window.__xss=1>"
        bad = {**CASE["courtCaseData"], "cnr": cnr, "petitioners": [evil + "Asha"], "respondents": ["<script>window.__xss=2</script>"],
               "judges": [evil], "courtName": evil, "actsAndSections": evil, "purpose": evil,
               "interimOrders": [{"orderDate": "2026-10-08", "description": evil, "orderUrl": "order-1.pdf"}],
               "historyOfCaseHearings": [{"hearingDate": "2026-10-08", "purposeOfListing": evil, "judge": evil}]}
        return {"data": {"courtCaseData": bad}, "meta": {}}
    if cnr != CNR:
        return JSONResponse({"error": {"code": "CASE_NOT_FOUND", "message": "Case with given CNR not found", "details": []}, "meta": {"request_id": "x"}}, status_code=404)
    return {"data": CASE, "meta": {"request_id": "r1"}}


@app.get("/api/partner/case/{cnr}/order-md/{filename}")
def order_md(cnr: str, filename: str):
    return {"data": {"markdownContent": ORDER, "pdfBase64": ""}, "meta": {"request_id": "r2"}}


@app.get("/api/partner/v2/search")
def search(litigants: str = ""):
    rows = [{"cnr": CNR, "caseType": "CS", "caseStatus": "PENDING", "filingDate": "2025-02-10", "nextHearingDate": "2026-12-03",
             "judges": [], "petitioners": ["Priya Sharma"], "respondents": ["Ramesh Gowda"], "courtCode": "DLCT01", "registrationNumber": "1234/2025"}] if "priya" in litigants.lower() else []
    return {"data": {"results": rows, "totalHits": len(rows), "page": 1, "pageSize": 10, "totalPages": 1, "hasNextPage": False, "facets": {}}, "meta": {"request_id": "r3"}}

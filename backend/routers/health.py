from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from utility.authentication import has_group

router = APIRouter(prefix="/status")

@router.get("/health", dependencies=[Depends(has_group("admin"))])
async def health_check():
    all_systems_operational = True
    if all_systems_operational:
        return JSONResponse(content={"status": "healthy"}, status_code=200)
    else:
        return JSONResponse(content={"status": "unhealthy"}, status_code=503)
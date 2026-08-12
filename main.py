import hmac

from fastapi import FastAPI

# openssl rand -base64 1000
SECRET = """
7TH2VK3nfiWeVgQNJ1kOT08CX5NVTimtTGW9Go4MVfradNOtPdp2RIBJcERkGRlJ
rTN7DuJzTGBuA8yF/86l45Uqyt9Z7goKgJ5ie/yOIYQWoCC2wjlAdlzbU1HliWus
g0pkXangi+sRpDxR8+LWBRyojIb0q5CYUhHf66i/GyZQtklOa4LEEo5MZ7qbU1sJ
+xYE5lWGVdRSxDK2pF2TNx6YjAYFz6MyReAi2Caw9gRPrZL2XWb1wtzgsAPfzpJq
eMPrpsQ2h6Fwkuf5T7uaGVjAa3xd6eEovMUuOLudnhmgWiXn3PHywExhJAg4lL4D
E8lcwsybUkz6UvqqpE/PMMgIvtQHrVfJnuMCHlgvH7ApYPU83Syxixr1ZfpcQXuR
hN884EMvB8Q3pSEQIytPJNu4Nw6+iLhifVFnadt1v2laX0I4bnxo8Bk2oIP8T5aP
Wl+cVqTZzAeogf0I1d+5uDo1X1f0iYY9xqd1Q99M+leQcdF+I0DqpEMdHYaRFlxY
Ub+rOvih6P2lsHCAO0X8h2MECHQ53AT+p3RWFTXhlHRO1URIem1Yv5Z2MG3+6Xe2
FLOyxGNIY7SawAdi3wLqT1ek+sVUNJpXVj7C/BqVpb7NqKQ2sw6EIBeUdKZKU2VS
GxfwwyhGKJzTWDmxWhGY6dptMKTpunFrEXUD0idjWsq3zlJB+k4NxboLMuwZLauO
PqXhZnmyOpSrXwtLtPka3JGxUYGETLeHzNrSblz/2Nvgv8tDCeXQTh8T7uuxKmER
l5fe6ZIl2YwCSglO1oyTB+qhs8cJWew+7SSq0s+8kLM5vynY6kbedDZ3/dugpshF
KsoeYuy6w4AsXWmcc6Ao5NldvQFMFjtLIiQplsgd38Mr57mVy/fWtqW4bqvY88ex
cY+fstTAdSzRNTJ81ZyY1WkArv6aNWfgp2HjpFdRPQ7DaOgKxZlPiRIQxqY1hT30
UL1uU/SShq9/avC33pyfM7XdxEYADmrfAh7QfI6NkOUgphGR+AoBqWchQB9gxi4D
fOFPgM+JdDuQ/N4K6bGdLqwVL8hFLaURjbx1cwGhHCY+cqJezXkiV7G6WKeY6UJf
S/wwwxVI3JdI6f5+bsDXs8X/DlWVnI7WVqr0NahomT+dRYXqn+D9M+NJrVrKU1d5
gScSVYOXFSFCa/2ZgEPJZYHxa09J0DYwRBPTmUiERQ868XCfFeTBaDLk0KZZFPEq
kf9Aj9/t5LZSGm7W3bCuicb+xUXa5+1WpY2nYfroORMwxCaC/auiE57KjTedn8D5
ir47nOGbQzHBn2X/afNqdlvSD69G2q0fgG3azTKQ65F85wBVEJ2Fgg==
""".strip()

app = FastAPI()


@app.get("/compare")
async def compare(request_value: str):
    return request_value == SECRET


@app.get("/compare-digest")
async def compare_digest(request_value: str):
    return hmac.compare_digest(request_value, SECRET)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

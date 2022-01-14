import uuid
import os

from simplex import SimplexSolver

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import pypandoc

OUTPUT_PATH = "output"


class CoolSolver(SimplexSolver):
    def print_doc(self):
        if not self.gen_doc:
            return
        self.doc += (r"\end{document}")


class SolveRequest(BaseModel):
    equations: list[list[float]]
    c: list[float]
    p: str


os.makedirs(OUTPUT_PATH, exist_ok=True)

app = FastAPI()

app.mount("/ui", StaticFiles(directory="ui"), name="ui")
app.mount("/output", StaticFiles(directory=OUTPUT_PATH), name="output")

@app.post("/solve")
def solve(params: SolveRequest):
    handle = uuid.uuid4().hex + ".pdf"
    lpath = os.path.join(OUTPUT_PATH, handle)
    rpath = f"/output/{handle}"

    # | 1 2 5 |
    # | 3 4 6 |
    # should become
    # | 1 2 |
    # | 3 4 |
    # and
    # | 5 |
    # | 6 |
    A = []
    b = []
    for row in params.equations:
        A.append(row[0:-1])
        b.append(row[-1])

    solver = CoolSolver()
    solver.run_simplex(A, b, params.c, prob=params.p, enable_msg=False, latex=True)
    pypandoc.convert_text(solver.doc, 'pdf', format="latex", outputfile=lpath)

    return {"path": rpath}

@app.get("/", response_class=RedirectResponse)
def root():
    return "/ui/index.html"

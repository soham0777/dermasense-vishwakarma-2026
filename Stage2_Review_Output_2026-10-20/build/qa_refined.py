"""
QA of the refined deck, measured by Microsoft PowerPoint (reuses 1_presentation/qa_deck.py read-only).
Differences from the original: paths point to this folder, and PowerPoint is never quit while the user still has a
presentation or a Protected View window open (the team often has the template open).
Writes ../Vishwakarma_Stage2_Refined.pdf (exported from the saved PPTX), qa_results.json here, PNG renders to renders/.
"""
import sys
from pathlib import Path

import win32com.client

HERE = Path(__file__).resolve().parent
OUTDIR = HERE.parent
sys.path.insert(0, str(OUTDIR.parent / "1_presentation"))
import qa_deck as Q  # noqa: E402

Q.DECK = OUTDIR / "Vishwakarma_Stage2_Refined.pptx"
Q.PDF = OUTDIR / "Vishwakarma_Stage2_Refined.pdf"
Q.OUT = HERE / "qa_results.json"
Q.RENDER = HERE / "renders"


class SafeApp:
    """Wraps the PowerPoint COM object; Quit() only when nothing of the user's is open."""

    def __init__(self, app):
        object.__setattr__(self, "_app", app)

    def __getattr__(self, name):
        return getattr(self._app, name)

    def __setattr__(self, name, value):
        setattr(self._app, name, value)

    def Quit(self):
        still_open = self._app.Presentations.Count + self._app.ProtectedViewWindows.Count
        if still_open == 0:
            self._app.Quit()
        else:
            print(f"PowerPoint left running: {still_open} of the user's window(s) open")


_dispatch = win32com.client.DispatchEx
win32com.client.DispatchEx = lambda prog: SafeApp(_dispatch(prog))

if __name__ == "__main__":
    Q.main()

## Math Tutor using CrewAI

---

### Setup local environment using miniconda

- Install: [miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install)
  - Create a new environment: `conda create -n math_tutor python=3.12`
  - Choose your Python Interpreter, in this case: `math_tutor (conda env)`
- Install `uv`: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Install `crewai` CLI: `uv tool install crewai`

### Run Math Tutor
- Remember to add your `GEMINI_API_KEY` into `.env`
  - e.g: `GEMINI_API_KEY=your_gemini_api_key`
- Run `crewai install`
- Start `crewai flow kickoff`
  - Input your question or absolute image path:
    - e.g:
      - Input your question: `(+7) - (+1)`
      - Input your question: `/your/absolute/image/path.png`
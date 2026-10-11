# Publish to GitHub (Windows / VS Code)

1. Create a **public empty** repository named `ai-identity-access-governance` at https://github.com/new. Do not initialize with a README.
2. Extract this ZIP, open the inner `ai-identity-access-governance` folder in VS Code, and open **Terminal → New Terminal**.
3. Run `python -m venv .venv`, then `.venv\Scripts\Activate.ps1` and `python -m pip install -r requirements.txt`.
4. Run `python -m pytest -q` and `python -m src.pipeline` before publishing.
5. Run:

```powershell
git init
git branch -M main
git add .
git commit -m "Build synthetic identity governance analytics demo"
git remote add origin https://github.com/mannsinha1902/ai-identity-access-governance.git
git push -u origin main
```

If `origin` already exists, use `git remote set-url origin https://github.com/mannsinha1902/ai-identity-access-governance.git` instead. If Git asks for your identity, configure `git config --global user.name "Your Name"` and `git config --global user.email "your-email@example.com"`.

6. Verify `README.md`, `src/`, `tests/`, `sql/`, and the green GitHub Actions workflow appear online. Add screenshots from the locally running Streamlit app to `docs/` and reference them in the README.

**Security:** Never commit real customer or employee identities, API keys, `.env`, or the local SQLite database.

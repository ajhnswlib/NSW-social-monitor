# NSW Liberal new-candidate public social monitor

## Run

```bash
pip install -r requirements.txt
python app.py
```
Open http://localhost:8000 . For hosting, run `gunicorn app:app --bind 0.0.0.0:$PORT` on a Python hosting service.

## Important limits

- No login, so anyone with the hosted URL can access it. `robots.txt` does not provide privacy.
- The starter roster comes from the publicly indexed NSW Liberal state candidate directory, and **is not verified as an exhaustive list of all new candidates**.
- At runtime the backend checks candidate profile URLs and extracts external social media links **only if they are actually present on the page**. The inferred slug may be wrong; errors are explicitly shown.
- This is a **working public-profile discovery dashboard**, not a fully functioning real-time Facebook/Instagram post scraper. Free anonymous access to those post feeds is generally restricted. Posts remain empty until a legitimate accessible feed is integrated. Never infer inactivity from missing posts.
- The frontend polls every two minutes, but backend profile checks are cached for 15 minutes.
- Do not bypass platform rate limits, login requirements or access controls.

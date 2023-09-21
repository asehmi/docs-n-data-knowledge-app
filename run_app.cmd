@echo off
echo ============================================================
echo === OPEN A BROWSER WINDOW AT "http://[ip-address]:6974/" ===
echo ============================================================
streamlit run --server.port=6974 --server.headless=false app.py %1 %2 %3 %4 %5 %6 %7 %8 %9

# Minimal reproducible example for empty downloaded pdf

The bug of downloading or sharing a pdf file but getting an empty file is a 
long-standing issue in firefox-ios, as mentioned in the following issues:
- https://github.com/mozilla-mobile/firefox-ios/issues/14053
- https://github.com/mozilla-mobile/firefox-ios/issues/11318
- https://github.com/mozilla-mobile/firefox-ios/issues/21845
- https://github.com/mozilla-mobile/firefox-ios/issues/20688
- ...

This repo provide a minimal reproducible example for a case for this issue.

## Reproduce steps
1. Install `flask` with `pip install flask`
2. Run the server with `python main.py`, and a server will be started at
    `http://localhost:7788`
3. Open the link in firefox-ios, and login with the username `admin` and password
    `password123`
4. Click the download button to download the pdf file

### Expected behavior
The pdf file should be downloaded successfully and can be opened with any pdf
viewer.

### Actual behavior
The downloaded pdf file is show in `results/test.pdf`. And if we open it as text
file, we can see that the content is actually the login page of the server.

## Possible reasons
The issue is likely caused by the authentication information is not passed when
downloading or sharing a pdf file in firefox-ios.
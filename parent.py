import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import settings

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    html = """
        <html>
            <head>
                <title>Parent page</title>
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
                <script>
                    document.cookie = "some_test_cookie=true;";

                    function ready() {
                        var theCookies = document.cookie.split(';');
                        var aString = '';
                        for (var i = 1 ; i <= theCookies.length; i++) {
                            aString += i + ' | ' + theCookies[i-1] + "<br>";
                        }
                        var cookie_list = document.getElementById('cookie-list');
                        cookie_list.innerHTML = aString;
                    }

                    document.addEventListener("DOMContentLoaded", ready);
                </script>
            </head>
            <body>
                <h1>Parent page</h1>
    """
    html += f"""
        <iframe id="iFrameExample"
            title="Inline Frame Example"
            src="{settings.child_url}/get_login_form">
        </iframe>
    """
    html += """
        <div id="cookie-list" style="margin: 16px;"></div>

        <script>
            const childWindow = document.getElementById('iFrameExample').contentWindow;
            window.addEventListener('message', ({ data }) => {
              console.log('i got some data!', data); // i got some data! hi!
            });
        </script>
        </body>
        </html>
    """
    return html


if __name__ == "__main__":
    uvicorn.run("parent:app", host="0.0.0.0", port=8000, reload=True)

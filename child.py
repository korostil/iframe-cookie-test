import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse, JSONResponse
import settings

app = FastAPI()


@app.get("/get_login_form", response_class=HTMLResponse)
async def read_login_form():
    html = """
        <html>
            <head>
                <title>Child page</title>
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
                <script>
                    document.cookie = "SameSite=None; Secure";

                    function success() {
                        console.log('postMessage');

                        window.parent.postMessage({
                          action: 'login',
                          login: 'userLogin',
                          success: true
                        }, '*');
                    };
                </script>
            </head>
            <body>
    """
    html += f"""
        <form id="myform" method="post" action="{settings.child_url}/login" onsubmit="success();">
            <div style="padding: 8px 16px;">
                <input type="text" id="password" name="username" placeholder="Username">
            </div>
            <div style="padding: 8px 16px;">
                <input type="text" id="password" name="password" placeholder="Password">
            </div>
            <div style="padding: 8px 16px;">
                <input type="submit" value="Sign in">
            </div>
        </form>
        </body>
        </html>
    """
    return html


@app.post("/login")
async def login(request: Request):
    print('request:', request)
    # if username == 'admin':
    #     return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST)

    response = JSONResponse(content={"message": "successful"})
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return response


if __name__ == "__main__":
    uvicorn.run("child:app", host="0.0.0.0", port=8001, reload=True)

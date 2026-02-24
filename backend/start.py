import uvicorn

# Run the FastAPI application using Uvicorn
# which is an ASGI server for Python.
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
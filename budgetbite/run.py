from app import create_app

app = create_app()

if __name__ == "__main__":
    # debug=True gives auto-reload + tracebacks while you're building.
    # Turn it off before deploying anywhere.
    app.run(debug=True)

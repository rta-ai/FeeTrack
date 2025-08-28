from app import app

if __name__ == '__main__':
    # Run on localhost only, no auto-reloader, no debug mode
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

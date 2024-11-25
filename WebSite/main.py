from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='63.176.135.154', port=5000, debug=True)
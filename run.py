from app import create_app, sk

if __name__ == '__main__':
    app = create_app()
    sk.run(app, debug=False, host="0.0.0.0", port=8080)

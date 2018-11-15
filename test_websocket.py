img_files = [
    "images/bike.jpg",
    "images/cat.jpg",
    "images/pen.jpg",
    "images/sneakers.jpg",
    "images/tiger.jpg"
]

idx = 0

def update_data(client):
    global img_files
    global idx
    with open(img_files[idx], "rb") as file:
        img = file.read()
    img_b64 = base64.b64encode(img).decode()
    client.send_data(img_b64)
    idx = (idx + 1) % len(img_files)
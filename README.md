# Internet Clipboard 📋

A lightweight, self-hosted, "burn-after-reading" pastebin inspired by cl1p.net. 

Securely share text, snippets, secrets, and small files. Data is stored entirely in memory and is **instantly destroyed** the moment it is read by the recipient.

## ✨ Features
* **Burn-After-Reading:** No databases, no persistent storage, and no volume permission errors. Data lives in RAM and is wiped upon the first read.
* **File Uploads:** Securely attach files up to 16MB. Files are Base64 encoded and embedded directly into the delivery payload, ensuring nothing is ever written to disk.
* **Custom URLs:** You dictate the URL. Just navigate to `yourdomain.com/whatever-you-want` to start typing.
* **Modern Dark Theme:** A sleek, high-contrast dark UI that is easy on the eyes.
* **Docker Native:** Instantly deployable via Docker and Docker Compose.

## 🚀 Quick Start (Deploying via Docker Hub)

If you just want to run the application on your server, you don't need to clone this repository. You can use the pre-built image.

1. Create a `docker-compose.yml` file:

```yaml
services:
  internet-clipboard:
    image: hanafytech/internet-clipboard:latest
    container_name: internet-clipboard
    restart: always
    ports:
      - "8080:8080"
```

2. Run the container:

```bash
docker compose up -d
```

3. Route your domain (e.g., using Cloudflare Tunnels) to `http://<your-host-ip>:8080`.

## 🛠️ Local Development & Building from Source

If you want to modify the code, change the theme, or build the image yourself:

1. Clone the repository:

```bash
git clone [https://github.com/hanafytech/internet-clipboard.git](https://github.com/hanafytech/internet-clipboard.git)
cd internet-clipboard
```

2. Build and run using Docker Compose:

```bash
docker compose up -d --build
```

## 📝 How to Use
1. Navigate to your deployed domain (e.g., `https://share.yourdomain.com`).
2. Add a custom path to the URL (e.g., `https://share.yourdomain.com/secret123`).
3. Type your message and/or attach a file (Max 16MB) and click **Save**.
4. Send the exact URL to your recipient. 
5. Once they open the link, the data is displayed/downloaded and permanently deleted from the server. Refreshing the page will show an error/empty box.

## 💻 Tech Stack
* **Backend:** Python, Flask, Gunicorn (Production Server)
* **Frontend:** HTML5, CSS3 (Jinja2 Templating)
* **Containerization:** Docker
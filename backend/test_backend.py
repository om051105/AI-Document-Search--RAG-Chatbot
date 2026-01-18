import requests
import os

def test_api():
    url = "http://localhost:8000"
    
    # 1. Test Root
    try:
        r = requests.get(f"{url}/")
        print(f"Root endpoint: {r.status_code} - {r.json()}")
    except Exception as e:
        print(f"Root endpoint failed: {e}")
        return

    # 2. Test Upload (Mock PDF)
    with open("test.pdf", "wb") as f:
        f.write(b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/Resources <<\n/Font <<\n/F1 4 0 R\n>>\n>>\n/MediaBox [0 0 612 792]\n/Contents 5 0 R\n>>\nendobj\n4 0 obj\n<<\n/Type /Font\n/Subtype /Type1\n/BaseFont /Helvetica\n>>\nendobj\n5 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 24 Tf\n100 100 Td\n(Hello World) Tj\nET\nendstream\nendobj\nxref\n0 6\n0000000000 65535 f\n0000000010 00000 n\n0000000060 00000 n\n0000000117 00000 n\n0000000259 00000 n\n0000000346 00000 n\ntrailer\n<<\n/Size 6\n/Root 1 0 R\n>>\nstartxref\n439\n%%EOF")

    files = {'file': open('test.pdf', 'rb')}
    try:
        print("Uploading test.pdf...")
        r = requests.post(f"{url}/upload", files=files)
        print(f"Upload endpoint: {r.status_code}")
        if r.status_code != 200:
            print(f"Error details: {r.text}")
        else:
            print(f"Success: {r.json()}")
    except Exception as e:
        print(f"Upload failed: {e}")
    finally:
        files['file'].close()
        os.remove("test.pdf")

if __name__ == "__main__":
    test_api()

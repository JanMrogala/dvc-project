from google_drive_manager import GoogleDriveFolder

# Use the shared drive ID as your folder_id
folder = GoogleDriveFolder(
    credentials_path="gdrive_limited_creds.json",
    folder_id="0AEMKKkJU9QwQUk9PVA",  # Shared drive ID
    use_shared_drive=True
)

# file_id = folder.upload_file("test.txt")
# List all shared drives you have access to
results = folder.drives().list().execute()
for drive in results.get('drives', []):
    print(f"Name: {drive['name']}, ID: {drive['id']}")
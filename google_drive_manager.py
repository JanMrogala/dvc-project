# gdrive_folder.py
import os
import io
import mimetypes
from typing import List, Dict, Optional, Union
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload, MediaIoBaseUpload

class GoogleDriveFolder:
    """
    A library for managing files in a specific Google Drive folder.
    Provides full CRUD operations: Create, Read, Update, Delete.
    """
    
    def __init__(self, credentials_path: str, folder_id: str, use_shared_drive: bool = True):
        """
        Initialize the Google Drive folder manager.
        
        Args:
            credentials_path: Path to service account JSON file
            folder_id: ID of the Google Drive folder to manage
        """
        self.folder_id = folder_id
        self.service = self._authenticate(credentials_path)
        self._verify_folder_access()
        self.use_shared_drive = True
    
    def _authenticate(self, credentials_path: str):
        """Authenticate with Google Drive API."""
        if not os.path.exists(credentials_path):
            raise FileNotFoundError(f"Credentials file not found: {credentials_path}")
        
        # Full access scopes for CRUD operations
        scopes = ['https://www.googleapis.com/auth/drive']
        
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path, scopes=scopes
        )
        return build('drive', 'v3', credentials=credentials)
    
    def _verify_folder_access(self):
        """Verify we can access the target folder."""
        try:
            folder = self.service.files().get(
                fileId=self.folder_id,
                fields='id, name, mimeType'
            ).execute()
            
            if folder.get('mimeType') != 'application/vnd.google-apps.folder':
                raise ValueError(f"ID {self.folder_id} is not a folder")
                
        except HttpError as e:
            if e.resp.status == 404:
                raise ValueError(f"Folder {self.folder_id} not found or no access")
            raise
    
    # READ operations
    def list_files(self, include_folders: bool = True) -> List[Dict]:
        """
        List all files in the folder.
        
        Args:
            include_folders: Whether to include subfolders in results
            
        Returns:
            List of file dictionaries with id, name, mimeType, size, etc.
        """
        query = f"'{self.folder_id}' in parents and trashed=false"
        if not include_folders:
            query += " and mimeType != 'application/vnd.google-apps.folder'"
        
        try:
            results = self.service.files().list(
                q=query,
                fields="files(id, name, mimeType, size, modifiedTime, createdTime, webViewLink)",
                orderBy="name"
            ).execute()
            
            return results.get('files', [])
            
        except HttpError as e:
            raise Exception(f"Failed to list files: {e}")
    
    def get_file_info(self, file_id: str) -> Dict:
        """
        Get detailed information about a specific file.
        
        Args:
            file_id: Google Drive file ID
            
        Returns:
            Dictionary with file information
        """
        try:
            return self.service.files().get(
                fileId=file_id,
                fields="id, name, mimeType, size, modifiedTime, createdTime, webViewLink, parents"
            ).execute()
        except HttpError as e:
            raise Exception(f"Failed to get file info: {e}")
    
    def search_files(self, search_term: str) -> List[Dict]:
        """
        Search for files by name in the folder.
        
        Args:
            search_term: Term to search for in file names
            
        Returns:
            List of matching files
        """
        query = f"'{self.folder_id}' in parents and name contains '{search_term}' and trashed=false"
        
        try:
            results = self.service.files().list(
                q=query,
                fields="files(id, name, mimeType, size, modifiedTime)"
            ).execute()
            
            return results.get('files', [])
            
        except HttpError as e:
            raise Exception(f"Failed to search files: {e}")
    
    def download_file(self, file_id: str, destination_path: Optional[str] = None) -> bytes:
        """
        Download a file from the folder.
        
        Args:
            file_id: Google Drive file ID
            destination_path: Local path to save file (optional)
            
        Returns:
            File content as bytes
        """
        try:
            # Get file info for the name
            file_info = self.get_file_info(file_id)
            
            # Download the file
            request = self.service.files().get_media(fileId=file_id)
            file_content = io.BytesIO()
            downloader = MediaIoBaseDownload(file_content, request)
            
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            
            file_bytes = file_content.getvalue()
            
            # Save to file if path provided
            if destination_path:
                with open(destination_path, 'wb') as f:
                    f.write(file_bytes)
            
            return file_bytes
            
        except HttpError as e:
            raise Exception(f"Failed to download file: {e}")
    
    # CREATE operations
    def upload_file(self, file_path: str, drive_filename: Optional[str] = None) -> str:
        """
        Upload a file to the folder.
        
        Args:
            file_path: Local path to file to upload
            drive_filename: Name to use in Drive (optional, uses original name)
            
        Returns:
            File ID of uploaded file
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Local file not found: {file_path}")
        
        filename = drive_filename or os.path.basename(file_path)
        mime_type, _ = mimetypes.guess_type(file_path)
        
        file_metadata = {
            'name': filename,
            'parents': [self.folder_id]
        }
        
        try:
            media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name'
            ).execute()
            
            return file.get('id')
            
        except HttpError as e:
            raise Exception(f"Failed to upload file: {e}")
    
    def upload_content(self, content: Union[str, bytes], filename: str, mime_type: Optional[str] = None) -> str:
        """
        Upload content directly to the folder.
        
        Args:
            content: String or bytes content to upload
            filename: Name for the file in Drive
            mime_type: MIME type (optional, will guess from filename)
            
        Returns:
            File ID of created file
        """
        if not self.use_shared_drive:
            raise Exception("Cannot upload to personal Drive folders with service accounts. Use a Shared Drive instead.")
        
        if isinstance(content, str):
            content = content.encode('utf-8')
        
        if not mime_type:
            mime_type, _ = mimetypes.guess_type(filename)
            mime_type = mime_type or 'application/octet-stream'
        
        file_metadata = {
            'name': filename,
            'parents': [self.folder_id]
        }
        
        try:
            media = MediaIoBaseUpload(
                io.BytesIO(content),
                mimetype=mime_type,
                resumable=True
            )
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name',
                supportsAllDrives=True
            ).execute()
            
            return file.get('id')
            
        except HttpError as e:
            if "storage quota" in str(e).lower():
                raise Exception("Service accounts cannot upload to personal Drive folders. Please use a Shared Drive instead.")
            raise Exception(f"Failed to upload content: {e}")
    
    def create_subfolder(self, folder_name: str) -> str:
        """
        Create a subfolder within the managed folder.
        
        Args:
            folder_name: Name for the new folder
            
        Returns:
            Folder ID of created folder
        """
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [self.folder_id]
        }
        
        try:
            folder = self.service.files().create(
                body=file_metadata,
                fields='id, name'
            ).execute()
            
            return folder.get('id')
            
        except HttpError as e:
            raise Exception(f"Failed to create folder: {e}")
    
    # UPDATE operations
    def rename_file(self, file_id: str, new_name: str) -> bool:
        """
        Rename a file in the folder.
        
        Args:
            file_id: Google Drive file ID
            new_name: New name for the file
            
        Returns:
            True if successful
        """
        try:
            self.service.files().update(
                fileId=file_id,
                body={'name': new_name}
            ).execute()
            return True
            
        except HttpError as e:
            raise Exception(f"Failed to rename file: {e}")
    
    def update_file_content(self, file_id: str, new_content: Union[str, bytes], mime_type: Optional[str] = None) -> bool:
        """
        Update the content of an existing file.
        
        Args:
            file_id: Google Drive file ID
            new_content: New content for the file
            mime_type: MIME type (optional)
            
        Returns:
            True if successful
        """
        if isinstance(new_content, str):
            new_content = new_content.encode('utf-8')
        
        if not mime_type:
            # Try to get existing mime type
            file_info = self.get_file_info(file_id)
            mime_type = file_info.get('mimeType', 'application/octet-stream')
        
        try:
            media = MediaIoBaseUpload(
                io.BytesIO(new_content),
                mimetype=mime_type,
                resumable=True
            )
            
            self.service.files().update(
                fileId=file_id,
                media_body=media
            ).execute()
            return True
            
        except HttpError as e:
            raise Exception(f"Failed to update file content: {e}")
    
    def replace_file(self, file_id: str, new_file_path: str) -> bool:
        """
        Replace an existing file with a new local file.
        
        Args:
            file_id: Google Drive file ID to replace
            new_file_path: Path to new file
            
        Returns:
            True if successful
        """
        if not os.path.exists(new_file_path):
            raise FileNotFoundError(f"Replacement file not found: {new_file_path}")
        
        mime_type, _ = mimetypes.guess_type(new_file_path)
        
        try:
            media = MediaFileUpload(new_file_path, mimetype=mime_type, resumable=True)
            
            self.service.files().update(
                fileId=file_id,
                media_body=media
            ).execute()
            return True
            
        except HttpError as e:
            raise Exception(f"Failed to replace file: {e}")
    
    # DELETE operations
    def delete_file(self, file_id: str, permanent: bool = False) -> bool:
        """
        Delete a file from the folder.
        
        Args:
            file_id: Google Drive file ID
            permanent: If True, permanently delete. If False, move to trash.
            
        Returns:
            True if successful
        """
        try:
            if permanent:
                self.service.files().delete(fileId=file_id).execute()
            else:
                # Move to trash
                self.service.files().update(
                    fileId=file_id,
                    body={'trashed': True}
                ).execute()
            return True
            
        except HttpError as e:
            raise Exception(f"Failed to delete file: {e}")
    
    def restore_file(self, file_id: str) -> bool:
        """
        Restore a file from trash.
        
        Args:
            file_id: Google Drive file ID
            
        Returns:
            True if successful
        """
        try:
            self.service.files().update(
                fileId=file_id,
                body={'trashed': False}
            ).execute()
            return True
            
        except HttpError as e:
            raise Exception(f"Failed to restore file: {e}")
    
    def empty_trash(self) -> bool:
        """
        Permanently delete all trashed files in the folder.
        
        Returns:
            True if successful
        """
        try:
            # Find trashed files in this folder
            query = f"'{self.folder_id}' in parents and trashed=true"
            results = self.service.files().list(q=query, fields="files(id)").execute()
            trashed_files = results.get('files', [])
            
            # Permanently delete each trashed file
            for file in trashed_files:
                self.service.files().delete(fileId=file['id']).execute()
            
            return True
            
        except HttpError as e:
            raise Exception(f"Failed to empty trash: {e}")
    
    # UTILITY methods
    def get_folder_info(self) -> Dict:
        """Get information about the managed folder."""
        return self.get_file_info(self.folder_id)
    
    def get_storage_usage(self) -> Dict:
        """
        Get storage usage statistics for the folder.
        
        Returns:
            Dictionary with file count, total size, etc.
        """
        files = self.list_files(include_folders=False)
        
        total_size = 0
        file_count = len(files)
        
        for file in files:
            size = file.get('size')
            if size and size.isdigit():
                total_size += int(size)
        
        return {
            'file_count': file_count,
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'total_size_gb': round(total_size / (1024 * 1024 * 1024), 3)
        }


# Example usage and testing
def example_usage():
    """Example of how to use the GoogleDriveFolder library."""
    
    # Initialize the folder manager
    folder = GoogleDriveFolder(
        credentials_path="gdrive_limited_creds.json",
        folder_id="your_folder_id_here"
    )
    
    # READ: List files
    files = folder.list_files()
    print(f"Found {len(files)} files")
    
    # CREATE: Upload a file
    # file_id = folder.upload_file("local_file.txt")
    
    # CREATE: Upload content directly
    # file_id = folder.upload_content("Hello World!", "test.txt", "text/plain")
    
    # UPDATE: Rename a file
    # folder.rename_file(file_id, "new_name.txt")
    
    # UPDATE: Update content
    # folder.update_file_content(file_id, "Updated content!")
    
    # DELETE: Move to trash
    # folder.delete_file(file_id)
    
    # GET: Storage stats
    stats = folder.get_storage_usage()
    print(f"Folder contains {stats['file_count']} files, {stats['total_size_mb']} MB")

if __name__ == "__main__":
    example_usage()
import dropbox

# Ersetze dies mit deinem Zugangstoken von Dropbox
ACCESS_TOKEN = 'YOUR_DROPBOX_ACCESS_TOKEN'

def upload_to_dropbox(content, filename):
    dbx = dropbox.Dropbox(ACCESS_TOKEN)
    dbx.files_upload(content.encode(), f'/calendar/{filename}', mode=dropbox.files.WriteMode.overwrite)

def download_from_dropbox(filename):
    dbx = dropbox.Dropbox(ACCESS_TOKEN)
    metadata, res = dbx.files_download(f'/calendar/{filename}')
    return res.content.decode()

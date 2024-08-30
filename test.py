from google.cloud import storage

def list_buckets():
    """Lists all buckets."""
    storage_client = storage.Client()
    buckets = storage_client.list_buckets()

    print("Buckets:")
    for bucket in buckets:
        print(bucket.name)

if __name__ == "__main__":
    try:
        list_buckets()
        print("Authentication successful!")
    except Exception as e:
        print(f"Authentication failed. Error: {e}")
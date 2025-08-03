import unzip_http
from sys import argv
from os import environ

def setOutput(key, value):
    """Set the output for GitHub Actions."""
    output = environ.get("GITHUB_OUTPUT")
    if output:
        with open(environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"{key}={value}\n")
    print(f"setOutput: {key}={value}") # Print the output


# Get medadata
url = argv[1]
print("Extracting metadata from:", url)
rzf = unzip_http.RemoteZipFile(url)
metadata_text = rzf.open_text('META-INF/com/android/metadata').read()
print("META-INF/com/android/metadata:")
print(metadata_text)

# Parse metadata
metadata = {}
for line in metadata_text.splitlines():
    key, value = line.split("=", maxsplit=1)
    if key and value:
        metadata[key.strip()] = value.strip()
print("Parsed metadata:")
print(metadata)

# Generate release note
metadata_md = ""
for k, v in metadata.items():
    metadata_md += f"- `{k}`: {v}\n"

note = f"""## Metadata

{metadata_md}"""

with open("output/note.md", "w") as f:
    f.write(note)

# Set output for later use
version_name = metadata["version_name"]
if metadata["product_name"] == "CPH2653EEA": # EU
    version_name += "(EU)"
elif metadata["product_name"] == "CPH2653":
    version_name += "(GLO)"
setOutput("version_name", version_name)

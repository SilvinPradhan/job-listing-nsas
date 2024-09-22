# Function to split long messages into chunks of 2000 characters
def split_message(content, limit=2000):
    # Split content into chunks of <= limit
    lines = content.split("\n")
    chunks = []
    current_chunk = ""

    for line in lines:
        if len(current_chunk) + len(
                line) + 1 > limit:  # +1 for the newline character
            chunks.append(current_chunk)
            current_chunk = line
        else:
            current_chunk += "\n" + line if current_chunk else line

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

# Function to build the pagination footer for users
def pagination_footer(current_page, total_pages):
    return f"Page {current_page}/{total_pages}"
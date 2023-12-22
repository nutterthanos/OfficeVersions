import re

# Read the script content from the file
with open("versions.py", "r") as script_file:
    script = script_file.read()

# Define the increment value for start_build and end_build
build_increment = 100

# Define the pattern to find the start_build and end_build lines
pattern_start_build = r"(start_build\s*=\s*)(\d+)"
match_start_build = re.search(pattern_start_build, script)
if match_start_build:
    # Extract the original value and calculate the new value
    original_start_build = int(match_start_build.group(2))
    new_start_build = original_start_build + build_increment

    # Replace the original line with the updated line
    updated_line_start_build = f"{match_start_build.group(1)}{new_start_build}"
    script = re.sub(pattern_start_build, updated_line_start_build, script)

# Repeat the process for end_build
pattern_end_build = r"(end_build\s*=\s*)(\d+)"
match_end_build = re.search(pattern_end_build, script)
if match_end_build:
    original_end_build = int(match_end_build.group(2))
    new_end_build = original_end_build + build_increment
    updated_line_end_build = f"{match_end_build.group(1)}{new_end_build}"
    script = re.sub(pattern_end_build, updated_line_end_build, script)

# Write the updated script back to the file
with open("versions.py", "w") as script_file:
    script_file.write(script)
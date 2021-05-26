import frontmatter
import json
import os
from glob import glob

path = '/home/pietro/.nb/politica/*.md'
output = 'out.html'

nodes = []
indexes = {}

for filename in glob(path):
    with open(filename, 'r') as file:
        directory = os.path.dirname(filename)
        filename = os.path.basename(filename)

        # Parse the file and it's metadata
        metadata, content = frontmatter.parse(file.read())

        # Read the index file to determine this file's id
        if directory not in indexes:
            with open(os.path.join(directory, '.index'), 'r') as index:
                indexes[directory] = index.read()
        # Now find the line where this file belongs
        file_id = indexes[directory].splitlines().index(filename) + 1

        # Find a line with only hashtags
        tags = []
        for line in content.splitlines():
            isTagLine = True
            segments = line.split(' ')
            for segment in segments:
                if len(segment) <= 1 or segment[0] != '#':
                    isTagLine = False
                    break

            if isTagLine:
                tags = segments
                break

        # Find a title
        title = filename
        if 'title' in metadata:
            title = metadata['title']
            del metadata['title']

        nodes.append({
            'title': title,
            'nbIndex': file_id,
            'filename': filename,
            'metadata': metadata,
            'content': content,
            'tags': tags,
        })

with open('index.html', 'r') as html:
    content = html.read()

    content = content.replace('/* __DATA_DECLARATION__ */', f'var data = {json.dumps(nodes)};')

    with open(output, 'w') as out:
        out.write(content)
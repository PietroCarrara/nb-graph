import frontmatter
import json
from glob import glob

nodes = []
path = '/home/pietro/.nb/politica/*.md'
output = 'out.html'

for filename in glob(path):
    with open(filename, 'r') as file:
        metadata, content = frontmatter.parse(file.read())

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

        nodes.append({
            'metadata': metadata,
            'content': content,
            'tags:': tags,
        })

with open('index.html', 'r') as html:
    content = html.read()

    content = content.replace('/* __DATA_DECLARATION__ */', f'var data = {json.dumps(nodes)};')

    with open(output, 'w') as out:
        out.write(content)
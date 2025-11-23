import xml.etree.ElementTree as ET

try:
    tree = ET.parse('output/feeds/podcast.atom.xml')
    root = tree.getroot()
    items = root.findall(".//item")
    
    print('✅ XML is valid!')
    print(f'Total episodes: {len(items)}')
    print(f'Feed title: {root.find(".//channel/title").text}')
    
    # Check a few descriptions
    print('\nSample descriptions:')
    for i, item in enumerate(items[:3]):
        desc = item.find('description')
        if desc is not None:
            print(f'{i+1}. {desc.text[:100]}...')
    
except ET.ParseError as e:
    print(f'❌ XML parsing error: {e}')
except Exception as e:
    print(f'❌ Error: {e}')


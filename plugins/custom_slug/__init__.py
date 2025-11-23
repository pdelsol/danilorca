"""
Custom slug generator plugin for Pelican
Generates slugs in format: company-person-title
"""

from pelican import signals
import re
import unicodedata


def slugify_custom(text):
    """Convert text to URL-safe slug"""
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text)
    # Remove accents
    text = ''.join([c for c in text if not unicodedata.combining(c)])
    # Convert to lowercase
    text = text.lower()
    # Replace spaces and special chars with hyphens
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    # Remove leading/trailing hyphens
    return text.strip('-')


def generate_custom_slug(generator, metadata):
    """Generate custom slug from company-person-title"""
    if 'slug' not in metadata:
        company = metadata.get('company', '')
        person = metadata.get('person', '')
        title = metadata.get('title', '')
        
        # Create slug: company-person-title
        slug_text = f"{company} {person} {title}"
        metadata['slug'] = slugify_custom(slug_text)


def register():
    signals.article_generator_context.connect(generate_custom_slug)


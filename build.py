import os
from datetime import datetime

import yaml


SOURCE = 'posts-src'
TARGET = 'posts'


def main():
    # Read the layout files
    with open('layout.html', 'r') as f:
        layout_template = f.read()

    # Delete old built files
    print 'Cleaning up old files'
    for old_file_name in os.listdir(TARGET):
        old_file_path = os.path.join(TARGET, old_file_name)
        os.remove(old_file_path)

    # Read page configuration
    post_config_path = 'pages.yml'
    with open(post_config_path, 'r') as f:
        post_config = yaml.load(f)

    # Build new files
    print 'Building pages from {}...\n'.format(post_config_path)
    post_slugs = post_config.keys()
    for post_slug in post_slugs:
        post = post_config[post_slug]
        file_name = post_slug + '.html'

        print '\t{}'.format(file_name)
        source_file_path = os.path.join(SOURCE, file_name)
        target_file_path = os.path.join(TARGET, file_name)

        # Read source file
        with open(source_file_path, 'r') as f:
            source_file_html = f.read()

        # Do templating
        html = layout_template.format(
            content=source_file_html,
        ).replace('href="./style.css"', 'href="../style.css"')

        # Write output file
        with open(target_file_path, 'w') as f:
            f.write(html)

    # Build index page
    print 'Building index...'

    source_file_path = os.path.join(SOURCE, 'index.html')
    target_file_path = 'index.html'

    # Read source file
    with open(source_file_path, 'r') as f:
        index_html = f.read()

    # Do templating - ensure that posts are in date order
    sort_by_date = lambda slug: datetime.strptime(post_config[slug]['date'], '%d/%m/%Y')
    post_slugs = sorted(post_slugs, key=sort_by_date)

    post_list_html = ''
    for post_slug in post_slugs:
        post_li = '<li><a href="./posts/{slug}.html">{title} - {date}</a></li>'.format(
            slug=post_slug,
            **post_config[post_slug]
        )
        post_list_html += post_li

    index_html = index_html.format(post_list=post_list_html)
    html = layout_template.format(
        content=index_html,
    )

    # Write output file
    with open(target_file_path, 'w') as f:
        f.write(html)


    print "Done!\n"


if __name__ == '__main__':
    main()
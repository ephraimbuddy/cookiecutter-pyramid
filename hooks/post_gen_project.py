import os

WORKING = os.path.abspath(os.path.curdir)


def main():
    clean_unused_template_settings()


def clean_unused_template_settings():
    selected_lang = '{{ cookiecutter.template_language }}'
    templates = os.path.join(
        WORKING, '{{cookiecutter.app_name}}', 'templates')

    if selected_lang == 'chameleon':
        extension = '.pt'
    else:
        extension = "." + selected_lang
    delete_other_ext(templates, extension)


def delete_other_ext(directory, extension):
    """
    Removes all files not ending with the extension.
    """
    for (root, dirs, files) in os.walk(directory, topdown=True):
        for template_file in files:
            if not template_file.endswith(extension):
                os.unlink(os.path.join(root, template_file))


if __name__ == '__main__':
    main()
    print("Check {{cookiecutter.app_name}}/README.txt file for next steps")

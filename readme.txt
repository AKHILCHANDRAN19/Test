Installation:

1. Create new project in PyCharm.
2. Move the files and folders to the project.
3. Run the command in terminal to install the packages into the virtual environment:

pip install -r requirements.txt

===============

main.py (Pin Uploader)

==== POSSIBLE ISSUES ====

1. If you encounter the 'TypeError: init() got multiple values for argument 'options'' error, try removing the first argument ChromeDriverManager().install() when creating the webdriver instance in the Pinterest class, login method.

In other words, replace this code:

driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=chrome_options
        )

with this:

driver = webdriver.Chrome(options=chrome_options)

2. The 'No credentials stored [Errno 2] No such file or directory:' is not critical. It will resolve itself when the cookies are saved to the folder after the first login to the account.

===============

image_generator.py (Pin Generator)

1. If you are using other fonts, you may need to change the font extension (ttf, otf). You can do this in the following lines of code:

font_title_path = READY / folder_name / 'assets' / 'fonts' / 'title_font.ttf'
font_post_path = READY / folder_name / 'assets' / 'fonts' / 'post_font.otf'
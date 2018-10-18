# medium.py
not half baked! almost well done. ;)

## A small, self hosted, medium like python blogging toolset.

Medium *like* means that it mimics the style, UX, usabilty like inline editing ... using the great stuff out there like mediumish theme from wowthemes. The wonderful medium-editor.js which gives you the capability to edit the articles inline. The backend is served by PythonOnWheels. The superb tinyDB is used as a small simple, local full python DB.

## Simple usage:

### clone the repo 
```git clone https://github.com/pythononwheels/medium.py.git medium```

### Install the requirements:

pip install - r requirements.txt

### start the server
python server.py

### Thats it!
Everything else works online just as you know it from medium.

## This is an impression of the article online edit mode:

You can see the inline medium like toolbar right there. You can also see that the selected text is currently formatted as H4. The *code*, *pyhton* and *js* buttons format code already prepared for highlight.js (right code class="", p and br removed ... after copy & paste)

![article edit mode](https://raw.githubusercontent.com/pythononwheels/medium.py/master/static/images/Screenshot_2018-10-18_medium_py_edit.png)


## This is a website screenshot of a demo article in show mode:

This is also the demo article included in the bundle. The edit options on the left are only visible whe you are logged in.

![article show mode](https://raw.githubusercontent.com/pythononwheels/medium.py/master/static/images/Screenshot_2018-10-18_medium_py_show.png)

## Last example is the article admin view:

![article admin mode](https://github.com/pythononwheels/medium.py/blob/master/static/images/Screenshot_2018-10-18_medium_py_article_admin.png)


Check the [Usable online Demo](http://mediumpy.pythononwheels.org). 
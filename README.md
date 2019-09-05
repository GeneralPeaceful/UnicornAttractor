# Stream 4 - Full Stack Frameworks with Django Milestone Project | UnicornAttractor [![Build Status](https://travis-ci.org/GeneralPeaceful/UnicornAttractor.svg?branch=master)](https://travis-ci.org/GeneralPeaceful/UnicornAttractor)


## Description

Unicorn Attractor is the latest and greatest website for compiling all myths, legends and campfire stories - or it will be when people start adding them... - but what makes it really great is that the maintenance and bug-fixing is all completely free! No ads, no annoying pop-ups, forever. "What about improving the site?" I hear you ask; That is where you, the fantastically brilliant user can help. If you want a feature added to the site, you can request it! To do so, I will require funds from said user, with a minimum expenditure of £1. If it does not meet the Development Cost as stated on the feature request, fear not for I will always use 50% of the time I spend working on the site working on the highest paid feature. The default Development Cost is £50, but this is subject to change by staff members. "How do I get you to prioritise a bug?" I hear you ask next; This is simply done by upvoting said bug on its own page.

On a serious note, this is my Module 5 Milestone Project for the Code Institute course. As such it uses the usual trio of HTML, CSS and Javascript/jQuery for the front end. Python makes up the backend with templating help from django and Jinja, the payment API handled by stripe, and the database provided by postgresql. Bootstrap and Fontawesome are used to aid front-end styling, and any other resources can be found in the Technologies Used or Credits sections below.


## Live Demo

[Live site](https://sebs-milestone-5-ua.herokuapp.com/)

Superuser credentials:

Username: admin

Password: adminpassword

Generic user credentials:

Username: basicuser

Password: basicpassword



## UX

The external user's goal (as determined by the idea brief) is to "Report and track work on bugs and other issues with a product they like". The product they like would hopefully be the blog-style posting system, which has limited functionality to demonstrate a purpose but not much more.

The developer's goals (again as determined by the idea brief) are to "Get user's feedback to guide prioritisation" and to "Get money to fund work on future features".

As a result of these aims, and the starting instruction of "Make an issuetracker", I ascertained the following apps and functionality were required:

### Necessary Apps

- **Issuetracker** - obviously. To deal with bugs and features.
- **Comments** - for feedback and inter-user interaction.
- **Cart** - for feature funding
- **Accounts** - to provide an online prescence that users can adopt.
- **Posts/Blog** - dummy functionality of "a product they[the user] likes".

### Necessary Functionality

- **Issuetracker:**
    - A way to report bugs found on the site
    - A way to view all reported bugs
    - A way to request new features
    - A way to view all feature requests
    - A way to edit bugs and features
    - A way for staff/admins to edit the status of bugs and features and the funds required for features
    - A way for users to upvote bugs to guide prioritisation
    - A way for users to contribute to features
    - Asynchronous updating of bug pages that users vote on
- **Comments:**
    - A way to add comments on:
        - Posts/blogs
        - Bugs
        - Features
- **Cart:**
    - A way to add funds, that users are willing to pay, to a general cart
    - A way to update the amounts a user is willing to pay from within the cart
    - A way to remove funds from the cart
    - A way to pay for all the funds in the cart
- **Accounts:**
    - A way to register a new user
    - A way to login an existing user
    - A way to log out again
- **Posts/Blog:**
    - A way to create a new post
    - A way to view all posts on the site
- **General/Other:**
    - A backend to allow admin/staff to edit all content on the site

As a final note on UX, all python files in this project comply with the [PEP8 python style guide](https://www.python.org/dev/peps/pep-0008/).

Except for three.

One is the `settings.py` file in the UA app. The value on line 101 is too long to fit in, if also attempting to comply with the indentation guidelines.
Another is the `test_forms.py` file in the issuetracker app. The name of one of the tests is too long, but to make the title accurate it has to be what it is.
The last one is the `test_forms.py` file in the posts app. Again, an overly long name that is as short yet descriptive as I can get it. So sue me.


## Features

I have used bootstrap v4.3.1 for the majority of the styling and layout on the website, though the main content boxes are handled with custom css.

Given the nature of the apps required, this was alwasy going to be a multi-page site. I determined the following basic layout based off of this:

### Features Implemented


- **bugs_&_features/** - no page for this url
    - **bugs** - page listing all reported bugs
    - **bugs/bugid** - page with a detailed view of a particular bug report. Has comments for user discussion and an upvoting button
    - **features** - page listing all requested features
    - **features/featureid** - page with a detailed view of a particular feature request. Has comments for user discussion and ability to contribute to the feature
    - **addbug** - page containing the report bug form. Form auto-formatted by bootstrap
    - **addfeature** - same as above, but for features instead
    - **editbug/bugid** - available only to the original user who reported the bug and staff. Loads the report bug form as it was last submitted (ie, with content)
    - **editfeature/featureid** - same as the editbug page above, but for feature requests
- **cart/** - shows all contributions that a user requests to contribute to. Saved in a session cookie related to the logged in user
    - **charge/** - view (not a viewable page though) that handles making a payment totalling all costs in the cart
- **accounts/** - no page for this url
    - **login/** - page containing the default django login form. Form auto-formatted by bootstrap. Page cannot be navigated to if already logged in
    - **register/** - page containing the default django registration form. Form auto-formatted by bootstrap. Page cannot be navigated to if already logged in
    - **logout/** - no page for this url, but handles logging out a logged in user. Url only available to logged in users
- **posts/** - the landing page for the website. This has some info about the site, as well as all posts submitted to the site
    - **post/id** - detailed page for each post. Shows when posted, who by, how many views, searchable tags. Has comments below the post
    - **new/** - page containing the add new post form. Form auto-formatted by bootstrap
- **admin/** - default django backend management pages with functionality limited or not by the superuser(s). Available only to site creator and staff members. Those able to log in to the admin site have a link on the main site (when logged in) that takes them there

### Features Left to Implement

### Technologies Used

#### Frontend

- [HTML](https://en.wikipedia.org/wiki/HTML)
- [CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [Javascript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [jQuery](https://jquery.com/)
- [BootStrap v4.3.1](https://getbootstrap.com/)
- [Font Awesome Icons](https://fontawesome.com/icons)

#### Backend

- [Python 3](https://www.python.org/)
- [Django 2.2](https://docs.djangoproject.com/en/2.2/)
- [Stripe](https://stripe.com/gb)
- [PostreSQL](https://www.postgresql.org/)


## Testing

All `forms.py`, `models.py` and `views.py` files have test files inside their respective app folders. These can all be run using `python3 manage.py test`. I have attempted to make the names of each test meaningful yet succinct. These tests are automated and run by [Travis CI](https://travis-ci.org/), and are implemented using django's `unittest` module.

Due to the nature of AWS cloud9, where literally everything (not just the dependencies related to your work) get put into the requirements.txt file, there are some minor commits to debug TravisCI. There may also be some dependencies in the requirements that are not required for the code behind this site to run, but I fear removing anything now in case everything breaks horrifically.

In terms of layout, I have tested on various browsers and all works well as far as I can tell. If you find something, submit a bug report on the site and I will work on it at some point...


## Deployment

The deployment instructions below are based off of the assumption that the user has git and python pre-installed and configured to run console commands. Following these steps should allow you to run this code locally. The other assumption is that the user is using Cloud9 as their IDE, other IDEs may have alternative or additional steps required to get the code functioning.

1. Clone the repository with

    `git clone https://github.com/GeneralPeaceful/UnicornAttractor.git`

2. Change directory to the cloned repository with

    `cd UnicornAttractor`

3. Install the dependencies from the requirements.txt file with

    `sudo pip3 install -r requirements.txt`

4. Set up environment variables.

    To do this, you need to create a file with the title `env.py` in the UnicornAttractor folder. Inside that file, you must set the following variables with `os.environ.setdefault('key', 'value')`:
    - `'STRIPE_PUBLISHABLE', '<public key acquired from Stripe>'`
    - `'STRIPE_SECRET', '<secret key acquired from Stripe'`
    - `'DATABASE_URL', '<>'`
    - `'SECRET_KEY', '<a secret key of some description>'`
    - `"AWS_ACCESS_KEY_ID", "<acquired from AWS' S3 bucket credentials>"`
    - `"AWS_SECRET_ACCESS_KEY", "<acquired from AWS' S3 bucket credentials>"`
    
    If the `DATABASE_URL` value is left blank, the default database of SQLite will be used. This is preferred for development and testing purposes. For the [Stripe](https://stripe.com/docs/keys) and [AWS bucket](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingBucket.html) keys, please see their respective sites and documentation on how to set these up as this is not covered in this readme.

5. Optional steps for testing purposes

    The aforementioned users should be usable for accessing the site, but if not then a new superuser can be created with `python3 manage.py createsuperuser` and filling out the details. For testing, you will also need to set `DEBUG = True` in the `settings.py` file in the UA folder within UnicornAttractor.

6. Run the code with

    `python3 manage.py runserver $IP:$PORT`
    
    Please note that you will get a bad gateway error, as the url you use will not yet be in the `ALLOWED_HOSTS` list in the `settings.py` file. Simply copy-paste it into there, and refresh the page.


## Credits

Credit to [OpenClipart Vectors](https://pixabay.com/users/openclipart-vectors-30363/) for the Unicorn svg I am using for a logo.

Much of the functionality and style ideas came from [Huckcity's Unicorn Attractor](https://milestone-project-five.herokuapp.com/) site. I felt that the UX was brilliant and strived to build something similar, without directly copying it.
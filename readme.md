# Inventory Management System for college clubs
A Full-Stack Web Application to facilitate sharing resources in college clubs. Each user can be a part of multiple clubs and request or approve resources based on their role(s) and permissions. Supports email notifications and valuable statistics on the user dashboard.


<br>
<h2>Member and Convenor Demo</h2>

https://user-images.githubusercontent.com/76661350/170917181-f410ddcc-c658-45ff-9e49-1363ffe91c70.mp4

<br>

<h2>Admin Demo</h2>

https://user-images.githubusercontent.com/76661350/170917170-75b93a30-f63a-4141-b08e-fcf6b494deaf.mp4

<br>

<h2>Tech Stack</h2>
<code><img height="40" width="40" src="https://img.icons8.com/color/48/000000/python--v1.png" alt="Python"></code>
<code><img height="40" width="40" src="https://user-images.githubusercontent.com/76661350/143919769-d61dd74a-ef98-49db-b1d0-781cb2df501c.png"></code>
<code><img height="45" width="40" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/html/html.png" alt="HTML"></code>
<code><img height="36" width="40" src="https://cdn.iconscout.com/icon/free/png-256/css-131-722685.png" alt="CSS"></code>
<code><img height="36" width="40" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/javascript/javascript.png" alt="Javascript"></code>
<code><img height="36" width="40" src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Bootstrap_logo.svg/1280px-Bootstrap_logo.svg.png" alt="Bootstrap"></code>
<code><img height="36" width="40" src="https://camo.githubusercontent.com/9be0208aa516b4d1976412d27e9f73d851ea253f8ee005a0b600939f841bba8b/68747470733a2f2f7777772e63686172746a732e6f72672f6d656469612f6c6f676f2d7469746c652e737667" alt="Chart.js"></code>
<code><img height="36" width="40" src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/SQLite370.svg/1280px-SQLite370.svg.png" alt="SQLite3"></code>
<br>
<br>

<h2>Installation Guide</h2>
<h3>Virtual Environment</h3>

`pip install virtualenvwrapper-win`<br>
`mkvirtualenv test` &nbsp; _test = name of virtual env_

<br>
<h3>Install required packages:</h3>

`pip install -r requirements.txt`<br>
_After ensuring that we are in a virtual environment (If not, use `workon test`)_

<h3>To run project:</h3>

`python manage.py makemigrations` <br>
`python manage.py migrate` <br>
`python manage.py runserver`<br>
<p>Visit development server at http://127.0.0.1:8000 </p>
<br>
<h3>Create Super user:</h3>

`python manage.py createsuperuser`
<p>Enter desired credentials</p>
<br>
<h3>To see emailing features</h3>
<p>- Visit https://www.wpoven.com/tools/free-smtp-server-for-testing</p>
<p>- Enter the desired email to see the inbox</p>

<br>
<h3>Admin Site:</h3>

http://127.0.0.1:8000/admin

<br>
<h3>Implemented Features</h3>
<ul>
    <li>Member
        <ul>
            <li>View club items</li>
            <li>Request for items</li>
            <li>View request status</li>
            <li>View statistics about their requests </li>
        </ul>
    </li>
    <li>Convenor
        <ul>
            <li>View all members of club</li>
            <li>View club items</li>
            <li>Add, Update items</li>
            <li>View member requests</li>
            <li>Approve/Reject requests</li>
            <li>Validation of quantity of requested item</li>
            <li>View statistics pertaining to the club</li>
        </ul>
    </li>
    <li>Admin
        <ul>
            <li>View all clubs, users, items and requests</li>
            <li>Add new club(s)</li>
            <li>Add, Update items</li>
            <li>Add new user or existing users to clubs</li>
            <li>Delete users</li>
        </ul>
    </li>
    <li>Authentication and page restrictions</li>
    <li>Reset, Change Password</li>
    <li>Email respective users about request flow</li>
</ul>
<br>
<br>
<h3>References:</h3>
<a href="https://docs.djangoproject.com/en/3.2/">Django's Official Documentation</a><br>
<a href="https://www.chartjs.org/">Chart.js Official Documentation</a><br>
<a href="https://www.youtube.com/watch?v=tUqUdu0Sjyc&list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO&index=15">Dennis Ivy
    Youtube</a><br>
<a href="https://www.youtube.com/watch?v=yyBF-2SXXOc&t=690s">Super Coders Youtube</a><br>
<a href="https://stackoverflow.com/">Stack Overflow</a><br>

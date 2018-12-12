Title:
404-Name Not Found

Subtitle:
Discourz

Semester:
Fall 2018

Overview:
Our team decided to create an application where you could have discussions, debates and polls about various topics with different users of the application. Users would be able to create their own profiles, their own debates, and their own polls that other users could interact with in real time. This is innovative because it makes the debate more interesting since it is in real time between two people. They can interact quickly for an unlimited amount of time until one of them ends a the debate. It is also innovative because it allows other users to give their opinion on who won the debate with a vote that is counted in real time. In order for the debate and discussion section to work the redits server must be used.  

Team Members:
Dhruv Khurana-khuranadhruv18, Panupong Leenawarat-Okrymus inc, Jared Pina-J4yrad, Prakrit Saetang-Number535, Patrick Conway-pjconway, Chen Xie-chen678

User Interface:

![example image](imgs/poll.png)

The above image is the poll view of our application where you are able to vote on a poll you or another user has created. The image above shows an example question with example answers showing the answer the user selected. The user is an admin because they are able to delete the post, as shown on the bottom of the page. 

![example image](imgs/discussion.png)

The above image shows an example of an ongoing discussion between several users, j4yrad, Mr_Awesome and EvilJared. This discussion is in real time and allows many users to participate at once. 

![example image](imgs/login.png)

The above image shows an example of the login view of our application. You are able to enter your username and password and then the application logs you in. If you do not already have profile, there is a link to the sign up page.

![example image](imgs/search.png)
The above image shows an example of the search view. This allows users to search words and related posts come up in the results. You can filter between polls, debates, and discussions. 

![example image](imgs/sign_up.png)
The above image shows the sign up view. In this view, the user creates a username, password, enters their email, and creates a bio about themselves. This profile will be viewable to other users.

![example image](imgs/pastpolls.png)
The above image shows the view of the polls that can be sorted by most recent and most popular. The user can create a new poll or select a poll that has already been created. Clicking on the poll brings them to a view where they can vote on that poll. 

![example image](imgs/profile.png)
The above image shows the profile view of the application for a specific user. It shows their past polls, debates, and discussions as well as showing the number of polls and discussions the user has created. It also shows the number of debates the user has won or lost.

![example image](imgs/profile2.png)
The above image is also the profile view of the application, but it also shows what it looks like when someone wins a debate. It shows tagged interests for the user as well.

Data Model:
![example image](imgs/data_model.png)


- The account model contains information of each user that signed up with our website.  It includes User field (username, password, email address), image field for a profile picture, test field for user's bio, text field for his/her interests, and integer fields to count how many times they win or lose debates
- PollTopic model contains information of each created poll. It includes the poll's title in text field, the poll's options' in text field, each option's votes in text field, voters (Account model), image of the poll, created date, and tags.
- Debate model contains information about each created debate, and is listed on the debate page for other users to interact with. We control whether the debate is open to new users with the isOpen boolean field. We have tags on the debate to indicate the different categories the debate falls under. We have the topic of the debate, and the initial user's position on the topic. Finally, we get the name of both users, and the date to order the objects correctly on the debates page. Much of this data is stored within the PastDebates model, which makes voting on the debate possible.
- Discussion model is essentially the same as debates, except we don't store the joining users' names and we allow the user to post an image. In the discussion page, more than 1 other user can join a discussion as opposed to just 1 person for debates.

URL Routes/Mappings:

/ -> index.html

This URL maps to the homepage where a user can view hot poll topics, recent past debates, live debates, live discussion, and recent polls.

/aboutus -> about_us.html

This URL maps to the "about us" page where a user can view the information about the website and developers.

/profile -> profile.html

This URL maps to the profile page where a user can see their own information such as username, email address, bio, interests, and their polls, debates, and discussions.

/debate

/waitLobby/<id>/

/joinChat/<uuid>/

/debateChat/<uuid>/

/debate_create

/pastChat/<uuid>

/edit_profile/<slug:username>

/poll_home -> poll_home.html

This URL maps to the homepage for polls where a user can either view most recent polls or most popular polls.

/poll_create -> poll_create.html

This URL maps to the page where a user can create a new poll.

/poll/<uuid>/ -> poll.html

This URL maps to the page where a user can vote on a specific poll

*if the user is in the admins group, the user can delete the poll on this page*

/poll_voting/<uuid>/<vote>/

This URL will allow a user to mark their vote and it will redirect to the poll.html.

/poll_deleting/<uuid>/

This URL will allow a user in the admins group to delete a poll.

/discussion_home

r'^search/$'

r'^ajax/create_past_debate/$'

r'^ajax/post_comment/$'

r'^ajax/new_message/$'


Authentication/Authorization:
Users are authenticated with basic sign up and sign in parts of the application. The admin has more permissions than the regular users. He is able to delete polls, while regular users are not. If a user is an admin, they will have a different perception of the poll view than a regular user because they will be able to delete polls while the regular users will not have this option.

Team Choice:
Our team choice was to include a real time aspect within our application. We wanted discussions and debates to be in real time to make it more interesting. The votes on who won the debate is also in real time. We had to add URL routes for the discussion, debates, comments, and search aspects of the application. 

Conclusion:
Overall, our team had a very positive experience working on this project. It was good to get to know eachother's strengths and weaknesses and learn to work to each member's strengths. We learned about creating a user interface, data models, URL routing, and authentication of the user. Putting together all this knowledge, we now have a broad overview of web programming. The biggest challenge that we faced as a group was organizing times where we could meet up and work on the project. Since we had a large group (6 people), it was difficult to find a time where we could all meet. Other than this, we experienced some slight bugs along the way but they were easily fixable and only slightly impacted our progress negatively. I think one thing we would have liked to know before starting the project would have been that we should start our code as early as possible. We started doing this later in the semester in order to give ourselves plenty of tiem to make sure everything is perfect and it took a lot of pressure off of us.

Overview: 
Our team, 404-Name Not Found, decided in the beginning of the semester to create a website on which you could have debates and polls about specified topics. We have not made any changes to our project proposal since the submission of project 2, but we have made a good amount of progress in building our website in that time. We have implemented login and logout functionality on our website using authentication support in Django. This allows us to give the user a specific view of our application based on the information associated with the user's profile. We used several user interaction forms in our application as well. These include the the debate page, the poll page, the login page, the edit profile page, and the user sign up page. 


Team Members:
Patrick Conway-pjconway, Dhruv Khurana-khuranadhruv18, Panupong Leenawarat-Okrymus inc, Jared Pina-J4yrad, Prakrit Saetang-Number535, Chen Xie-chen678


Video Link:
https://www.youtube.com/watch?v=rZ7IBnCd5Fw

Design Overview:
For this stage of the project, our team was able to implement login/logout functionality as well as make it so users are able to create and edit a new profile. When a user creates their profile, their profile and its information is stored in our database. After creating their profile, the user can edit basically every aspect of their profile (email, profile picture, biography, etc.) and these changes will be saved in our database. We also implemented a way for users to start debates and polls. The polls and debates that the user started will also be linked to their profile.  


Problems:
The main problem that we experienced during this stage of the project was the same as our main problem for project 2, scheduling. We have a fairly large team (6 students), so finding a time where we could all meet and discuss the project outside of class proved to be difficult. Thankfully, we divided the work up during class and were able to commit our individual parts to github, but it would have been better if we could have met to discuss our project in person more. Another problem we experienced was choosing a topic for team choice. We were not disagreeing with eachother on what we should do, it just took us a while to come up with a good idea that we wanted to implement in our application.


Successes:
We had several successes while working on this stage of the project, but we agree that our greatest success was being able to complete every part of the project (except for the write-ups and video) about 2 weeks before the due date. This took a lot of pressure off of us because we did not have to scramble to finish the project close to the due date. We were able to accomplish this because we did a very good job dividing up the work and everyone was able to complete their part of the project in a timely manner. Another success we had was implementing forms in our application. Our website requires many forms, as shown in the overview, and we feel as though we implemented them seamlessly.


Team Choice:
For the team choice section of our project, our team decided that we wanted to implement real-time chats in the debate page of our application. In order to accomplish this, we will use a library call Django Channels. This library extends Django's abilities beyond HTTP and allows it to handle chat protocols, resulting in a real-time chat. It does this by layering an asynchronous layer underneath Django, allowing it to handle connections and sockets asynchronously.

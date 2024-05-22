# Installation

##  Test Repo
This will be updated with the "formal" pypi repo eventually, but for now it's located here.

    python3 -m pip install --upgrade --index-url https://test.pypi.org/simple/ canvas-lms-api

## Formal Repo
This will be updated with the "formal" pypi repo eventually, but for now it's located here.

    python3 -m pip install --upgrade canvas-lms-api

Alternatively, you can download the source code and pip install from that:

    git clone https://github.gatech.edu/omscs-ta/canvas-lms-api
    cd canvas-lms-api
    pip install .

I would also *strongly* encourage you to use a .ta folder and house a .yml file in your home directory so you can just point to it with any/all scripts.


# Usage:
## Get Canvas Token
Found here: Canvas > Account > Settings > Approved Integrations: > New Access Token.

## Get Course Number
There are really 2 ways. 
1. Use this tool to find all the courses and then use the number below (course is optional so you can set it later)
````
from canvas_lms_api import Canvas
grader = Canvas(base="https://gatech.instructure.com", token=YOUR TOKEN)
grader.GetCourses()
````
2. Login to canvas
    * Go to your course
    * eg: https://gatech.instructure.com/courses/46234
    * The value for canvas_course is "46234"

## Get Assignments Example

````
from canvas_lms_api import Canvas
grader = Canvas(base="https://gatech.instructure.com", token=YOUR TOKEN, course=Your Course Number)
grader.GetAssignments()
````

## Get Course Users Example
````
from canvas_lms_api import Canvas
grader = Canvas(base="https://gatech.instructure.com", token=YOUR TOKEN, course=Your Course Number)
grader.GetCourseUsers()
````

## Submit Grades Example
````
from canvas_lms_api import Canvas
grader = Canvas(base="https://gatech.instructure.com", token=YOUR TOKEN, course=Your Course Number)
# Find your assignment id number see Get Assignments Example
assignment_id = ""
# Find your student id number see Get Course Users Example
student_id = ""

# Set score and comment
score = "75"
comment = "The student failed to complete the assignment\nAnd they got thse points wrong\n(-10) for poor guessing"
grader.SubmitGrade(assignment_id, student_id, score, comment, visibility=False)
````

## Get StudentID by sortable name
````
from canvas_lms_api import Canvas
grader = Canvas(base="https://gatech.instructure.com", token=YOUR TOKEN, course=Your Course Number)
# If you have downloaded all submissions from canvas, the students files should be named with their sortable name in the string
# For your use case you'll need to parse them, but then when you have them you can get the student id from there. This will allow you to use the submit grades function.
sortable_name = "deanjimmy"
grader.GetIDBySortableName(sortable_name)
````

## GetCourseModules
If you include "True" in GetCourseModules, this should allow you to get all full urls to modules.

I use the following to post links to lectures in my weekly announcements. (Though I have a shared repo for this if you ask for the url).

````
def lectures_to_dict(modules):
    res = {}
    for i in modules:
       # The lectures in my course use the form P#L# but you can tweak this to match how you name your sections, or even make a dictionary of your titles.
       m = re.search('(P\dL\d).*', i["name"]) 
       if m:
          for j in i["items"]:
              if j["position"] == 1:
                  print (j)
                  res[m.group(1)] = j["html_url"]
    return res
````

````
def replace_content(schedule, post_content, week_number, post_numbers, classID, lectures):
    # This is where we replace "variable content" in our weekly announcements.
    post_content = post_content.replace("|||HW1RELEASEDATE|||", schedule["hw1_assigned"] + ' T11:59:59Z')
    post_content = post_content.replace("|||HW2RELEASEDATE|||", schedule["hw2_assigned"] + ' T11:59:59Z')
....
    new_content = ""
    for j in post_content.split('\n'):
        found = False
        for i in lectures:
            if i in j:
                new_content += "* <a href=" + lectures[i] + ">" + i + "</a>" # Here is where we plop in the lectures. I just search for the dictionary strings in the weekly post content I have.
                found = True
        if not found:
            new_content += j + "\n"
    post_content = str(new_content) 
    return post_content
````


````
# get_week_announcement(week_number)  # This just returns the content of the weeks announcement.

# this is the high level series of functions I'll call to get a post put together, I also post to piazza in later functions not noted here.
grader = Canvas(base=_config["base"], token=_config["canvas_api"], course=_config["canvas_course"])


# This is the important function!
students_canvas = grader.GetCourseModules(True) # True will get all modules

res = lectures_to_dict (students_canvas)
post_content = get_week_announcement(week_number)
post_content = replace_content(_schedule, post_content, week_number, post_numbers, _config["piazzaclass"], res)
````

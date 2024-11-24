import requests
import json
from bs4 import BeautifulSoup
import re
from gpt import summarize

# ex: getProf("ecse-324")
def getProf(courseCode, season):

    season = season.strip().lower().capitalize()

    URL = "https://www.mcgill.ca/study/2024-2025/courses/" + courseCode
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    elements = soup.find_all(class_="catalog-instructors")

    pattern = r"([\w\s',;]+)\((Fall|Winter)\)"
    matches = re.findall(pattern, str(elements))

    instructorDict = {"Fall": [], "Winter": []}

    for instructors, semester in matches:
        instructorList = instructors.split(";")
        for i in range(len(instructorList)):
            instructorList[i] = instructorList[i].strip()
        instructorDict[semester] = instructorList

    return instructorDict[season]


def getProfId(name):
    URL = "https://www.ratemyprofessors.com/search/professors/1439?q=" + name
    page = requests.get(URL)
    pattern = r'"legacyId":(\d+)'
    match = re.search(pattern, page.text)
    if match:
        legacyId = match.group(1)
        return legacyId
    else:
        return "000000"


# Returns a list of dict including class, quality rating, difficulty rating, comment
def getProfInfo(legacyId):
    infoList = []

    URL = "https://www.ratemyprofessors.com/professor/" + legacyId
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    elements = soup.find_all(class_="Rating__RatingBody-sc-1rhvpxz-0 dGrvXb")

    for element in elements:

        infoDict = {}

        pattern = r'RatingHeader__StyledClass-sc-1dlkqw1-3 eXfReS"> <!-- -->([^<]+)'
        match = re.search(pattern, str(element))
        if match:
            course = match.group(1)
            infoDict["course"] = course

        pattern = r'Quality.*?(\d\.\d)'
        match = re.search(pattern, str(element))
        if match:
            quality = match.group(1)
            infoDict["quality"] = quality

        pattern = r'Difficulty.*?(\d\.\d)'
        match = re.search(pattern, str(element))
        if match:
            difficulty = match.group(1)
            infoDict["difficulty"] = difficulty

        pattern = r'Comments__.*?>([^<]+)'
        match = re.search(pattern, str(element))
        if match:
            comment = match.group(1)
            infoDict["comment"] = comment.strip()

        infoList.append(infoDict)

    return infoList

def convertGradeToNumber(grade):
    if grade == "A":
        return 0
    elif grade == "A-":
        return 1
    elif grade == "B+":
        return 2
    elif grade == "B":
        return 3
    elif grade == "B-":
        return 4
    elif grade == "C+":
        return 5
    elif grade == "C":
        return 6
    elif grade == "D":
        return 7
    elif grade == "F":
        return 8
    else:
        raise ValueError("Invalid grade entered")

def convertNumberToGrade(number):
    number = round(number)
    if number == 0:
        return "A"
    elif number == 1:
        return "A-"
    elif number == 2:
        return "B+"
    elif number == 3:
        return "B"
    elif number == 4:
        return "B-"
    elif number == 5:
        return "C+"
    elif number == 6:
        return "C"
    elif number == 7:
        return "D"
    elif number == 8:
        return "F"
    else:
        raise ValueError("Invalid number entered")

def getComments(listOfClasses, semester):

    toReturn = []

    for aClass in listOfClasses:

        commentList = []

        profList = getProf(aClass, semester)

        aClass = aClass.upper().replace("-", "")

        if len(profList) >= 1:
            for prof in profList:
                infoList = getProfInfo(getProfId(prof))
                for infoDict in infoList:
                    if infoDict.get("course") == aClass:
                        commentList.append(infoDict.get("comment"))

        toReturn.append(commentList)

    return toReturn

def getAverageForClass(className):
    jsonfile = open("./data/averages.json")
    classes = json.load(jsonfile)
    jsonfile.close()
    processedName = className.upper().replace("-","")
    grades = []
    for term in classes[processedName]:
        grades.append(term["average"])

    grades = grades[-5:]

    for i, grade in enumerate(grades):
        grades[i] = convertGradeToNumber(grade)

    average = sum(grades)/len(grades)
    lettergrade = convertNumberToGrade(average)
    return lettergrade, average


def getCreditsForClass(className):
    jsonfile = open("./data/averages.json")
    classes = json.load(jsonfile)
    jsonfile.close()
    processedName = className.upper().replace("-","")
    return classes[processedName][-1]["credits"]



# The higher the rating, the harder the class
def getClassRating(credit, pastAverage, classDifficulty, profRating):

    classRating = 0


    if pastAverage == 0: # A
        classRating += 0
    elif pastAverage == 1: # A-
        classRating += 10
    elif pastAverage == 2:  # B+
        classRating += 20
    elif pastAverage == 3:  # B
        classRating += 25
    elif pastAverage == 4:  # B-
        classRating += 35
    elif pastAverage == 4:  # C+
        classRating += 45
    else:
        classRating += 50

    classRating += (classDifficulty/6)*25

    classRating += ((6-profRating)/6)*25

    if credit == 1:
        classRating *= 0.4
    elif credit == 3:
        pass
    elif credit == 4:
        classRating *= 1.2

    return classRating

# The higher the rating, the harder the semester, average is 1
def getSemesterRating(classRating, totalCredits):

    maxRating = 50*5

    semesterRating = 0

    for rating in classRating:
        semesterRating += rating
    multiplier = 1 + 0.05 * (totalCredits - totalCredits % 3 - 15) + 0.02 * (totalCredits % 3)
    semesterRating *= multiplier

    semesterRating /= maxRating

    return semesterRating

def getListOfClasses(userInput):
    classes = userInput.split(",")
    for i in range(len(classes)):
        classes[i] = classes[i].strip().lower().replace(" ", "-")
    return classes



if __name__ == "__main__":
    # avg = getClassRating(3, 3, 3, 3)
    # class1 = getClassRating(4, 3, 3, 3)
    # class2 = getClassRating(1, 1, 2, 4)
    # print(class2)
    # print(getSemesterRating([50,50,50,50, 20],13))
    # print(getSemesterRating([class1,avg,avg,avg,avg, class2],16))
    print(summarize(getComments(["ecse-324", "ecse-325", "ecse-206", "ecse-250"], "Fall")))

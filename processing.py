import requests
from bs4 import BeautifulSoup
import re


# ex: getProf("ecse-324")
def getProf(courseCode, season):
    season = season.strip().lower().capitalize()
    courseCode = courseCode.lower().replace(" ", "-")

    URL = "https://www.mcgill.ca/study/2024-2025/courses/" + courseCode
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    elements = soup.find_all(class_="catalog-instructors")

    pattern = r"([\w\s',;]+)\((Fall|Winter)\)"
    matches = re.findall(pattern, str(elements))

    instructorDict = {}

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




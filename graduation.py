
# coding: utf-8

# In[4]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from getpass import getpass
import re,os

returnData = []
scoreArray = []
selectiveCourse = []
selectiveCoreNum = [0,0,0,0]
languageCourse = []
selectiveCoreCourseList = [['計算機圖學於智慧手機導論','影像處理導論','訊號與系統'],['嵌入式系統導論','軟體工程'],['無線網路導論','網路程式設計'],['資訊安全導論','正規語言']]
exceptKeyword = ['軟體','程式','多媒體','系統','資訊','電腦','網路','資料','計算機','手機']

def calFunc(code_point,englishReview,professionalEnglishCourse,crossDegreeOfGeneralEducation,generalEducationPoint):
    if scoreArray[1] <64:
        returnData.append("必修門檻未通過，還差" + str(64-scoreArray[1]) +"學分，請補修本系必修科目\n")
    else:
        returnData.append("必修門檻已通過\n")

    if scoreArray[2] <24:
        returnData.append("選修門檻未通過，還差" + str(24-scoreArray[2]) +"學分，請補修本系選修科目\n")
    else:
        returnData.append("選修門檻已通過\n")

    core_field=0
    core_total=0
    for i in range(0,4):
        if(selectiveCoreNum[i]!=0):
            core_field+=1
        core_total+=selectiveCoreNum[i]

    if core_field <2:
        returnData.append("核心選修領域數門檻未通過，還差" + str(2-core_field) +"領域，請補修本系核心選修科目\n")
    else:
        returnData.append("核心選修領域數門檻已通過\n")

    if core_total <3:
        returnData.append("核心選修課堂數門檻未通過，還差" + str(3-core_total) +"堂課，請補修本系核心選修科目\n")
    else:
        returnData.append("核心選修課堂數門檻已通過\n")

    if languageCourse[0]*2 <4:
        returnData.append("國文門檻未通過，還差" + str(4-languageCourse[0]*2) +"學分，請補修國文科目\n")
    else:
        returnData.append("國文門檻已通過\n")

    over_point = 0
    if scoreArray[2] >24:
        over_point =  over_point+scoreArray[2]-24
    if scoreArray[6] >16:
        over_point = over_point+scoreArray[6]-16
        scoreArray[6] = 16

    if languageCourse[1]<6 and (professionalEnglishCourse*2+over_point)<6:
        returnData.append("英文門檻未通過，請補修專英科目\n(若系上選修已修足24則可使用系上選修補修，若系外必選修超過16學分則可使用系外必選修補修)\n")
    else:
        returnData.append("英文門檻已通過\n")

    if languageCourse[2] <4:
        returnData.append("體育門檻未通過，還差" + str(4-languageCourse[2]) +"堂課\n")
    else:
        returnData.append("體育門檻已通過\n")

    if generalEducationPoint<18:
        returnData.append("通識學分數門檻未通過，還差" + str(18-generalEducationPoint) +"學分\n")
    else:
        returnData.append("通識學分數門檻已通過\n")
        
    if crossDegreeOfGeneralEducation<5:
        returnData.append("通識領域數門檻未通過，還差" + str(5-crossDegreeOfGeneralEducation) +"領域\n")
    else:
        returnData.append("通識領域數門檻已通過\n")


    if languageCourse[1] ==7:
        languageCourse[1]=6

    if scoreArray[5]>6:
        scoreArray[5]=6

    if(scoreArray[5]+scoreArray[6])>16:
        other_point_total = 16
    else:
        other_point_total = scoreArray[5]+scoreArray[6]

    total_point = scoreArray[1]+scoreArray[2]+languageCourse[0]*2+languageCourse[1]+generalEducationPoint+other_point_total

    if total_point<132:
         returnData.append("總畢業學分門檻未通過，還差" + str(132-total_point) +"學分\n")
    else:
        returnData.append("總畢業學分門檻已通過\n")

    if englishReview ==0:
        returnData.append("英語能力畢業資格未通過\n")
    else:
        returnData.append("英語能力畢業資格已通過\n")

    if code_point <2:
        returnData.append("程式能力畢業資格未通過\n")
    else:
        returnData.append("程式能力畢業資格已通過\n")

def main(accountFromWeb,passwordFromWeb,CPEPointFromWeb):
    #open Chrome browser
    chrome_options = Options()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)


    #visit website
    driver.get('https://ohs01.ntpu.edu.tw/student_new.htm')
    #get account bar
    accountBar = driver.find_element_by_name('stud_num')
    passwordBar = driver.find_element_by_name('passwd')
    #input account info
    accountBar.send_keys(accountFromWeb)
    passwordBar.send_keys(passwordFromWeb)
    #submit
    driver.find_element_by_id('loginBtn1').click()
    if driver.current_url == 'https://ohs01.ntpu.edu.tw/pls/pm/stud_system.login':
    	return(4044444)


    code_point = int(CPEPointFromWeb)

    #go to  graduate page
    driver.get('https://ohs01.ntpu.edu.tw/pls/univer/query_all_course.judge?func=9')

    #get require course info
    arrayOfNum = driver.find_elements_by_class_name('ss1')
    for grade in arrayOfNum:
        scoreArray.append(int(re.findall(r'\d+',grade.get_attribute('innerHTML'))[0]))

    #get selective course info 
    arrayOfSelectiveCourses = driver.find_elements_by_xpath("//td[@style='padding-right: 10px']")
    for course in range(0,len(arrayOfSelectiveCourses),3):
        #print(arrayOfSelectiveCourses[course].get_attribute('innerHTML'))
        selectiveCourse.append(arrayOfSelectiveCourses[course].get_attribute('innerHTML'))

    #get language course and PE  info
    arrayOfLanguage = driver.find_elements_by_xpath("//table[@style='border-collapse: collapse'][5]/tbody/tr/td")
    languageCourseOriginal = []
    for course in range(0,len(arrayOfLanguage)):
        languageCourseOriginal.append(re.findall(r'[^\n\u3000]+',arrayOfLanguage[course].get_attribute('innerHTML')))
    for courseType in range(0,len(languageCourseOriginal)):
        if languageCourseOriginal[courseType][0] == '<img src="../../img/stopped.gif">':
            languageCourse.append(0)
        else:
            languageCourse.append(len(languageCourseOriginal[courseType]))

    #get toeic score range
    toeicChecker = driver.find_elements_by_xpath("//table[@style='border-collapse: collapse'][6]/tbody/tr/td/font")
    if len(toeicChecker) > 0 and toeicChecker[0].get_attribute('innerHTML').find('免修') != -1:
        languageCourse[1] = 0

    #get english graduate review info
    if driver.find_elements_by_xpath("//table[@style='border-collapse: collapse'][2]/tbody/tr/td/p/font")[0].get_attribute('innerHTML').find('不') == -1:
        englishReview = 1
    else:
        englishReview =  0

    #get professional english info and other course info
    arrayOfProfessionalEnglish = driver.find_elements_by_xpath("//table[@style='border-collapse: collapse'][6]/tbody/tr/td")
    professionalEnglishCourse = len(re.findall(r'專業英文',arrayOfProfessionalEnglish[0].get_attribute('innerHTML')))
    scoreArray[5] -= len(re.findall(r'全民國防教育',arrayOfProfessionalEnglish[0].get_attribute('innerHTML')))*2

    #except other course by keyword
    arrayOfOtherDepartmentCourse = re.findall(r'[^\s]+',arrayOfProfessionalEnglish[1].get_attribute('innerHTML'))
    for course in arrayOfOtherDepartmentCourse:
        for keyword in exceptKeyword:
            if course.find(keyword) != -1:
                scoreArray[6] -= int(re.findall(r'(\d+)(?!.*\d)',course))

    #print(scoreArray)
    #print(selectiveCourse)
    #print(languageCourse)

    #get general Education info
    arrayOfGeneralEducation = driver.find_elements_by_xpath("//table[@style='border-collapse: collapse'][5]/tbody/tr/th/table/tbody/tr/td")
    crossDegreeOfGeneralEducation = 0
    for i in arrayOfGeneralEducation:
        if len(re.findall(r'(2)',i.get_attribute('innerHTML'))) > 0:
            crossDegreeOfGeneralEducation+=1
    #print(crossDegreeOfGeneralEducation)

    generalEducationPoint = driver.find_elements_by_xpath("//table[@style='border-collapse: collapse'][5]/tbody/tr/th/table/tbody/tr/th")
    generalEducationPoint = int(generalEducationPoint[len(generalEducationPoint)-2].get_attribute('innerHTML'))
    #print(generalEducationPoint)

    for course in selectiveCourse:
        for coreCourseIndex in range(0,len(selectiveCoreCourseList)):
            if course in selectiveCoreCourseList[coreCourseIndex]:
                selectiveCoreNum[coreCourseIndex]+=1

    if languageCourse[1] == 4:
        languageCourse[1] = 6

    driver.quit()
    calFunc(code_point,englishReview,professionalEnglishCourse,crossDegreeOfGeneralEducation,generalEducationPoint)
    return(returnData)

if __name__== "__main__":
    main()


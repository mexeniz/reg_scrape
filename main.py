from lxml import html
import time , datetime
import requests
import urllib3
import econnector

def get_text(course_code) :
	# urllib3.disable_warnings()
	cookie = '_ga=GA1.3.1139030350.1417094164; cresist=Iivt43_9080@ZkkIvt; JSESSIONID=0000qsF2vcQXCyJd9U68atkeqHU:-1'
	header = {
				"Host" : 'www2.reg.chula.ac.th' ,
				"Connection" : 'keep-alive',
				"Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
				"Upgrade-Insecure-Requests": 1 ,
				"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
				"Referer": "https://www2.reg.chula.ac.th/servlet/com.dtm.chula.cs.servlet.QueryCourseScheduleNew.CourseListNewServlet?examdateCombo=I2014101%2F12%2F2014&studyProgram=S&semester=1&acadyearEfd=2558&submit.x=35&submit.y=6&courseno=2110&coursename=&examdate=&examstartshow=&examendshow=&faculty=21&coursetype=&genedcode=&cursemester=1&curacadyear=2558&examstart=&examend=&activestatus=OFF&acadyear=2558&lang=T&download=download",
				"Accept-Encoding": 'gzip, deflate, sdch',
				"Accept-Language": 'en-US,en;q=0.8,th;q=0.6',
				"Cookie": cookie 
				}

	# session = requests.Session()
	page = requests.get('https://www2.reg.chula.ac.th/servlet/com.dtm.chula.cs.servlet.QueryCourseScheduleNew.CourseScheduleDtlNewServlet?courseNo={0}&studyProgram=S'.format(course_code) , headers = header)

	# page = requests.get('https://www.youtube.com/watch?v=8obobqFsD9c')
	tree = html.fromstring(page.text)
	# seat = tree.xpath('//*[@id="Table3"]/tbody/tr[3]/td[10]/nobr/font/text()')
	text = tree.xpath('//nobr/font/text()')
	return text

def extract(text) :
	array = []
	for s in text :
		if not (s.find('/')== -1 ) :
			array.append(s)

	result = []
	for string in array :
		length = len(string)
		i = string.find('/')
		t_index = string.rfind('t')

		available_seat = (string[t_index+1:i].strip())
		max_seat = (string[i+1:length].strip())
		if(available_seat.isdigit() and max_seat.isdigit()) :
			result.append((int(available_seat) , int(max_seat)))
	return result

def display(result) :
	sec = 1
	print datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M:%S%p")
	for s in result :
		print 'section {2} : {0}/{1}'.format(s[0],s[1],sec)
		sec = sec + 1
def main():

	course_code = input("Insert Course Code :")
	text = get_text(course_code)
	result = extract(text)

	f = open('courese{0}.log'.format(course_code), 'a+')

	# Prepate Elasticsearch Connection
	# es = econnector.connect()
	last_seat = []
	for i in range(len(result)) :
		last_seat.append(result[i][0])
		data = {
			"course_code" : course_code ,
			"section" : i+1, 
			"seat" : result[i][0],
			"max_seat" : result[i][1] ,
			"new_seat" : 0
		}
		log = '{0} :\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M:%S%p"),
												data['course_code'],
												data['section'],
												data['seat'],
												data['new_seat'],
												data['max_seat'])
		f.write(log)
		# econnector.put_doc(es , data)
	display(result)
	time.sleep(1)

	while 1 :
		text = get_text(course_code)
		result = extract(text)

		# Prepate Elasticsearch Connection
		# es = econnector.connect()
		for i in range(len(result)) :
			
			data = {
				"course_code" : course_code ,
				"section" : i+1, 
				"seat" : result[i][0],
				"max_seat" : result[i][1] ,
				"new_seat" : -last_seat[i] + result[i][0]
			}
			log = '{0} :\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M:%S%p"),
												data['course_code'],
												data['section'],
												data['seat'],
												data['new_seat'],
												data['max_seat'])
			f.write(log)
			# econnector.put_doc(es , data)
			last_seat[i] = result[i][0]

		display(result)
		time.sleep(1)		

if __name__ == '__main__':
	main()

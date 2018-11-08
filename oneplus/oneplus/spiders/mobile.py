# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
import re

def paramreturn(parameters, title):
	if(title in parameters):
		val = parameters[parameters.index(title)+1]
	else:
		val = ""

	return val

class MobileSpider(Spider):
	name = 'mobile'
	rotate_user_agent = True
	allowed_domains = ['mysmartprice.com']
	start_urls = ['http://www.mysmartprice.com/mobile/pricelist/oneplus-mobile-price-list-in-india.html']

	def parse(self, response):
		phones = response.xpath('//*[@class="prdct-item__img-wrpr"]/@href').extract()
		for phone in phones:
			absolute_url = response.urljoin(phone)
			yield Request(absolute_url, callback=self.parse_phone)

		#processing next pages
		next_page_url = response.xpath('//a[text()="Next"]/@href').extract_first()
		absolute_next_page_url = response.urljoin(next_page_url)
		yield Request(absolute_next_page_url)


	def parse_phone(self, response):

		name=display_size=display_prot=height=width=depth=weight=soft=b_no_of_camera=backcam=f_no_of_camera=frontcam=internal=ram=expandable=battery=chipset=architecture=cores=proc_make=frequency=gpu=price=""

		name = response.xpath('//*[@class="prdct-dtl__ttl"]/text()').extract_first()
		
		tech = response.xpath('//*[@class = "tchncl-spcftn__tbl-wrpr"]')

		features = tech[0].xpath('//*[@class="tchncl-spcftn__cptn"]/text()').extract()

		#Extracting display parameters of the phone
		if ('Display' in features):
			ind = features.index('Display')
			display = tech[ind].xpath('.//tbody/tr/td/text()').extract()
			
			if('Size (in inches)' in display):
				display_size = paramreturn(display, 'Size (in inches)')
				if(type(display_size) == str and display_size != ""):
					display_size = float(re.findall(r'\d+.\d+', display_size)[0])
			if('Protection' in display):
				display_prot = paramreturn(display, 'Protection')

		#Extracting Design and build features of the phone
		if ('Design and Build' in features):
			ind = features.index('Design and Build')
			dimension = tech[ind].xpath('.//tbody/tr/td')
			param_dim = tech[ind].xpath('.//tbody/tr/td/text()').extract()

			if('Dimensions' in param_dim):
				height = dimension.xpath('//*[@itemprop="height"]/text()').extract_first() 
				if(type(height) == str):
					height = re.findall(r'\d+.\d+|\d+',height)[0]
					height = float(height)

				width = dimension.xpath('//*[@itemprop="width"]/text()').extract_first() 
				if(type(width) == str):
					width = re.findall(r'\d+.\d+|\d+',width)[0]
					width = float(width)

				depth = re.findall(r'\d+.\d+|\d+', dimension.xpath('//*[@itemprop="depth"]/text()').extract_first())[0]
				if(type(depth) == str):
					depth = re.findall(r'\d+.\d+|\d+',depth)[0]
					depth = float(depth)

			if('Weight' in param_dim):
				weight = re.findall(r'\d+.\d+|\d+', dimension.xpath('//*[@itemprop="weight"]/text()').extract_first())[0]
				if(type(weight) == str):
					weight = re.findall(r'\d+.\d+|\d+',weight)[0]
					weight = float(weight)

		#Extracting software details of the phone
		if ('Software' in features):
			ind = features.index('Software')
			software = tech[ind].xpath('.//tbody/tr/td/text()').extract()
			soft = paramreturn(software, 'Operating System')

		#Extracting camera features of the phonr
		if ('Camera' in features):
			ind = features.index('Camera')
			camera = tech[ind].xpath('.//tbody/tr/td/text()').extract()
			
			backcam = paramreturn(camera, 'Primary ')
			if(type(backcam) == str and backcam != ""):
				#For finding the lens megapixels from the string
				bcam = re.findall(r'\d{1,2}\.?\d{0,2}', backcam)
				#Assigning no.of lenses
				b_no_of_camera = len(bcam)
				#Creating variable lens and assigning the string with 'cam 1'+'cam 2'+..+'cam n'
				blens = ""
				for items in bcam:
					blens = blens + items + '+'
				#Removing last '+'
				backcam = blens[:-1]

			frontcam = paramreturn(camera, 'Front')
			if(type(frontcam) == str and frontcam != ""):
				#For finding the lens megapixels from the string
				fcam = re.findall(r'\d+|\d+.\d', frontcam)
				#Assigning no.of lenses
				f_no_of_camera = len(fcam)
				#Creating variable lens and assigning the string with 'cam 1'+'cam 2'+..+'cam n'
				flens = ""
				for items in fcam:
					flens = flens + items + '+'
				#Removing last '+'
				frontcam = flens[:-1]

		#Extracting storage features of the phone
		if ('Storage' in features):
			ind = features.index('Storage')	
			storage = tech[ind].xpath('.//tbody/tr/td/text()').extract()
			
			internal = paramreturn(storage, 'Internal')
			if(type(internal) == str and internal != ""):
				if(len(re.findall('MB',internal))>0):
					internal = float(internal.split('MB')[0])
					internal = internal/1024.0

				elif(len(re.findall('GB',internal))>0):
					internal = float(internal.split('GB')[0])

			ram = paramreturn(storage, 'RAM') 
			if(type(ram) == str and ram != ""):
				if(len(re.findall('MB',ram))>0):
					ram = float(ram.split('MB')[0])
					ram = ram/1024.0

				elif(len(re.findall('GB',ram))>0):
					ram = float(ram.split('GB')[0])

			expandable = paramreturn(storage, 'Expandable')
			if(type(expandable) == str and expandable != ""):
				if(expandable != 'Yes'):
					if(expandable == 'No'):
						expandable = 0
					elif(len(re.findall(r'\d+', expandable)) > 0):
						expandable = re.findall(r'\d+', expandable)[0]
					

		#Extracting battery details of the phone
		if('Battery' in features):
			ind = features.index('Battery')
			battery = tech[ind].xpath('.//tbody/tr/td/text()').extract()

			capacity = paramreturn(battery, 'Capacity')
			if(type(capacity) == str and capacity != ""):
				capacity = capacity.split(' ')[0]
		
		#Extracting performance details of the phone
		if('Processor' in features):
			ind = features.index('Processor')
			per = tech[ind].xpath('.//tbody/tr/td/text()').extract()

			chipset = paramreturn(per, 'Chipset')
			architecture = paramreturn(per, 'Architecture')
			
			cores = paramreturn(per, 'No of Cores')
			if(type(cores) == str and cores!=""):
				cores = float(cores.split(' ')[0])
			
			proc_make = paramreturn(per, 'Make')
			
			frequency = paramreturn(per, 'Frequency')
			freq = re.findall(r'\d+.\d+|\d+',frequency)
			frequencies = ""
			for core in freq:
				frequencies = frequencies + core + '+'

			frequency = frequencies[:-1]

			gpu = paramreturn(per, 'GPU')

		#Extracting price of the device
		value = response.xpath('//*[@class="sctn__inr prc-grid__expctd-prc"]/p/text()|//*[@class="sctn__inr prc-grid__expctd-prc"]/text()').extract_first()
		exp = r'Rs. (\d+,{0,1}\d+)'
		price = re.findall(exp, value)[0]

		yield {
			'device_name' : name, 
			'display_size (inches)' : display_size,
			'display_prot' : display_prot,
			'height (inches)' : height,
			'width (inches)' : width,
			'depth (inches)' : depth,
			'weight (grams)' : weight,
			'os' : soft,
			'b_no_of_camera(s)' : b_no_of_camera,
			'backcam (megapixels)' : backcam,
			'f_no_of_camera(s)' : f_no_of_camera,
			'frontcam (megapixels)' : frontcam,
			'internal (GB)' : internal,
			'ram (GB)' : ram,
			'expandable (GB)' : expandable,
			'battery (mAh)' : capacity,
			'chipset' : chipset,
			'architecture' : architecture,
			'cores' : cores,
			'proc_make' : proc_make,
			'frequency (MHz)' : frequency,
			'gpu' : gpu,
			'price (INR)' : price
		}

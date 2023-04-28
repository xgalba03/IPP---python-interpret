#IPP 2. projekt 2020
#Author: Šimon Galba 
#login: xgalba03

import xml.etree.ElementTree as ET
import sys
import re
instrNumber = 0
callers = []
GF = {}
debug = 0
data_stack = []

def exit(code, msg):					#Na STDERR pošle požadovanú chybovú správu a ukončí interpret s príslušným kódom
		print("ERROR:",msg, file=sys.stderr)
		sys.exit(code)

def main():	#---------------------------------------- MAIN
	global debug
	
	if ((len(sys.argv) > 3) or (len(sys.argv) <= 1)):
		exit(10,"Zlý počet argumentov. Pre nápovedu použite: '--help'")
	if sys.argv[1] == "--help":
		if (len(sys.argv) != 2):
			exit(10,"Argument --help sa dá použiť len samostatne!")
		print_help()

	LF = None
	TF = None
	source_found = "no"
	input_found = 0 
	source_num = "no"
	input_num = 0
	source_path = "NOT_FOUND"
	file_path = "NOT_FOUND"

	for i in range(len(sys.argv)):
		if re.match('--source=', sys.argv[i]):
			source_found = "yes"
			source_num = i
			source_path = sys.argv[i][9:]
		if re.match('--input=', sys.argv[i]):
			input_found = "yes"
			input_num = i
			file_path = sys.argv[i][9:]


	if debug: print("Source:",source_found,"on:",source_num,"Input:",input_found,"on:",input_num)
	if debug: print("Source path:",source_path,"Input path:",file_path)

	try:
		tree = ET.parse(source_path)
	except IOError:
		exit(10, "Opening input file error")        
	except ET.ParseError:
		exit(31, "XML not well formed")        


	root = tree.getroot()   
	koren = root
	tree.write('output.xml')
	labels = {}
	global instrNumber

	if root.attrib["language"] != "IPPcode20":
		exit(32 ,"Zlý jazyk v XML dokumente")

	max = 0
	orders = []
	i = 0
	for instruction in root:		#nájde všetky labels a pridá ich do listu + ošetrí duplicidu order + záporné hodnoty order
		i+=1
		if instruction.tag != "instruction":
			exit(32 ,"Zlý tag instrukcie")
		if int(instruction.attrib["order"]) <= 0:
			exit(32 ,"Záporné poradie instrukcie")
		if instruction.attrib["order"] in orders:
			exit(32 ,"Duplikované poradie instruckie")
		orders.append(instruction.attrib["order"])
		if(int(instruction.attrib["order"]) > max):
			max = int(instruction.attrib["order"])			#max - zistím po akú hodnotu order má interpret vykonávať inštrukcie
		if(instruction.attrib["opcode"] in ['LABEL']):
			if instruction[0].text in labels:
				exit(52 ,"Redefinícia náveštia")
			labels[instruction[0].text] = int(instruction.attrib["order"])

	if debug: print(orders)
	if debug: print("LABELS DONE:",labels)		

	stop = False
	while(stop == False):			#.......... Hlavný cyklus programu - nájde inštrukciu a vykoná ju
		if debug: print("what")
		if instrNumber > max:
			stop = True
		found = 0
		for instruction in root:		
			order = instruction.attrib["order"]
			poradie = instrNumber 
			if int(order) == int(instrNumber+1):
				found = 1
				if debug: print("Execute instruction ",instruction.attrib["opcode"])
				if debug: print("execute instrNumber: ", instrNumber)
				if debug: print("Inštrukcia:",instruction,"opcode:",instruction.attrib["opcode"],"argc:",len(root),instrNumber)
				execute.execute_instruction(instruction,instruction.attrib["opcode"],len(root),labels,LF,TF)
				break
		if found != 1:
			instrNumber+=1	

	
	if debug: print(0,labels)
	if debug: print(GF)
	sys.exit(0)	#koniec intepretu (yay)


def print_help(): #funkcia na poskytnutie nápovedy na štandardný výstup
	print("This program interprets code in language IPPcode20 parsed to XML")
	print("Author: Simon Galba (xgalba03)")
	print("Usage:")
	print("python3.8 interpret.py --source=<path to .src>")
	sys.exit(0)

class execute():			
	global debug, data_stack
	def execute_instruction(instruction,opcode,argc,labels,local_frame,temp_frame):  #................ Hlavná funkcia na vykonávanie inštrukcií
		global instrNumber
		instrNumber+=1
		if debug: print("Vykonavam instrukciu",instruction)

		
		if opcode.upper() == 'MOVE':				# roztriedenie inštrukcií 
			execute.move(instruction)
			if debug: print("case MOVE")
		elif opcode.upper() == 'CREATEFRAME':
			if debug: print("case CREATEFRAME")
			execute.createframe(instruction, local_frame, temp_frame)
		elif opcode.upper() == 'POPFRAME':
			if debug: print("case POPFRAME")
		elif opcode.upper() == 'DEFVAR':
			execute.defvar(instruction, local_frame, temp_frame)
			if debug: print("case DEFVAR")
		elif opcode.upper() == 'CALL':
			execute.call(instruction,labels)
			if debug: print("case CALL")
		elif opcode.upper() == 'RETURN':
			execute._return(instruction)
			if debug: print("case RETURN")
		elif opcode.upper() == 'PUSHS':
			if debug: print("case PUSHS")
			execute.pushs(instruction)
		elif opcode.upper() == 'POPS':
			execute.pops(instruction)
			if debug: print("case POPS")
		elif opcode.upper() == 'ADD':
			execute.add(instruction)
			if debug: print("case ADD")
		elif opcode.upper() == 'SUB':
			execute.sub(instruction)
			if debug: print("case SUB")
		elif opcode.upper() == 'MUL':
			execute.mul(instruction)
			if debug: print("case MUL")
		elif opcode.upper() == 'IDIV':
			if debug: print("case IDIV")
			execute.idiv(instruction)
		elif opcode.upper() == 'LT':
			if debug: print("case LT")
		elif opcode.upper() == 'GT':
			if debug: print("case GT")
		elif opcode.upper() == 'EQ':
			if debug: print("case EQ")
		elif opcode.upper() == 'AND':
			if debug: print("case AND")
		elif opcode.upper() == 'OR':
			if debug: print("case OR")
		elif opcode.upper() == 'NOT':
			if debug: print("case NOT")
		elif opcode.upper() == 'INT2CHAR':
			if debug: print("case INT2CHAR")
			execute.int2char(instruction)
		elif opcode.upper() == 'STRI2INT':
			if debug: print("case STRI2INT")
		elif opcode.upper() == 'READ':
			if debug: print("case READ")
		elif opcode.upper() == 'WRITE':
			execute.write(instruction)
			if debug: print("case WRITE")
		elif opcode.upper() == 'CONCAT':
			if debug: print("case CONCAT")
		elif opcode.upper() == 'STRLEN':
			if debug: print("case STRLEN")
		elif opcode.upper() == 'GETCHAR':
			if debug: print("case GETCHAR")
		elif opcode.upper() == 'SETCHAR':
			if debug: print("case SETCHAR")
		elif opcode.upper() == 'TYPE':
			if debug: print("case TYPE")
			execute.type(instruction)
		elif opcode.upper() == 'LABEL':
			if debug: print("case LABEL")
		elif opcode.upper() == 'JUMP':
			execute.jump(instruction,labels)
			if debug: print("case JUMP")
		elif opcode.upper() == 'JUMPIFEQ':
			if debug: print("case JUMPIFEQ")
			execute.jump(instruction)
		elif opcode.upper() == 'JUMPIFNEQ':
			if debug: print("case JUMPIFNEQ")
		elif opcode.upper() == 'EXIT':
			execute.exit(instruction)
			if debug: print("case EXIT")
		elif opcode.upper() == 'DPRINT':
			execute.dprint(instruction)
			if debug: print("case DPRINT")
		elif opcode.upper() == 'BREAK':
			if debug: print("case BREAK")
		else:
			exit(32,"Neplaný operačný kód")

			#--------------------------- Spoločný komentár ADD SUB IDIV MUL
			# frame a name - frame je zistenie typu rámcu (GF/TF/LF) a name je názov premennej v nej
			#pre všetky 4 funckie sa pracuje len s typom int, preto rozsiahle kontroly goodtwo a goodone - potrebné pretypovanie 

	def add(instruction):		#sčítanie (3 argumenty)
		global GF
		if(instruction.find("arg1") == None) or (instruction.find("arg2") == None) or (instruction.find("arg2") == None) or (len(instruction) != 3):
			exit(32,"Zle zadaný argument")	

		destination = instruction.find("arg1")  
		frame = destination.text[:3]
		name = destination.text[3:]
		arg2 = instruction.find("arg2")
		arg3 = instruction.find("arg3")
		goodone = False
		goodtwo = False
		if debug: print(type(GF["var2"]))
		if debug: print(GF[arg3.text[3:]])

		if((arg2.attrib["type"] == "var") and (arg2.text[:3] == "GF@") and (arg2.text[3:] in GF) and (type(GF[arg2.text[3:]]) is int)):
			arg2.text = GF[arg2.text[3:]]
			goodtwo = True

		if((arg3.attrib["type"] == "var") and (arg3.text[:3] == "GF@") and (arg3.text[3:] in GF) and (type(GF[arg3.text[3:]]) is int)):
			arg3.text = GF[arg3.text[3:]]
			goodone = True

		if(arg3.attrib["type"] == "int"):
			try: 
				arg3.text = int(arg3.text)
			except:
				exit(32,"wrong int")
			goodone = True

		if(arg2.attrib["type"] == "int"):
			try: 
				arg2.text = int(arg2.text)
			except:
				exit(32,"wrong int")
			goodtwo = True

		if(goodtwo and goodone):	
			result = (arg2.text)+(arg3.text)
			if frame == "GF@":
				if name in GF:
					GF[name] = int(result)
				else:
					exit(54,"Nedefinovaná premenná")	
		else:		
			if debug: print(goodone,goodtwo,": ",arg3.attrib["type"] == "var",arg3.text[:3] == "GF@",arg3.text[3:] in GF,type(GF[arg3.text]))		
			exit(53,"Zle zadaný argument")

			#--------------------------- Spoločný komentár ADD SUB IDIV MUL
			# frame a name - frame je zistenie typu rámcu (GF/TF/LF) a name je názov premennej v nej
			#pre všetky 4 funckie sa pracuje len s typom int, preto rozsiahle kontroly goodtwo a goodone - potrebné pretypovanie 

	def mul(instruction):  	#násobenie (3 argumenty)
		global GF
		if(instruction.find("arg1") == None) or (instruction.find("arg2") == None) or (instruction.find("arg2") == None) or (len(instruction) != 3):
			exit(32,"Zle zadaný argument")	

		destination = instruction.find("arg1")
		frame = destination.text[:3]
		name = destination.text[3:]
		arg2 = instruction.find("arg2")
		arg3 = instruction.find("arg3")
		goodone = False
		goodtwo = False

		if((arg2.attrib["type"] == "var") and (arg2.text[:3] == "GF@") and (arg2.text[3:] in GF) and (type(GF[arg2.text[3:]]) is int)):
			arg2.text = GF[arg2.text[3:]]
			goodtwo = True

		if((arg3.attrib["type"] == "var") and (arg3.text[:3] == "GF@") and (arg3.text[3:] in GF) and (type(GF[arg3.text[3:]]) is int)):
			arg3.text = GF[arg3.text[3:]]
			goodone = True

		if(arg3.attrib["type"] == "int"):
			try: 
				arg3.text = int(arg3.text)
			except:
				exit(32,"wrong int")
			goodone = True

		if(arg2.attrib["type"] == "int"):
			try: 
				arg2.text = int(arg2.text)
			except:
				exit(32,"wrong int")
			goodtwo = True

		if(goodtwo and goodone):	
			result = (arg2.text)*(arg3.text)
			if frame == "GF@":
				if name in GF:
					GF[name] = int(result)
				else:
					exit(54,"Nedefinovaná premenná")	
		else:		
			if debug: print(goodone,goodtwo,": ",arg3.attrib["type"] == "var",arg3.text[:3] == "GF@",arg3.text[3:] in GF,type(GF[arg3.text]))		
			exit(53,"Zle zadaný argument")

			#--------------------------- Spoločný komentár ADD SUB IDIV MUL
			# frame a name - frame je zistenie typu rámcu (GF/TF/LF) a name je názov premennej v nej
			#pre všetky 4 funckie sa pracuje len s typom int, preto rozsiahle kontroly goodtwo a goodone - potrebné pretypovanie 
			
	def idiv(instruction):  	#delenie (3 argumenty)
		global GF
		if(instruction.find("arg1") == None) or (instruction.find("arg2") == None) or (instruction.find("arg2") == None) or (len(instruction) != 3):
			exit(32,"Zle zadaný argument")	

		goodone = False
		goodtwo = False
		destination = instruction.find("arg1")
		frame = destination.text[:3]
		name = destination.text[3:]
		arg2 = instruction.find("arg2")
		arg3 = instruction.find("arg3")

		if((arg2.attrib["type"] == "var") and (arg2.text[:3] == "GF@") and (arg2.text[3:] in GF) and (type(GF[arg2.text[3:]]) is int)):
			arg2.text = GF[arg2.text[3:]]
			goodtwo = True

		if((arg3.attrib["type"] == "var") and (arg3.text[:3] == "GF@") and (arg3.text[3:] in GF) and (type(GF[arg3.text[3:]]) is int)):
			arg3.text = GF[arg3.text[3:]]
			goodone = True

		if(arg3.attrib["type"] == "int"):
			try: 
				arg3.text = int(arg3.text)
			except:
				exit(32,"wrong int")
			goodone = True

		if(arg2.attrib["type"] == "int"):
			try: 
				arg2.text = int(arg2.text)
			except:
				exit(32,"wrong int")
			goodtwo = True

		if(arg3.text == 0):
			exit(57, "Delenie nulou")

		if(goodtwo and goodone):	
			result = (arg2.text)/(arg3.text)
			if frame == "GF@":
				if name in GF:
					GF[name] = int(result)
				else:
					exit(54,"Nedefinovaná premenná")	
		else:		
			if debug: print(goodone,goodtwo,": ",arg3.attrib["type"] == "var",arg3.text[:3] == "GF@",arg3.text[3:] in GF,type(GF[arg3.text]))		
			exit(53,"Zle zadaný argument")

			#--------------------------- Spoločný komentár ADD SUB IDIV MUL
			# frame a name - frame je zistenie typu rámcu (GF/TF/LF) a name je názov premennej v nej
			#pre všetky 4 funckie sa pracuje len s typom int, preto rozsiahle kontroly goodtwo a goodone - potrebné pretypovanie 
			
	def sub(instruction):	#odčítanie (3 argumenty)
		global GF
		if(instruction.find("arg1") == None) or (instruction.find("arg2") == None) or (instruction.find("arg2") == None) or (len(instruction) != 3):
			exit(32,"Zle zadaný argument")	

		destination = instruction.find("arg1")
		frame = destination.text[:3]
		name = destination.text[3:]
		arg2 = instruction.find("arg2")
		arg3 = instruction.find("arg3")
		goodone = False
		goodtwo = False

		if((arg2.attrib["type"] == "var") and (arg2.text[:3] == "GF@") and (arg2.text[3:] in GF) and (type(GF[arg2.text[3:]]) is int)):
			arg2.text = GF[arg2.text[3:]]
			goodtwo = True

		if((arg3.attrib["type"] == "var") and (arg3.text[:3] == "GF@") and (arg3.text[3:] in GF) and (type(GF[arg3.text[3:]]) is int)):
			arg3.text = GF[arg3.text[3:]]
			goodone = True

		if(arg3.attrib["type"] == "int"):
			try: 
				arg3.text = int(arg3.text)
			except:
				exit(32,"wrong int")
			goodone = True

		if(arg2.attrib["type"] == "int"):
			try: 
				arg2.text = int(arg2.text)
			except:
				exit(32,"wrong int")
			goodtwo = True

		if(goodtwo and goodone):	
			result = (arg2.text)-(arg3.text)
			if frame == "GF@":
				if name in GF:
					GF[name] = int(result)
				else:
					exit(54,"Nedefinovaná premenná")	
		else:		
			if debug: print(goodone,goodtwo,": ",arg3.attrib["type"] == "var",arg3.text[:3] == "GF@",arg3.text[3:] in GF,type(GF[arg3.text]))		
			exit(53,"Zle zadaný argument")

	def exit(instruction):		#ukončí interpet zo zadaným kódom
		if ((int(instruction[0].text) > 49) or (int(instruction[0].text) < 0)):
			exit(57, "Zadaná hodnota pre funkciu EXIT nie je v povolenom rozmedzí")
		sys.exit(int(instruction[0].text))		

	def jumpifeq(instruction):		#podmienený skok
		if debug: print("def jumpifeq")		

	def dprint(instruction):			#vypíše správu na STDERR
		print(instruction[0].text, file=sys.stderr)	

	def type(instruction):		#zistenie typu symbolu
		global GF
		arg2 = instruction.find("arg2")
		symbol = instruction.find("arg2").text
		var = instruction.find("arg1")
		name = var.text[3:]
		frame = var.text[:3]
		if debug: print("name: ",name,"frame: ",frame,"instance: ", type(symbol)==int,"symbol: ",type(symbol))
		if arg2.attrib["type"] == "var":		# v prípade, že symbol je premenná (práca s rámcami)
			if frame == "GF@":		
				symbol = GF[symbol[3:]]
				if debug: print(symbol)
			elif frame == "LF@":
				print("type LF not supported")
			elif frame == "TF@":
				print("type TF not supported")
			if symbol == None:
				if frame == "GF@":	
					GF[name] = "nil"
				elif frame == "LF@":
					print("type LF not supported")
				elif frame == "TF@":
					print("type TF not supported")
			elif isinstance(symbol, str) and symbol not in ['true', 'false'] or symbol == None:
				if frame == "GF@":	
					GF[name] = "string"
				elif frame == "LF@":
					print("type LF not supported")
				elif frame == "TF@":
					print("type TF not supported")
			elif isinstance(symbol, int):
				if frame == "GF@":	
					GF[name] = "int"
				elif frame == "LF@":
					print("type LF not supported")
				elif frame == "TF@":
					print("type TF not supported")
			elif isinstance(symbol, str):
				if frame == "GF@":	
					GF[name] = "bool"
				elif frame == "LF@":
					print("type LF not supported")
				elif frame == "TF@":
					print("type TF not supported")		
		else:								#symbol nie je premenná, práca s XML
			if debug: print("NOT VAR TYPE")
			if arg2.attrib["type"] == "string":
				if frame == "GF@":	
					GF[name] = "string"
				elif frame == "LF@":
					print("type LF not supported")
				elif frame == "TF@":
					print("type TF not supported")
			elif arg2.attrib["type"] == "int":
				if debug: print("INT TYPE")
				if frame == "GF@":	
					GF[name] = "int"
				elif frame == "LF@":
					print("type LF not supported")
				elif frame == "TF@":
					print("type TF not supported")
			elif arg2.attrib["type"] == "bool":
				if frame == "GF@":	
					GF[name] = "bool"
				elif frame == "LF@":
					print("type LF not supported")
				elif frame == "TF@":
					print("type TF not supported")		

	def int2char(instruction):			#pretypuje integer na char
		if debug: print("def int2char")
		global GF
		if(instruction.find("arg1") == None) or (instruction.find("arg2") == None):
			exit(99,"Nezadaný argument")
		symbol = instruction.find("arg2")
		symbol_type = symbol.attrib["type"]
		destination = instruction.find("arg1")
		name = destination.text[3:]
		frame = destination.text[:3]
		if frame == "GF@":
			if debug: print(GF[symbol.text[3:]])	
			if symbol_type == "var":
				GF[name] = chr(int(GF[symbol.text[3:]])) 
				if debug: print(GF[name])
		elif frame == "LF@":
			print("int2char LF not supported")
		elif frame == "TF@":
			print("int2char TF not supported")


	def pops(instruction):	#vyberie vrchnú hodnotu zo zásobníka a uloží do zadanej premennej
		global GF
		global data_stack
		if data_stack == []:
				exit(56,"Zásobník je prázdny.")
	
		if instruction[0].text[:3] == "GF@":
			if instruction[0].text[3:] in GF:
				if debug: print("POPS do GF")
				GF[instruction[0].text[3:]] = data_stack.pop()
				if debug: print("Popped: ",GF[instruction[0].text[3:]])		
		if debug:print(GF)
		if debug:print(data_stack)
		if debug:print(instruction[0].text[:3])

	def pushs(instruction):		#uloží zadanú hodnotu na vrch zásobníka
		global data_stack
		if debug: print("def pushs")
		if instruction[0].attrib["type"] != "var":
			data_stack.append(instruction[0].text)	
			if debug: print("Pushing: ",instruction[0].text,"Stack: ", data_stack)
		if 	instruction[0].attrib["type"] == "var":
			child = instruction.find("arg1")
			frame = child.text[:3]
			name = child.text[3:]
			if frame == "GF@":
				if name in GF:
					data_stack.append(instruction[0].text[3:])	
			elif frame == "LF@":
				#
				if debug: print("pushs")
			elif frame == "TF@":
				if debug: print("pushs")
		else: 
			data_stack.append(instruction[0].text)
				
	def createframe(instruction, temp_frame, local_frame):		#vytvorí rámec
		if debug: print("def createframe")
		local_frame = {}		

	def move(instruction):				# vloží hodnotu do premennej (práca s rámcami)
		if(instruction.find("arg1") == None) or (instruction.find("arg2") == None) or (len(instruction) > 2):
			exit(32,"Zle zadaný argument")
		symbol = instruction.find("arg2")
		symbol_type = symbol.attrib["type"]
		destination = instruction.find("arg1")
		frame = destination.text[:3]
		name = destination.text[3:]
		if symbol_type != "var":
			if symbol_type == "int":
				GF[name] = int(symbol.text)
			else:
				GF[name] = symbol.text
			 

	def defvar(instruction, local_frame, temp_frame):		#zadefinuje premennú v danom rámci
		if(len(instruction) != 1):
			exit(32,"Zle zadaný argument")
		global GF
		if debug: print(list(instruction))
		if debug: print(instruction.find("arg1") != None)
		if debug: print(instruction.find("arg1").attrib["type"])
		child = instruction.find("arg1")
		frame = child.text[:3]
		name = child.text[3:]
		if frame == "GF@":
			if name in GF:
				exit(52, "Redefinícia premennej")
			if debug: print("global frame")
			GF[name] = None
		elif frame == "LF@":
			if local_frame == None:
				exit(55, "Neexistujúci rámec")
			if debug: print("local frame")
		elif frame == "TF@":
			if temp_frame == None:
				exit(55, "Neexistujúci rámec")
			if debug: print("temporary frame")


		if debug: print("def defvar")

	def _return(instruction):		#vráti sa na poslednú inštrukciu 'call'
		global instrNumber
		global callers
		instrNumber = callers.pop()
		if debug: print("return num: ",instrNumber)

	def write(instruction):		#vypíše požadovanú správu či hodnotu na STDOUT
		global GF
		if(instruction.find("arg1") == None):
			exit(32,"Nezadaný argument")
		if instruction[0].attrib["type"] == "var":
			child = instruction.find("arg1")
			frame = child.text[:3]
			name = child.text[3:]
			if frame == "GF@":
				if name in GF and GF[name] != "nil":
					if debug: print("Write: ",GF[name])
					print(str(GF[name]),end='')
				if debug: print("global frame write")
			elif frame == "LF@":
				if debug: print("local frame write")
			elif frame == "TF@":
				if debug: print("temporary frame write")
		else:
			if instruction[0].attrib["type"] != "nil":
				print(instruction[0].text,end='')
				if debug: print(instruction[0].text)
				if debug: print("def write")

	def call(instruction,labels):			#zavolá inú inštrukciu
		global callers     
		callers.append(instrNumber)
		Labels.check_label(instruction[0].text,labels)
		if debug: print ("IN CALL:","tag:",instruction.tag,"atr:",instruction.attrib)
			
		if debug: print("def call")

	def jump(instruction,labels):
		Labels.check_label(instruction[0].text,labels)
		if debug: print ("IN JUMP:","tag:",instruction.tag,"atr:",instruction.attrib)
			
		if debug: print("def jump")


class Labels:		#spracovanie náveští
	global debug
		
	@classmethod
	def check_label(cls,name,labels):	#skontroluje či náveštie existuje, ak áno, mení poradie inštrukcií
		global instrNumber
		name = str(name)
		if name in labels:
			if debug: print("Skáčem na lebel:",name)
			instrNumber = labels[name]
			if debug: print("setting active inst to:", instrNumber)
			return 
		else:
			if debug: print("31", "LABEL",name,"doesnt exist in:",labels)      
main()
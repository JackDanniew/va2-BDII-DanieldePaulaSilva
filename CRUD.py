#coding: utf-8

from appJar import gui
import MySQLdb

#conexao = MySQLdb.connect("192.168.56.101", "aluno", "aluno2017", "mundo")


#cursor = conexao.cursor()

def usando(btn):
	
	global cursor
	
	global conexao

	h = login.getEntry("Host")
	u = login.getEntry("Usuário")
	s = login.getEntry("Senha")

	try: 
		conexao = MySQLdb.connect(h, u, s, "mundo")
		cursor = conexao.cursor()
	except MySQLdb.Error as err:
		print err
		

	login.stop()

login = gui("Login", "300x150")

login.addLabelEntry("Host")
login.addLabelEntry("Usuário")
login.addSecretLabelEntry("Senha")

login.addButton("Entrar", usando)

login.go()

app = gui("CRUD de MySQL", "600x300")

def pesquisar(btn):	
	termo = app.getEntry("txtBusca")
	if termo == '':
		app.errorBox("Erro", 'Informe um termo para pesquisar!')
	else:
		cursor.execute("SELECT Cidade.Nome, Estado.Nome FROM Cidade INNER JOIN Estado ON Estado.id = Cidade.Estado_id WHERE Cidade.Nome LIKE '%" + termo + "%'")

		rs = cursor.fetchall()	

		app.clearListBox("lBusca")

		for x in rs:
			app.addListItem("lBusca", "%s - %s" % (x[0],x[1]))

def exibir(btn):
	cursor.execute("SELECT Cidade.Nome, Estado.Nome, Pais.Nome FROM Cidade INNER JOIN Estado ON Estado.id = Cidade.Estado_id INNER JOIN Pais ON Pais.id = Estado.Pais_id")

	rs = cursor.fetchall()

	app.clearListBox("lBusca")

	for x in rs:
		app.addListItem("lBusca", "%s - %s / %s" % (x[0],x[1], x[2]))

def inserir(btn):
	
	app.showSubWindow('janela_inserir')

def salvar(btn):
	
	cidade = app.getEntry('txtcidade')
	idestado = app.getEntry('txtestado')
	cursor.execute("INSERT INTO Cidade (Nome, Estado_id) VALUES('{}',{})".format(cidade,idestado))

	app.hideSubWindow('janela_inserir') 


def excluir(btn):
	
	app.showSubWindow('janela_excluir')

def confirmar(btn):
	
	cidade = app.getEntry('cidadetxt')
	cursor.execute("DELETE FROM Cidade WHERE Nome = '{}'".format(cidade))

	app.hideSubWindow('janela_excluir')

def atualizar(btn):
	
	app.showSubWindow('janela_atualizar')

def ratificar(btn):
	
	cidade = app.getEntry('cidade')
	newcity = app.getEntry('novacity')
	cursor.execute("UPDATE Cidade SET Nome = '{}' WHERE Nome = '{}'".format(newcity, cidade))  

	app.hideSubWindow('janela_atualizar')


app.startSubWindow("janela_inserir", modal=True)
app.addLabel("l1", "Insira os Dados")
app.addEntry('txtestado')
app.addEntry('txtcidade')
app.addButton('Salvar',salvar)
app.setEntryDefault("txtestado", "ID do Estado")
app.setEntryDefault("txtcidade", "Nome da Cidade")
app.stopSubWindow()

app.startSubWindow("janela_excluir", modal=True)
app.addLabel("l2", "Informe qual dado deseja excluir")
app.addEntry('cidadetxt')
app.addButton('Deletar',confirmar)
app.setEntryDefault("cidadetxt", "Nome da Cidade")
app.stopSubWindow()

app.startSubWindow("janela_atualizar", modal=True)
app.addLabel("l3", "Informe qual dado deseja atualizar")
app.addEntry('cidade')
app.addEntry('novacity')
app.addButton('Atualizar', ratificar)
app.setEntryDefault("cidade", "Nome da Cidade")
app.setEntryDefault("novacity", "Nova Cidade")
app.stopSubWindow()

app.addLabel("lNome", '', 0,0,2)
app.addButton("Exibir dados", exibir, 1,0)
app.addButton("Inserir dados", inserir, 1,1)
app.addButton("Atualizar dados", atualizar, 2,0)
app.addButton("Excluir dados", excluir, 2,1)
app.addEntry("txtBusca", 3,0,2)
app.setEntryDefault("txtBusca", "Digite o termo...")
app.addButton("Pesquisar", pesquisar, 4,0,2)
app.addListBox("lBusca", [], 5,0,2)
app.setListBoxRows("lBusca", 5)

app.go()
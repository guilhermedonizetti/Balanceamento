from math import ceil


class Balanceamento:

    #Metodo construtor
    def __init__(self):
        self.ANTERIOR = []
        self.USUARIOS = []
        self.UMAX = 0


    def adicionar_usuario(self, atual):
        """Esse metodo adiciona novos usuarios nos servidores.
        O parametro 'atual' recebe a lista de usuarios divididos por servidor."""

        consumo = []
        tam_atu = len(atual)
        tam_ant = len(self.ANTERIOR)
        maior = max([tam_ant, tam_atu])
        
        #completar com 0 a menor lista para ficar com o mesmo tamanho que a maior.
        if tam_atu > tam_ant:
            for i in range(tam_atu):
                self.ANTERIOR.append(0)
        else:
            for i in range(tam_ant):
                atual.append(0)

        #incluir os novos usuarios somando com os usuarios anteriormente presentes
        sobra = 0
        for i in range(maior):
            soma = atual[i] + self.ANTERIOR[i] + sobra
            sobra = 0
            if soma > self.UMAX:
                consumo.append(self.UMAX)
                sobra = soma - self.UMAX
            else:
                consumo.append(soma)
        if sobra != 0:
            consumo.append(sobra)

        self.ANTERIOR = consumo #a lista atual de usuarios sera a ANTERIOR para a proxima insercao
        return consumo
        

    def inicio(self):
        """Esse metodo deve ser o unico metodo a ser chamado atraves da instancia da classe.
        Esse metodo chama adicionar_usuario, subtrair_usuario e mostrar_balanceamento sempre
        que necessario."""

        ttask = int(input()) #recebe o numero de ticks das tarefas
        self.UMAX = int(input()) #recebe o maximo de usuarios por servidor
        balanceamento = []
        contador = 0
        custo = 0
        tick = True

        x = True
        while x == True:
            try:
                entrada = int(input()) #ler o numero de usuarios por tick
                servidor = ceil(entrada / self.UMAX) #numero de servidores
                usuarios_ativos = []

                #se for necessario apenas 1 servidor para o(s) novo(s) usuario(s)...
                if servidor <= 1:
                    usuarios_ativos.append(entrada)
                #se for necessario mais de 1 servidor para o(s) novo(s) usuario(s)...
                else:
                    #distribuir os usuarios pela quantidade de servidores
                    for i in range(servidor):
                        decomposicao = entrada - self.UMAX
                        entrada = decomposicao
                        if decomposicao >= 0:
                            usuarios_ativos.append(self.UMAX)
                        else:
                            usuarios_ativos.append(decomposicao*(-1))
                
                self.USUARIOS.append(usuarios_ativos) #lista de usuarios por tick
                #somar usuarios que conectaram agora aos usuarios que continuam conectados
                resul = self.adicionar_usuario(usuarios_ativos)

                """Se o contador for maior ou igual que ttask, ja existe tarefas para encerrar"""
                if contador >= ttask:
                    tempo = contador - ttask
                    saida_usuarios = self.subtrair_usuario(resul, tick) #tirar usuarios de tarefas finalizadas
                    balanceamento.pop(tempo) #remove os usuarios ja desconectados
                else:
                    saida_usuarios = resul
    
                balanceamento.append(saida_usuarios) #incluir o balanceamento atual
                self.ANTERIOR = saida_usuarios
                self.mostrar_balanceamento(saida_usuarios) #mostrar balanceamento
                saida_usuarios = list(filter((0).__ne__, saida_usuarios)) #excluir servidores vazios
                custo = custo + len(saida_usuarios)
                contador = contador + 1

            except:
                x = False

                """Quando acabar a entrada de dados, o programa continua ate as tarefas encerrarem."""
                for i in self.USUARIOS:
                    tick = balanceamento[-1] #balanceamento anterior
                    saida_usuarios = self.subtrair_usuario(i, tick) #tirar usuarios de tarefas finalizadas
                    balanceamento.append(saida_usuarios) #incluir o balanceamento atual
                    self.mostrar_balanceamento(saida_usuarios)
                    saida_usuarios = list(filter((0).__ne__, saida_usuarios))
                    custo = custo + len(saida_usuarios)
                    contador = contador + 1
                
                print(custo)
    

    def subtrair_usuario(self, usu_ativos, tick=None):
        """Esse metodo remove remove do balanceamento atual os usuarios com tarefas finalizadas."""

        if tick == True:
            #condicao verdadeira se ainda existe entrada de dados
            usu_anterior = self.USUARIOS[0]
        else:
            usu_anterior = tick

        tam_anterior = len(usu_anterior)
        tam_ativo = len(usu_ativos)
        menor = min([tam_ativo, tam_anterior])
        sair = []

        #copiar a maior lista
        if len(usu_ativos) > len(usu_anterior):
            maior = usu_ativos
        else:
            maior = usu_anterior

        #criar uma nova lista com a diferenca entre:
        #a lista de usuarios que finalizaram suas tarefas e os que estao no balanceamento atual 
        for i in range(menor):
            maior_valor = max([usu_anterior[i], usu_ativos[i]])
            menor_valor = min([usu_anterior[i], usu_ativos[i]])
            sair.append(maior_valor - menor_valor)
        
        try:
            #fazer merge da lista SAIR com a maior lista
            for i in range(len(sair), len(maior)):
                sair.append(maior[i])
        except:
            pass

        #remover os usuarios que finalizaram as tarefas SE ainda houver entrada de dados
        if tick == True:
            self.USUARIOS.pop(0)
        
        if sum(sair) == 2:
            return [2]
        elif sum(sair) == 1:
            return [1]
        elif sum(sair) == 0:
            return [0]
        else:
            return sair
    

    def mostrar_balanceamento(self, usuarios):
        """Esse metodo formata a saida do programa, incluindo o resultado na mesma linha
        separa por virgula."""

        tam = len(usuarios)
        if tam == 1:
            print(usuarios[0])
        else:
            s = ""
            for i in range(tam):
                if i == tam - 1:
                    s = s + str(usuarios[i])
                else:
                    s = s + "{},".format(usuarios[i])
            print(s)


#Instanciar a classe
balanco = Balanceamento()
balanco.inicio()
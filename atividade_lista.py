#Crie uma lista com os nomes de 5 objetos
lista = ["mamão","mel","chocolate","banana","caramelo"]
print("lista criada")
#Adicione mais um objeto ao final da lista
lista.append("cebola")
print("objeto adicionado")
#Acesse o objeto que está na segunda posição
print(lista[1])
print("objeto da segunda posição listado")
#Remova um objeto da lista
lista.remove("caramelo")
print("objeto removido")
#Exiba o tamanho da lista
print(f"o tamanho da lista é {len(lista)}")
#Mostre todos os itens com um laço for
for item in lista:
    print(item)
#Verifique se 'cadeira' está na lista. Se sim remova-a, senão adicione
if "cadeira" in lista:
    lista.remove("cadeira")
    print("objeto removido")
else:
    lista.append("cadeira")
    print("objeto adicionado")
#Ordene a lista em ordem alfabética
lista.sort()
print("lista ordenada")
#Exiba o primeiro e o último objeto
print(lista[0],lista[-1])
print("objetos exibidos")
#Limpe toda a lista
lista.clear()
print("lista limpa")

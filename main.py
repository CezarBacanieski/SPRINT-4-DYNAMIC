import random
from datetime import datetime, timedelta
from collections import deque
import json

class Insumo:
    """Classe para representar um insumo médico"""
    def __init__(self, codigo, nome, categoria, quantidade, validade, unidade):
        self.codigo = codigo
        self.nome = nome
        self.categoria = categoria
        self.quantidade = quantidade
        self.validade = validade
        self.unidade = unidade
        self.timestamp = datetime.now()
    
    def __str__(self):
        return f"[{self.codigo}] {self.nome} - Qtd: {self.quantidade} {self.unidade} - Val: {self.validade}"
    
    def __repr__(self):
        return self.__str__()
    
    def to_dict(self):
        return {
            'codigo': self.codigo,
            'nome': self.nome,
            'categoria': self.categoria,
            'quantidade': self.quantidade,
            'validade': self.validade,
            'unidade': self.unidade,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }

class FilaConsumo:
    """Implementação de Fila (FIFO) para registro cronológico de consumo"""
    def __init__(self):
        self.fila = deque()
    
    def enfileirar(self, insumo):
        """Adiciona insumo na fila (final)"""
        self.fila.append(insumo)
        print(f"✓ Insumo enfileirado: {insumo.nome}")
    
    def desenfileirar(self):
        """Remove e retorna o primeiro insumo da fila"""
        if self.esta_vazia():
            print("⚠ Fila vazia!")
            return None
        return self.fila.popleft()
    
    def visualizar_frente(self):
        """Retorna o primeiro elemento sem remover"""
        if self.esta_vazia():
            return None
        return self.fila[0]
    
    def esta_vazia(self):
        return len(self.fila) == 0
    
    def tamanho(self):
        return len(self.fila)
    
    def listar_todos(self):
        """Lista todos os elementos da fila"""
        return list(self.fila)

class PilhaConsumo:
    """Implementação de Pilha (LIFO) para consultas em ordem inversa"""
    def __init__(self):
        self.pilha = []
    
    def empilhar(self, insumo):
        """Adiciona insumo no topo da pilha"""
        self.pilha.append(insumo)
        print(f"✓ Insumo empilhado: {insumo.nome}")
    
    def desempilhar(self):
        """Remove e retorna o insumo do topo"""
        if self.esta_vazia():
            print("⚠ Pilha vazia!")
            return None
        return self.pilha.pop()
    
    def visualizar_topo(self):
        """Retorna o elemento do topo sem remover"""
        if self.esta_vazia():
            return None
        return self.pilha[-1]
    
    def esta_vazia(self):
        return len(self.pilha) == 0
    
    def tamanho(self):
        return len(self.pilha)
    
    def listar_todos(self):
        """Lista todos os elementos da pilha"""
        return list(self.pilha)

class BuscaInsumos:
    """Implementação de algoritmos de busca"""
    
    @staticmethod
    def busca_sequencial(lista, codigo):
        """
        Busca sequencial - O(n)
        Percorre a lista elemento por elemento
        """
        comparacoes = 0
        for i, insumo in enumerate(lista):
            comparacoes += 1
            if insumo.codigo == codigo:
                print(f"✓ Busca Sequencial: Encontrado em {comparacoes} comparações")
                return i, insumo
        print(f"✗ Busca Sequencial: Não encontrado após {comparacoes} comparações")
        return -1, None
    
    @staticmethod
    def busca_binaria(lista, codigo):
        """
        Busca binária - O(log n)
        Requer lista ordenada por código
        """
        lista_ordenada = sorted(lista, key=lambda x: x.codigo)
        esquerda, direita = 0, len(lista_ordenada) - 1
        comparacoes = 0
        
        while esquerda <= direita:
            comparacoes += 1
            meio = (esquerda + direita) // 2
            
            if lista_ordenada[meio].codigo == codigo:
                print(f"✓ Busca Binária: Encontrado em {comparacoes} comparações")
                return meio, lista_ordenada[meio]
            elif lista_ordenada[meio].codigo < codigo:
                esquerda = meio + 1
            else:
                direita = meio - 1
        
        print(f"✗ Busca Binária: Não encontrado após {comparacoes} comparações")
        return -1, None

class OrdenacaoInsumos:
    """Implementação de algoritmos de ordenação"""
    
    @staticmethod
    def merge_sort(lista, chave='quantidade', ordem='desc'):
        """
        Merge Sort - O(n log n)
        Algoritmo estável de divisão e conquista
        """
        if len(lista) <= 1:
            return lista
        
        meio = len(lista) // 2
        esquerda = OrdenacaoInsumos.merge_sort(lista[:meio], chave, ordem)
        direita = OrdenacaoInsumos.merge_sort(lista[meio:], chave, ordem)
        
        return OrdenacaoInsumos._merge(esquerda, direita, chave, ordem)
    
    @staticmethod
    def _merge(esquerda, direita, chave, ordem):
        """Função auxiliar para mesclar duas listas ordenadas"""
        resultado = []
        i = j = 0
        
        while i < len(esquerda) and j < len(direita):
            valor_esq = getattr(esquerda[i], chave)
            valor_dir = getattr(direita[j], chave)
            
            if ordem == 'asc':
                if valor_esq <= valor_dir:
                    resultado.append(esquerda[i])
                    i += 1
                else:
                    resultado.append(direita[j])
                    j += 1
            else:  # desc
                if valor_esq >= valor_dir:
                    resultado.append(esquerda[i])
                    i += 1
                else:
                    resultado.append(direita[j])
                    j += 1
        
        resultado.extend(esquerda[i:])
        resultado.extend(direita[j:])
        return resultado
    
    @staticmethod
    def quick_sort(lista, chave='quantidade', ordem='desc'):
        """
        Quick Sort - O(n log n) médio, O(n²) pior caso
        Algoritmo in-place de divisão e conquista
        """
        if len(lista) <= 1:
            return lista
        
        pivo = lista[len(lista) // 2]
        valor_pivo = getattr(pivo, chave)
        
        if ordem == 'asc':
            menores = [x for x in lista if getattr(x, chave) < valor_pivo]
            iguais = [x for x in lista if getattr(x, chave) == valor_pivo]
            maiores = [x for x in lista if getattr(x, chave) > valor_pivo]
        else:  # desc
            menores = [x for x in lista if getattr(x, chave) > valor_pivo]
            iguais = [x for x in lista if getattr(x, chave) == valor_pivo]
            maiores = [x for x in lista if getattr(x, chave) < valor_pivo]
        
        return OrdenacaoInsumos.quick_sort(menores, chave, ordem) + iguais + OrdenacaoInsumos.quick_sort(maiores, chave, ordem)

class SistemaControleInsumos:
    """Sistema principal de controle de insumos"""
    
    def __init__(self):
        self.fila = FilaConsumo()
        self.pilha = PilhaConsumo()
        self.registro_completo = []
    
    def gerar_dados_simulados(self, quantidade=20):
        """Gera dados simulados de consumo de insumos"""
        print("\n" + "="*60)
        print("GERANDO DADOS SIMULADOS DE CONSUMO")
        print("="*60)
        
        categorias = ['Reagente', 'Descartável', 'Equipamento']
        insumos_nomes = {
            'Reagente': ['Hemograma', 'Glicose', 'Ureia', 'Creatinina', 'PCR'],
            'Descartável': ['Seringa 5ml', 'Luva P', 'Luva M', 'Luva G', 'Agulha'],
            'Equipamento': ['Tubo coleta', 'Lâmina', 'Swab', 'Álcool 70%', 'Algodão']
        }
        unidades = ['ml', 'un', 'cx', 'fr', 'pct']
        
        data_base = datetime.now()
        
        for i in range(quantidade):
            categoria = random.choice(categorias)
            nome = random.choice(insumos_nomes[categoria])
            codigo = f"INS{1000 + i}"
            quantidade_consumo = random.randint(10, 500)
            unidade = random.choice(unidades)
            dias_validade = random.randint(30, 365)
            validade = (data_base + timedelta(days=dias_validade)).strftime('%Y-%m-%d')
            
            insumo = Insumo(codigo, nome, categoria, quantidade_consumo, validade, unidade)
            insumo.timestamp = data_base - timedelta(hours=quantidade-i)
            
            self.fila.enfileirar(insumo)
            self.pilha.empilhar(insumo)
            self.registro_completo.append(insumo)
        
        print(f"\n✓ {quantidade} registros de consumo gerados com sucesso!")
    
    def demonstrar_fila(self):
        """Demonstra operações com fila"""
        print("\n" + "="*60)
        print("DEMONSTRAÇÃO - FILA (FIFO)")
        print("="*60)
        print(f"Tamanho da fila: {self.fila.tamanho()}")
        print(f"\nPrimeiro da fila: {self.fila.visualizar_frente()}")
        
        print("\n--- Desenfileirando 3 primeiros consumos ---")
        for i in range(3):
            item = self.fila.desenfileirar()
            if item:
                print(f"{i+1}. {item}")
    
    def demonstrar_pilha(self):
        """Demonstra operações com pilha"""
        print("\n" + "="*60)
        print("DEMONSTRAÇÃO - PILHA (LIFO)")
        print("="*60)
        print(f"Tamanho da pilha: {self.pilha.tamanho()}")
        print(f"\nTopo da pilha: {self.pilha.visualizar_topo()}")
        
        print("\n--- Desempilhando 3 últimos consumos ---")
        for i in range(3):
            item = self.pilha.desempilhar()
            if item:
                print(f"{i+1}. {item}")
    
    def demonstrar_buscas(self):
        """Demonstra algoritmos de busca"""
        print("\n" + "="*60)
        print("DEMONSTRAÇÃO - ALGORITMOS DE BUSCA")
        print("="*60)
        
        if not self.registro_completo:
            print("⚠ Nenhum registro disponível")
            return
        
        # Buscar um código existente
        codigo_busca = self.registro_completo[len(self.registro_completo)//2].codigo
        print(f"\nBuscando código: {codigo_busca}")
        
        print("\n--- Busca Sequencial ---")
        idx_seq, insumo_seq = BuscaInsumos.busca_sequencial(self.registro_completo, codigo_busca)
        if insumo_seq:
            print(f"Resultado: {insumo_seq}")
        
        print("\n--- Busca Binária ---")
        idx_bin, insumo_bin = BuscaInsumos.busca_binaria(self.registro_completo, codigo_busca)
        if insumo_bin:
            print(f"Resultado: {insumo_bin}")
    
    def demonstrar_ordenacao(self):
        """Demonstra algoritmos de ordenação"""
        print("\n" + "="*60)
        print("DEMONSTRAÇÃO - ALGORITMOS DE ORDENAÇÃO")
        print("="*60)
        
        # Merge Sort por quantidade (decrescente)
        print("\n--- Merge Sort (Por Quantidade Consumida) ---")
        lista_merge = OrdenacaoInsumos.merge_sort(
            self.registro_completo.copy(), 
            chave='quantidade', 
            ordem='desc'
        )
        print("Top 5 insumos mais consumidos:")
        for i, insumo in enumerate(lista_merge[:5], 1):
            print(f"{i}. {insumo}")
        
        # Quick Sort por validade (crescente)
        print("\n--- Quick Sort (Por Data de Validade) ---")
        lista_quick = OrdenacaoInsumos.quick_sort(
            self.registro_completo.copy(), 
            chave='validade', 
            ordem='asc'
        )
        print("Top 5 insumos com validade mais próxima:")
        for i, insumo in enumerate(lista_quick[:5], 1):
            print(f"{i}. {insumo}")
    
    def gerar_relatorio_completo(self):
        """Gera relatório completo do sistema"""
        print("\n" + "="*60)
        print("RELATÓRIO COMPLETO DO SISTEMA")
        print("="*60)
        
        print(f"\nTotal de registros: {len(self.registro_completo)}")
        print(f"Registros na fila: {self.fila.tamanho()}")
        print(f"Registros na pilha: {self.pilha.tamanho()}")
        
        # Estatísticas por categoria
        categorias = {}
        for insumo in self.registro_completo:
            if insumo.categoria not in categorias:
                categorias[insumo.categoria] = []
            categorias[insumo.categoria].append(insumo.quantidade)
        
        print("\n--- Consumo por Categoria ---")
        for cat, quantidades in categorias.items():
            total = sum(quantidades)
            media = total / len(quantidades)
            print(f"{cat}: Total={total}, Média={media:.2f}, Registros={len(quantidades)}")
        
        # Alertas de validade
        print("\n--- Alertas de Validade (próximos 60 dias) ---")
        data_limite = (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d')
        alertas = [i for i in self.registro_completo if i.validade <= data_limite]
        if alertas:
            for insumo in alertas[:5]:
                print(f"⚠ {insumo}")
        else:
            print("✓ Nenhum alerta de validade")

def main():
    """Função principal de demonstração"""
    print("="*60)
    print("SISTEMA DE CONTROLE DE INSUMOS - DASA")
    print("Desafio FIAP - Estruturas de Dados")
    print("="*60)
    
    # Inicializar sistema
    sistema = SistemaControleInsumos()
    
    # Gerar dados simulados
    sistema.gerar_dados_simulados(20)
    
    # Demonstrações
    sistema.demonstrar_fila()
    sistema.demonstrar_pilha()
    sistema.demonstrar_buscas()
    sistema.demonstrar_ordenacao()
    sistema.gerar_relatorio_completo()
    
    print("\n" + "="*60)
    print("EXECUÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*60)

if __name__ == "__main__":
    main()
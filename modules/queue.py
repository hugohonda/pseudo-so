# fila global - filas devem suportar no máximo 1000 processos

# fila de processos de tempo real - FIFO sem preempção

# fila de processos de usuários - múltiplas filas de prioridades com realimentação
#   - três filas com prioridades distintas
class Queue:
    def __init__(self, priority):
        self.fila = []
        self.priority = priority

class queue_interface:
    
    def __init__(self, queue, priority):
        self.real_time = new Queue(0)
        self.user_p1 = new Queue(1)
        self.user_p2 = new Queue(2)
        self.user_p3 = new Queue(3)

    def add_to_queue(self, process):
        if(process.priority == 0):
            self.real_time.append(process)
        elif(process.priority == 1):
            self.user_p1.fila.append(process)
        elif(process.priority == 2):
            self.user_p2.fila.append(process)
        elif(process.priority == 3):
            self.user_p3.fila.append(process)
    
    def pop_in_priority_order(self):
        if(self.real_time != []):
            return self.real_time.fila.pop()
        if(self.user_p1 != []):
            return self.user_p1.fila.pop()
        if(self.user_p2 != []):
            return self.user_p2.fila.pop()
        if(self.user_p3 != []):
            return self.user_p3.fila.pop()

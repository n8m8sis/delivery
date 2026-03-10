import random
import heapq
from collections import deque

class DeliverySimulator:
    def __init__(self, num_couriers, lambda_orders=30, avg_delivery_time=25, sim_time=480):
        self.num_couriers = num_couriers
        self.lambda_orders = lambda_orders / 60
        self.avg_delivery_time = avg_delivery_time
        self.sim_time = sim_time
        
        self.couriers = [{'id': i, 'available': True, 'busy_until': 0} 
                        for i in range(num_couriers)]
        self.order_queue = deque()
        self.event_queue = []
        
        self.total_orders = 0
        self.completed_orders = 0
        self.total_wait_time = 0
        self.courier_busy_time = [0] * num_couriers
        self.delayed_orders = 0
        
        first_order_time = random.expovariate(self.lambda_orders)
        heapq.heappush(self.event_queue, (first_order_time, 'new_order', None))
    
    def run(self):
        current_time = 0
        
        while current_time < self.sim_time and self.event_queue:
            current_time, event_type, order_id = heapq.heappop(self.event_queue)
            
            if event_type == 'new_order':
                self._process_new_order(current_time)
            elif event_type == 'delivery_complete':
                self._process_delivery_complete(current_time, order_id)
        
        return self._calculate_metrics()
    
    def _process_new_order(self, current_time):
        self.total_orders += 1
        order_id = self.total_orders
        
        available_courier = None
        for courier in self.couriers:
            if courier['available'] and courier['busy_until'] <= current_time:
                available_courier = courier
                break
        
        if available_courier:
            self._assign_order(available_courier, order_id, current_time, 0)
        else:
            self.order_queue.append({'id': order_id, 'arrival_time': current_time})
        
        next_order_time = current_time + random.expovariate(self.lambda_orders)
        if next_order_time < self.sim_time:
            heapq.heappush(self.event_queue, (next_order_time, 'new_order', None))
    
    def _assign_order(self, courier, order_id, current_time, wait_time):
        courier['available'] = False
        delivery_time = random.expovariate(1/self.avg_delivery_time)
        courier['busy_until'] = current_time + delivery_time
        self.courier_busy_time[courier['id']] += delivery_time
        
        if wait_time > 10:
            self.delayed_orders += 1
        self.total_wait_time += wait_time
        
        heapq.heappush(self.event_queue, 
                      (current_time + delivery_time, 'delivery_complete', courier['id']))
    
    def _process_delivery_complete(self, current_time, courier_id):
        courier = self.couriers[courier_id]
        self.completed_orders += 1
        
        if self.order_queue:
            next_order = self.order_queue.popleft()
            wait_time = current_time - next_order['arrival_time']
            self._assign_order(courier, next_order['id'], current_time, wait_time)
        else:
            courier['available'] = True
    
    def _calculate_metrics(self):
        avg_wait = self.total_wait_time / self.completed_orders if self.completed_orders > 0 else 0
        avg_util = (sum(self.courier_busy_time) / (self.num_couriers * self.sim_time)) * 100
        salary = self.num_couriers * (self.sim_time / 60) * 200
        penalty = self.delayed_orders * 50
        total = salary + penalty
        
        return {
            'num_couriers': self.num_couriers,
            'avg_wait_time': round(avg_wait, 2),
            'avg_utilization': round(avg_util, 2),
            'delayed_orders': self.delayed_orders,
            'total_cost': round(total, 2)
        } 

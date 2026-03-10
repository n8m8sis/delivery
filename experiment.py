from simulator import DeliverySimulator

print("Запуск эксперимента по оптимизации количества курьеров")
print("=" * 50)

results = []

for n in range(5, 16):
    print(f"Тестируем {n} курьеров...")
    runs = []
    for _ in range(5):
        sim = DeliverySimulator(num_couriers=n)
        runs.append(sim.run())
    
    avg = {
        'n': n,
        'wait': sum(r['avg_wait_time'] for r in runs) / len(runs),
        'util': sum(r['avg_utilization'] for r in runs) / len(runs),
        'cost': sum(r['total_cost'] for r in runs) / len(runs)
    }
    results.append(avg)

print("\n" + "=" * 60)
print(f"{'Курьеров':^10} | {'Время ожидания':^16} | {'Загрузка':^10} | {'Затраты':^12}")
print("=" * 60)
for r in results:
    print(f"{r['n']:^10} | {r['wait']:^16.2f} | {r['util']:^10.2f} | {r['cost']:^12.2f}")
print("=" * 60)

# Находим оптимальное количество
optimal = min(results, key=lambda x: x['cost'])
print(f"\n✅ Оптимальное количество курьеров: {optimal['n']}")
print(f"   Время ожидания: {optimal['wait']} мин")
print(f"   Затраты: {optimal['cost']} руб")

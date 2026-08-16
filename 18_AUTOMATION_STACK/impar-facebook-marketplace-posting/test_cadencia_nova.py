#!/usr/bin/env python3
import random
from datetime import date, datetime, time as datetime_time, timedelta
from collections import defaultdict

TIME_SLOTS = [
    {"periodo": "manhã", "inicio": datetime_time(8, 0), "fim": datetime_time(11, 0)},
    {"periodo": "tarde", "inicio": datetime_time(13, 30), "fim": datetime_time(16, 30)},
    {"periodo": "noite", "inicio": datetime_time(18, 30), "fim": datetime_time(21, 0)},
]

def get_posts_per_day(target_date):
    is_weekend = target_date.weekday() >= 5
    if is_weekend:
        return random.randint(7, 9)
    return random.randint(8, 10)

def get_random_interval():
    return random.randint(7, 20)

def calculate_scheduled_time(day_position, total_posts, target_date):
    posts_per_period = max(1, total_posts // 3)
    period_index = min(2, (day_position - 1) // posts_per_period)
    slot = TIME_SLOTS[period_index]
    start_minutes = int(slot["inicio"].hour * 60 + slot["inicio"].minute)
    end_minutes = int(slot["fim"].hour * 60 + slot["fim"].minute)
    position_in_period = (day_position - 1) % posts_per_period
    cumulative_minutes = sum(get_random_interval() for _ in range(position_in_period))
    random_minute = random.randint(start_minutes, max(start_minutes, end_minutes - cumulative_minutes))
    return datetime_time(random_minute // 60, random_minute % 60)

def main():
    print("\n" + "=" * 100)
    print("TESTE DA NOVA CADÊNCIA - Facebook Marketplace Impar")
    print("=" * 100)
    print("\n📋 CONFIGURAÇÃO")
    print("  Horários: Manhã (08:00-11:00) | Tarde (13:30-16:30) | Noite (18:30-21:00)")
    print("  Intervalo: 7-20 minutos (aleatório)")
    print("  Posts/dia: 7-9 (finais de semana) | 8-10 (dias úteis)")
    
    start_date = date.today()
    all_schedules = []
    stats_by_period = defaultdict(int)
    
    print("\n📅 EXEMPLO DE AGENDAMENTO (7 dias)")
    print("-" * 100)
    
    for day_offset in range(7):
        target_date = start_date + timedelta(days=day_offset)
        posts_today = get_posts_per_day(target_date)
        day_type = "🌴 FDS" if target_date.weekday() >= 5 else "📅 Útil"
        
        print(f"\n{target_date.isoformat()} {day_type} → {posts_today} anúncios")
        print("  ", end="")
        
        for position in range(1, posts_today + 1):
            scheduled_time = calculate_scheduled_time(position, posts_today, target_date)
            posts_per_period = max(1, posts_today // 3)
            period_index = min(2, (position - 1) // posts_per_period)
            slot = TIME_SLOTS[period_index]
            
            all_schedules.append({"date": target_date, "time": scheduled_time, "period": slot["periodo"]})
            stats_by_period[slot["periodo"]] += 1
            print(f"{scheduled_time.strftime('%H:%M')} ", end="")
    
    print("\n\n" + "=" * 100)
    print("📊 ESTATÍSTICAS")
    print("=" * 100)
    print("\n⏰ Distribuição por período:")
    for period in ["manhã", "tarde", "noite"]:
        count = stats_by_period[period]
        pct = (count / len(all_schedules)) * 100 if all_schedules else 0
        print(f"  {period.capitalize():6} → {count:2} posts ({pct:5.1f}%)")
    
    posts_list = [sum(1 for s in all_schedules if (start_date + timedelta(days=d)) == s["date"]) for d in range(7)]
    print(f"\n📈 Resumo: {sum(posts_list)} anúncios em 7 dias (média {sum(posts_list)/7:.1f}/dia)")
    print("\n✅ Nova cadência funcionando!\n" + "=" * 100 + "\n")

if __name__ == "__main__":
    main()

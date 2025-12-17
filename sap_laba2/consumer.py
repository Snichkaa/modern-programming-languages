#ПРИНИМАЕТ И СОХРАНЯЕТ ДАННЫЕ
from kafka import KafkaConsumer
import json
import psycopg2
import psycopg2.extras

#Определяем тип данных
def get_column_type(values):
    non_null = [v for v in values if v is not None]
    
    if not non_null:
        return "TEXT"
    
    if all(isinstance(v, bool) for v in non_null):
        return "BOOLEAN"
    
    if all(isinstance(v, int) for v in non_null):
        return "BIGINT"
    
    if all(isinstance(v, (int, float)) for v in non_null):
        return "DOUBLE PRECISION"
    
    return "TEXT"

#Подключаем к Kafka
consumer = KafkaConsumer(
    "tables_topic",
    bootstrap_servers=["localhost:9092"],
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

#Подключаемся к PostgreSQL
conn = psycopg2.connect(
    dbname="user_db",
    user="admin",
    password="1234",
    host="localhost",
    port=5434
)
cur = conn.cursor()

print("Consumer started. Waiting for data...")

#Цикл ожидания
for msg in consumer:
    #Извлекаем данные из сообщения:
    data = msg.value
    table = data["table"]
    columns = data["columns"]
    rows = data["rows"]
    
    #Создаём словарь для сбора всех значений каждой колонки
    column_values = {c: [] for c in columns}
    
    #Собираем все значения по колонкам, проходим по каждой строке и каждой колонке
    for row in rows:
        for i in range(len(columns)):
            col = columns[i]
            val = row[i]
            column_values[col].append(val)
    
    #Определяем тип для каждой колонки, собираем в список
    column_defs = []
    for c in columns:
        pg_type = get_column_type(column_values[c])
        column_defs.append(f"{c} {pg_type}")
    
    #SQL команда для создания таблицы
    sql_create = f"""
        CREATE TABLE IF NOT EXISTS {table} (
            id SERIAL PRIMARY KEY,
            {", ".join(column_defs)}
        );
    """
    #Выполняем SQL команду
    cur.execute(sql_create)
    
    #Вставка данных
    sql_insert = f"INSERT INTO {table} ({', '.join(columns)}) VALUES %s"
    
    #Ошибки
    try:
        psycopg2.extras.execute_values(cur, sql_insert, rows)
        conn.commit()
        print(f"Inserted {len(rows)} rows into '{table}'")
        
    except psycopg2.errors.UndefinedColumn:
        conn.rollback()
        print(f"Columns mismatch in '{table}'. Skipping.")
        continue
        
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        continue
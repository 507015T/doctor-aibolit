### DB

## 2) creating table

```sql
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE TABLE developers(
id UUID PRIMARY KEY,
name VARCHAR(255),
department VARCHAR(255),
geolocation GEOMETRY(POINT, 4326),
last_known_ip INET,
is_available BOOLEAN
);
```

## 3) Creating 20 records

Постарался добавить около рандом

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
INSERT INTO developers(id, name, department, geolocation, last_known_ip, is_available)
SELECT uuid_generate_v4() as id,
	((ARRAY['James', 'Mary', 'James', 'John', 'Robert', 'Patrica', 'Robert'])[floor(random() * 5 + 1)] || ' ' ||
	(ARRAY['Smith', 'Johnson', 'Williams', 'Brown', 'Jones'])[floor(random() * 5 + 1)]) as name,
	(ARRAY['backend','backend', 'backend', 'frontend', 'ios', 'ios', 'android'])[floor(random() * 7 + 1)] as department,
    ST_SetSRID(ST_MakePoint(
        19.5 + random() * 3.0,
        54.3 + random() * 1.0
    ), 4326) as geolocation,
	inet(concat_ws('.', floor(random() * 253)::int, floor(random() * 256)::int, floor(random() * 256)::int, floor(random() * 254)::int)) AS last_known_ip,
	random() < 0.7 as is_available
FROM generate_series(1, 20);
```

# SELECT \* FROM developers;

"0957de1a-69e1-4a77-bcb0-4a698401bb9a" "Robert Jones" "backend" "0101000020E6100000F7DA184450F33440A7618B20BF334B40" "109.163.136.215" true
"d1adcbd5-7a70-4f68-83b3-36c415c8331e" "James Johnson" "ios" "0101000020E6100000280E6C79A711354091885CC64E274B40" "208.80.116.146" false
"cc8cf2e6-eb54-4358-98bd-8a3ecf2aeb7e" "Robert Smith" "backend" "0101000020E6100000A8D16406AA4D3440CE101C373F4D4B40" "158.14.176.29" false
"0c320502-e99c-4dcd-a541-e67e8acecc0e" "James Jones" "frontend" "0101000020E61000000B3FEBCF3B71354009E2D8029E524B40" "56.93.233.136" true
"d6b7f7b4-5d27-4f71-8704-4bdcd8d07022" "James Williams" "frontend" "0101000020E6100000D5A82F1337ED3440FD793A00E69F4B40" "144.155.110.14" false
"110e9048-4885-4eba-80fe-b87703a3c933" "James Smith" "backend" "0101000020E6100000AD5EFC0E39A9354045C4CDA8EA4A4B40" "73.188.0.223" true
"4d576352-04a8-4b0c-bd46-78408b862494" "Robert Jones" "backend" "0101000020E6100000E4F32010EF3A35402C668A326C8E4B40" "4.12.50.199" false
"4ac3ccfd-b2e7-4cda-a795-697a8d1c8d2d" "James Smith" "frontend" "0101000020E6100000F324F16468EB3540717122F9D9984B40" "131.50.217.47" true
"dd70e9b2-e933-4526-a340-5472ac727008" "James Johnson" "backend" "0101000020E61000001E0364C36AB133401547E9CE2B9C4B40" "226.247.151.21" true
"c0cb81c7-9db2-4964-9980-4abc31fdba2a" "Mary Brown" "backend" "0101000020E61000005DD1DEC3E31836406BA507672F634B40" "115.121.7.204" true
"4629ec7b-6722-4164-a1f9-64cf92d54f79" "Mary Brown" "backend" "0101000020E6100000784B713830F434401D2C8DD1C5554B40" "137.32.109.165" true
"129be56c-5806-4a3c-af3d-45401b87108c" "James Smith" "backend" "0101000020E6100000D383A94C238D33407122A82CFE3F4B40" "177.191.156.218" true
"2edcf089-5ba0-46dc-bfea-b56f47155d2b" "James Williams" "backend" "0101000020E61000002E4CE85B26E033409D8C716FB9634B40" "87.87.225.240" true
"0eeeb956-e1d9-491c-9ae9-fc1c12bbb1f4" "Robert Williams" "ios" "0101000020E6100000BAA6CCDB44A233400FB5AEB0D3874B40" "231.151.242.9" true
"df7dfa8f-207b-40f6-bee7-687c4ebfcbdd" "James Brown" "backend" "0101000020E6100000B1B6FBF3973634404D5C2B9ACC984B40" "57.120.248.179" true
"02c3d267-b460-4dbf-a985-fd45371f91bf" "James Williams" "ios" "0101000020E6100000424877859A4C364082090A1D86464B40" "86.252.6.153" true
"d7638cdf-5e23-4601-85cd-83f3f79d98d3" "Mary Johnson" "backend" "0101000020E6100000CED5981A93CE33405074A26E4F774B40" "170.124.205.120" false
"aae158f5-a824-4b15-9190-dbf61d8154ce" "Robert Smith" "backend" "0101000020E61000007989CCF7DFAB334070ED3B04D93D4B40" "56.79.72.120" false
"02fee06e-7ed5-440c-b7df-f30c2dd0035b" "Robert Williams" "backend" "0101000020E6100000D6767F189E8235401FA0053BC3A24B40" "95.20.19.153" true
"bea77172-6747-4faf-97f6-0a48635ffcc9" "Robert Johnson" "ios" "0101000020E61000003390DA6BE6C93340C138843080524B40" "106.166.252.108" true

3)[Задание со здездочкой](./script.sql)

```sql
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE TABLE if NOT EXISTS developers(
id UUID PRIMARY KEY,
name VARCHAR(255),
department VARCHAR(255),
geolocation GEOMETRY(POINT, 4326),
last_known_ip INET,
is_available BOOLEAN
);
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
INSERT INTO developers(id, name, department, geolocation, last_known_ip, is_available)
SELECT uuid_generate_v4() as id,
	((ARRAY['James', 'Mary', 'James', 'John', 'Robert', 'Patrica', 'Robert'])[floor(random() * 5 + 1)] || ' ' ||
	(ARRAY['Smith', 'Johnson', 'Williams', 'Brown', 'Jones'])[floor(random() * 5 + 1)]) as name,
	(ARRAY['backend','backend', 'backend', 'frontend', 'ios', 'ios', 'android'])[floor(random() * 7 + 1)] as department,
	ST_SetSRID(ST_MakePoint(random() * 360 - 180, random() * 180 - 90), 4326) as geolocation,
	inet(concat_ws('.', floor(random() * 256)::int, floor(random() * 256)::int, floor(random() * 256)::int, floor(random() * 256)::int)) AS last_known_ip,
	random() < 0.7 as is_available

FROM generate_series(1, (floor(random() * (10000 - 1000 + 1)) + 1000)::int);
```

## 4)

всего 7981 записей

- first
  **input**:

    ```sql
    EXPLAIN(ANALYZE, BUFFERS) SELECT * FROM developers WHERE name LIKE 'James%';
    ```

    **output**:
    "Bitmap Heap Scan on developers (cost=61.34..239.40 rows=4005 width=74) (actual time=0.268..1.727 rows=4005 loops=1)"
    " Filter: ((name)::text ~~ 'James%'::text)"
    " Heap Blocks: exact=128"
    " Buffers: shared hit=133"
    " -> Bitmap Index Scan on idx_developers_name_pattern (cost=0.00..60.34 rows=4005 width=0) (actual time=0.225..0.226 rows=4005 loops=1)"
    " Index Cond: (((name)::text ~>=~ 'James'::text) AND ((name)::text ~<~ 'Jamet'::text))"
    " Buffers: shared hit=5"
    "Planning Time: 0.113 ms"
    "Execution Time: 2.094 ms"

- second
  **input**:

    ```sql
    EXPLAIN(ANALYZE, BUFFERS) SELECT * FROM developers WHERE department = 'backend';
    ```

    **output**:
    "Seq Scan on developers (cost=0.00..202.76 rows=3441 width=74) (actual time=0.014..1.099 rows=3441 loops=1)"
    " Filter: ((department)::text = 'backend'::text)"
    " Rows Removed by Filter: 4540"
    " Buffers: shared hit=103"
    "Planning Time: 0.069 ms"
    "Execution Time: 1.314 ms"

- third
  **input**:
    ```sql
    EXPLAIN(ANALYZE, BUFFERS) SELECT * FROM developers WHERE last_known_ip = '192.168.1.10';
    ```
    **output**:
    "Seq Scan on developers (cost=0.00..251.78 rows=1 width=74) (actual time=1.443..1.444 rows=0 loops=1)"
    " Filter: (last_known_ip = '192.168.1.10'::inet)"
    " Rows Removed by Filter: 9902"
    " Buffers: shared hit=128"
    "Planning:"
    " Buffers: shared hit=5"
    "Planning Time: 0.127 ms"
    "Execution Time: 1.461 ms"
- forth
  **input**:

    ```sql
    EXPLAIN(ANALYZE, BUFFERS) SELECT * FROM developers WHERE is_available = TRUE;
    ```

    **output**:
    "Seq Scan on developers (cost=0.00..227.02 rows=6912 width=74) (actual time=0.015..1.455 rows=6912 loops=1)"
    " Filter: is_available"
    " Rows Removed by Filter: 2990"
    " Buffers: shared hit=128"
    "Planning Time: 0.079 ms"
    "Execution Time: 1.854 ms"

- fifth
  **input**:

    ```sql
      EXPLAIN(ANALYZE, BUFFERS)
      SELECT *
      FROM developers
      WHERE ST_DWithin(
          geolocation::geography,
          ST_SetSRID(ST_MakePoint(20.4522, 54.7104), 4326)::geography,
          10000
      );
    ```

    **output**:
    "Seq Scan on developers (cost=0.00..124026.77 rows=1 width=74) (actual time=0.172..26.016 rows=151 loops=1)"
    " Filter: st_dwithin((geolocation)::geography, '0101000020E61000004F401361C3733440098A1F63EE5A4B40'::geography, '10000'::double precision, true)"
    " Rows Removed by Filter: 9751"
    " Buffers: shared hit=128"
    "Planning Time: 0.105 ms"
    "Execution Time: 26.047 ms"

Задание со звездочкой

```sql
SELECT *
FROM developers
WHERE ST_DWithin(
    geolocation::geography,
    ST_SetSRID(ST_MakePoint(20.4522, 54.7104), 4326)::geography,
    10000
);
```

## 5)

### Индексация name

Если это какая-то внутренняя таблица разработчиков, то вряд ли будет кто-то искать по имени
Если это какой-то публичный каталог с поиском по имени(мб какая-то соц.сеть для разработчиков),
то добавить индекс будет уместно, добавим для проверки работы explain

**Запрос**:

```sql
CREATE INDEX idx_developers_name_pattern ON developers(name text_pattern_ops);
```

### Индексация department

Однозначно да, это база, искать по направлению разрабов самое то.

**Запрос**:

```sql
CREATE INDEX idx_developers_department ON developers(department);
```

### Индексация по geolocation

Да, для поиска в ближайшем округе.

```sql
CREATE INDEX idx_developers_geolocation ON developers USING GIST(geolocation);
```

### Индексация по last_known_ip

Я думаю неуместно по причине уже индексированной geolocation. Обычно, если необходимо найти разработчиков,
мы смотрим поблизости, а это мы сможем через geolocation. Но в контексте текущего задания, чтобы проверить
работу explain до и после индексирования можно добавить.

```sql
CREATE INDEX idx_developers_ip ON developers(last_known_ip);
```

### Индексация по is_available

Низкая селективность. Индекс будет сканироваться почти польностью. Но можно добавить для true, если мы
часто фильтруем по нему

```sql
CREATE INDEX idx_developers_available_true ON developers(is_available) WHERE is_available = TRUE;
```

## 6)

- first
  **input**:

    ```sql
    EXPLAIN(ANALYZE, BUFFERS) SELECT * FROM developers WHERE name LIKE 'James%';
    ```

    **output**:
    "Bitmap Heap Scan on developers (cost=61.34..239.40 rows=4005 width=74) (actual time=0.162..1.191 rows=4005 loops=1)"
    " Filter: ((name)::text ~~ 'James%'::text)"
    " Heap Blocks: exact=128"
    " Buffers: shared hit=133"
    " -> Bitmap Index Scan on idx_developers_name_pattern (cost=0.00..60.34 rows=4005 width=0) (actual time=0.137..0.137 rows=4005 loops=1)"
    " Index Cond: (((name)::text ~>=~ 'James'::text) AND ((name)::text ~<~ 'Jamet'::text))"
    " Buffers: shared hit=5"
    "Planning:"
    " Buffers: shared hit=15 read=1"
    "Planning Time: 0.300 ms"
    "Execution Time: 1.431 ms"

- second
  **input**:

    ```sql
    EXPLAIN(ANALYZE, BUFFERS) SELECT * FROM developers WHERE department = 'backend';
    ```

    **output**:
    "Bitmap Heap Scan on developers (cost=42.95..188.96 rows=3441 width=74) (actual time=0.140..0.723 rows=3441 loops=1)"
    " Recheck Cond: ((department)::text = 'backend'::text)"
    " Heap Blocks: exact=103"
    " Buffers: shared hit=107"
    " -> Bitmap Index Scan on idx_developers_department (cost=0.00..42.09 rows=3441 width=0) (actual time=0.119..0.119 rows=3441 loops=1)"
    " Index Cond: ((department)::text = 'backend'::text)"
    " Buffers: shared hit=4"
    "Planning Time: 0.093 ms"
    "Execution Time: 0.935 ms"

- third
  **input**:
    ```sql
    EXPLAIN(ANALYZE, BUFFERS) SELECT * FROM developers WHERE last_known_ip = '192.168.1.10';
    ```
    **output**:
    "Index Scan using idx_developers_ip on developers (cost=0.29..8.30 rows=1 width=74) (actual time=0.029..0.030 rows=0 loops=1)"
    " Index Cond: (last_known_ip = '192.168.1.10'::inet)"
    " Buffers: shared read=2"
    "Planning:"
    " Buffers: shared hit=19 read=1"
    "Planning Time: 0.354 ms"
    "Execution Time: 0.048 ms"
- forth
  **input**:

    ```sql
    EXPLAIN(ANALYZE, BUFFERS) SELECT * FROM developers WHERE is_available = TRUE;
    ```

    **output**:
    "Seq Scan on developers (cost=0.00..227.02 rows=6912 width=74) (actual time=0.010..1.487 rows=6912 loops=1)"
    " Filter: is_available"
    " Rows Removed by Filter: 2990"
    " Buffers: shared hit=128"
    "Planning:"
    " Buffers: shared hit=16 read=1"
    "Planning Time: 0.283 ms"
    "Execution Time: 1.889 ms"

- fifth
  **input**:

    ```sql
    EXPLAIN(ANALYZE, BUFFERS)
    SELECT *
    FROM developers
    WHERE ST_DWithin(
        geolocation::geography,
        ST_SetSRID(ST_MakePoint(20.4522, 54.7104), 4326)::geography,
        10000
    );
    ```

    **output**:
    "Seq Scan on developers (cost=0.00..124026.77 rows=1 width=74) (actual time=0.181..24.693 rows=151 loops=1)"
    " Filter: st_dwithin((geolocation)::geography, '0101000020E61000004F401361C3733440098A1F63EE5A4B40'::geography, '10000'::double precision, true)"
    " Rows Removed by Filter: 9751"
    " Buffers: shared hit=128"
    "Planning Time: 0.141 ms"
    "Execution Time: 24.721 ms"

ощутимого прироста на текущих данных дало только установка индексирования к айпи
"public" "developers" "idx_developers_name_pattern" "CREATE INDEX idx_developers_name_pattern ON public.developers USING btree (name text_pattern_ops)"
"public" "developers" "idx_developers_department" "CREATE INDEX idx_developers_department ON public.developers USING btree (department)"
"public" "developers" "idx_developers_ip" "CREATE INDEX idx_developers_ip ON public.developers USING btree (last_known_ip)"
"public" "developers" "idx_developers_available_true" "CREATE INDEX idx_developers_available_true ON public.developers USING btree (is_available) WHERE (is_available = true)"
"public" "developers" "idx_developers_geolocation" "CREATE INDEX idx_developers_geolocation ON public.developers USING gist (geolocation)"


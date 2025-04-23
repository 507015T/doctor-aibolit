
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS developers (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    department VARCHAR(255),
    geolocation GEOMETRY(POINT, 4326),
    last_known_ip INET,
    is_available BOOLEAN
);

TRUNCATE developers;

INSERT INTO developers(id, name, department, geolocation, last_known_ip, is_available)
SELECT 
    uuid_generate_v4() as id,
	((ARRAY['James', 'Mary', 'James', 'John', 'Robert', 'Patrica', 'Robert'])[floor(random() * 5 + 1)] || ' ' ||
	(ARRAY['Smith', 'Johnson', 'Williams', 'Brown', 'Jones'])[floor(random() * 5 + 1)]) as name,
	(ARRAY['backend','backend', 'backend', 'frontend', 'ios', 'ios', 'android'])[floor(random() * 7 + 1)] as department,
    ST_SetSRID(ST_MakePoint(
        19.5 + random() * 3.0,
        54.3 + random() * 1.0
    ), 4326) as geolocation,
    CASE 
        WHEN random() < 0.01 THEN NULL
        ELSE inet(
            concat_ws('.', 
                (floor(random() * 253) + 1)::int, 
                (floor(random() * 256))::int, 
                (floor(random() * 256))::int, 
                (floor(random() * 254) + 1)::int
            )
        )
    END AS last_known_ip,
    random() < 0.7 as is_available
FROM generate_series(1, (floor(random() * (10000 - 1000 + 1)) + 1000)::int);

ANALYZE developers;


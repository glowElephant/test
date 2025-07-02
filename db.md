## DB 구조 요약

### 1. users  
- **목적**: 유저 정보 및 포인트 보유량 관리  
- **컬럼**  
  - `id` (PK, SERIAL)  
  - `point_balance` (INTEGER, NOT NULL, DEFAULT 0)  

### 2. characters  
- **목적**: 커스터마이징 가능한 캐릭터 템플릿 정보  
- **컬럼**  
  - `id` (PK, SERIAL)  
  - `name` (VARCHAR(100), NOT NULL)  
  - `intro` (TEXT, NULLABLE)  

### 3. user_characters  
- **목적**: 특정 유저가 보유한 캐릭터 인스턴스  
- **컬럼**  
  - `id` (PK, SERIAL)  
  - `user_id` (FK → users.id, NOT NULL)  
  - `character_id` (FK → characters.id, NOT NULL)  

### 4. packages  
- **목적**: 캐릭터별 커스터마이징 패키지(테마)  
- **컬럼**  
  - `id` (PK, SERIAL)  
  - `character_id` (FK → characters.id, NOT NULL)  
  - `name` (VARCHAR(150), NOT NULL)  
  - `thumbnail_url` (VARCHAR(500), NOT NULL)  
  - `description` (TEXT, NULLABLE)  

### 5. patch_groups  
- **목적**: 캐릭터 파츠 종류(부위 그룹)  
- **컬럼**  
  - `id` (PK, SERIAL)  
  - `character_id` (FK → characters.id, NOT NULL)  
  - `name` (VARCHAR(50), NOT NULL)  

### 6. items  
- **목적**: 각 패키지·파츠 그룹의 꾸밈용 아이템  
- **컬럼**  
  - `id` (PK, SERIAL)  
  - `package_id` (FK → packages.id, NOT NULL)  
  - `patch_group_id` (FK → patch_groups.id, NOT NULL)  
  - `name` (VARCHAR(100), NOT NULL)  
  - `price` (INTEGER, NOT NULL, DEFAULT 50)  
  - `metadata` (JSONB, NULLABLE)  
  - `original_image_url` (VARCHAR(500), NOT NULL)  
  - `web_image_url` (VARCHAR(500), NOT NULL)  
  - `is_default` (BOOLEAN, NOT NULL, DEFAULT FALSE)  
- **제약**  
  - `UNIQUE(package_id, patch_group_id) WHERE is_default = TRUE`  
    → 패키지×파츠당 기본 아이템은 하나만  

### 7. user_character_customizations  
- **목적**: 유저 캐릭터 인스턴스별 장착 상태  
- **컬럼**  
  - `user_character_id` (PK, FK → user_characters.id, NOT NULL)  
  - `patch_group_id` (PK, FK → patch_groups.id, NOT NULL)  
  - `item_id` (FK → items.id, NOT NULL)  
- **제약**  
  - `PRIMARY KEY(user_character_id, patch_group_id)`  
    → 파츠당 하나만 장착  
  - `FOREIGN KEY(patch_group_id, item_id) REFERENCES items(patch_group_id, id)`  
    → 올바른 부위–아이템 매칭  

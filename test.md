## 1. 개발 과제 목적

- AI 활용한 프로토타이핑, 쉽게 말하면 "https://www.lab.twenty.style/custom" 구현

## 2. 와이어 프레임 및 기능 설명

### (0) 용어 설명

- 캐릭터 - 패키지를 등록할 캐릭터, 하나의 캐릭터에 여러 패키지를 등록할 수 있음
- 패키지 - 하나의 꾸미기 세트 (여러 파츠와 아이템으로 구성되어 있음)
- 파츠 - 패키지 내 아이템 그룹 (e.g. 머리, 몸통, 손, 발 등)
- 아이템 - 한 파츠에 속해 있는 아이템 (e.g. 머리 파츠 > 단발 머리, 포니테일, 만두 머리 등)
- 포인트 - 아이템 구매시 사용되는 재화

### (1) 크리에이터 페이지

- 페이지 이동 :
    - 패키지 리스트 페이지 → 패키지 등록 or 확인 페이지 → 캐릭터 생성 및 등록 페이지
    - 패키지를 등록하고 나면, 리스트에서 각 패키지 상태 확인 가능 (e.g. 심사 대기, 심사 중, …)
- 캐릭터 등록할 때 입력값 :
    - 캐릭터 대표 이미지, 캐릭터 이름, 캐릭터 소개
- 패키지 등록할 때 입력값 :
    - 패키지 대표 이미지, 패키지 이름, 패키지 파일(폴더 통째로 업로드)

![IMG_0672.jpg](attachment:a88efec1-a929-4c12-82ab-fbd700606421:IMG_0672.jpg)

### (2) 패키지 상태 관리

- 패키지 등록이 완료되면, 관리자가 심사 진행
- 패키지 상태 변경 예시 :
    - 심사대기 → 심사중 → 승인 보류 → 삭제
    - 심사대기 → 심사중 → 승인 완료(=판매 중) → 판매 중단
- 패키지 삭제 :
    - 패키지 삭제할 수 있는 상태는 오직 2개 - ‘심사대기’ or ‘승인 보류’

### (3) 캐릭터 꾸미기 페이지

- 페이지 이동 :
    - 판매 중인 패키지 리스트 페이지 →  캐릭터 꾸미기 화면(아이템 구매 가능) → 배경화면 다운로드 화면
- 아이템 구매 기능
    - 유저가 포인트를 사용해서 아이템을 구매 → 캐릭터를 꾸밀 수 있음
- 프로토타이핑 편의상 가정한 조건
    - 모든 아이템 가격은 10포인트로 가정, 유저에게는 1000포인트 충전 되었다고 가정
    - 구매 전에는 아이템 착용 불가 (아이템 구매 후, 아이템 착용 가능)

![IMG_0673.jpg](attachment:780b5089-363f-487c-87ff-e3d744b7a881:IMG_0673.jpg)

### (4) 이미지 관리 및 보안

- 업로드된 이미지 관리
    - 꾸미기용 이미지와 POD 상품 제작용 이미지는 나눠서 관리해야 함
        - 고퀄리티 원본 이미지는 POD 업체에게만 제공되어야 함
        - 유저에게는 꾸미기용 해상도 이미지만 보여줌
- 해상도 관리:
    - 꾸미기용 이미지 : 웹/앱 최적화 해상도 (WebP 형식, 300-500KB 이하)
    - POD 상품 제작용: 고해상도 원본 (4000x4000px 이상, 300dpi)
    - 배경화면 저장용 : 중간 해상도 (2000x2000px, 72dpi)
- 이미지 파일명:
    - 시스템에서 자동 생성된 고유 ID로 변경하여 저장 (원본 파일명 보존 불필요)

### (5) 프로토타입 구현 범위 아님

- 회원 가입 관련 기능 (크리에이터, 유저 모두 회원 가입 되어있다고 가정)
- 다국어 지원 기능 (한국어로만 샘플 데이터 제공)
- POD 업체의 이미지 접근 권한 관리 (POD 업체에서 유저가 주문 접수한 이미지만 다운로드 가능)
- 연령/국가에 따른 콘텐츠 접근 관리
- 서버/프론트 테스트 코드 작성
- 포인트 충전, 환불 기능
- 아이템 할인, 환불 기능

## 3. 평가

### (1) 평가 항목

1. DB - SQL 설계
    1. 실제 서버에 적용될 수 있는 수준으로 테이블 및 컬럼 설계
    2. (DB, 트래픽) 확장성과 보안이 고려되어야 함
2. 서버 - 일반적인 프로토콜 계층 정의 및 관리 (동시성 처리) 
3. 프런트 - AI가 작성한 UI 코드 보고 판단해서 구현할 수 있는지 확인

### (2) 평가 방법

1. 프론트 시연
    1. A,B 캐릭터 생성 및 등록 → ‘판매 중’ 상태 변경
        1. 패키지 상태에 따른 UI 반영 확인
    2. A,B 캐릭터 꾸미기
    3. 배경화면 저장하기
2. DB 설계에 대한 질의 응답
3. 백엔드 핵심 코드 리뷰
    1. 서버 프로토콜 계층 설계에 대한 질의 응답

# fashion drops access dynamodb API v1.01

[TOC]

## /*
- Request: GET, POST, PUT, DELETE
- Response, Success : 200 (OK with contents)
- Response, Fail : 400(Bad Request)

## /health

서버 상태를 반환한다.	`Done`
- Request: GET
- Response: 200
```json
{
	"status": "healthy"
}
```

## /create
dynamoDB 테이블을 생성한다. 이미 있는 테이블의 경우 테이블과 연결을 시도한다.
- Request: GET
* Usage
http://54.65.178.128:5000/accessfdrops/api/v1/create

- Response: 200(OK)
```json
{
	"status": "success",
}
```
- Fail: 400 with error message
```json
{
	"error": "error message"
}
```

## /drop
dynamoDB 테이블과 데이터를 모두 삭제한다.
- Request: GET
* Usage
http://54.65.178.128:5000/accessfdrops/api/v1/drop

- Response: 200(OK)
```json
{
	"status": "success",
}
```
- Fail: 400 with error message
```json
{
	"error": "error message"
}
```

## /malls
쇼핑몰에 대한 정보를 가져온다.	`Done`

- Request: GET

* Usage
http://54.65.178.128:5000/accessfdrops/api/v1/malls?limit=10
http://54.65.178.128:5000/accessfdrops/api/v1/malls?mallname=StyleNanda

* Argument
mallname : 쇼핑몰이름 (주어지지 않으면 모든 데이터 조회)
limit : 아이템 개수 (주어지지 않으면 10)

- Response: 200
```json
{
	"result" : [
    	{
            "name": "stylenanda",
            "desc": "유니크, 모던시크, 캐쥬얼, 여성의류 브랜드쇼핑몰, 드레스, 스냅백 등 판매.",
            "InsertDateTime": 1432539814,
            "Timer": 1000
        },
        ...
    ]
}
```
- Fail: 409 with errmsg
```json
{
	"error" : "error message"
}
```

쇼핑몰 정보를 입력한다.	`Done`

* Sample code
python access_crawled/sample/sample.py --table=mall

- Request : POST
```json
{
	"malls" : [
    	{
            "name": "stylenanda",
            "desc": "유니크, 모던시크, 캐쥬얼, 여성의류 브랜드쇼핑몰, 드레스, 스냅백 등 판매.",
            "InsertDateTime": 1432539814,
            "Timer": 1000
        },
        ...
    ]
}
```

- Response: 200
```json
{
	"result" : {
    	"success" : 10,
        "fail" : 2
    }
}
```

- Fail : 401 with error message
```json
{
	"error" : "error message"
}
```


## /products
상품에 대한 정보를 가져온다.	`Done`

- Request: GET

* Usage
http://54.65.178.128:5000/accessfdrops/api/v1/products?limit=10
http://54.65.178.128:5000/accessfdrops/api/v1/products?mallname=StyleNanda
http://54.65.178.128:5000/accessfdrops/api/v1/products?mallname=StyleNanda&code=xxxTEST
http://54.65.178.128:5000/accessfdrops/api/v1/products?category=formal

* Argument
mallname : 쇼핑몰이름
code : 상품코드 (startswith 검색)
category : 대표 카테고리명
limit : 아이템 개수 (주어지지 않으면 10)
mallname과 category가 둘 다 주어지지 않은 경우 전체데이터 조회

- Response: 200
```json
{
	"result" : [
    	{
            "MallName": "StyleNanda",
            "Code": "fake_product_data_2",
            "CategoryMain": "Formal",
            "CategoryAll": ["Female", "Formal", "dress"],
            "Name": "yyy skirt",
            "Price": 50000,
            "Url": "http://stylenanda.com/front/php/product.php?product_no=136714&main_cate_no=53&display_group=1",
            "ImageUrl": "http://file2.stylenanda.com/web/upload6/150519_02_hy.jpg",
            "InsertDateTime": 1432534920
        },
        ...
    ]
}
```
- Fail: 409 with errmsg
```json
{
	"error" : "error message"
}
```

상품 정보를 입력한다.	`Done`

* Sample code
python access_crawled/sample/sample.py --table=product

- Request : POST
```json
{
	"products" : [
    	{
            "MallName": "StyleNanda",
            "Code": "fake_product_data_2",
            "CategoryMain": "Formal",
            "CategoryAll": ["Female", "Formal", "dress"],
            "Name": "yyy skirt",
            "Price": 50000,
            "Url": "http://stylenanda.com/front/php/product.php?product_no=136714&main_cate_no=53&display_group=1",
            "ImageUrl": "http://file2.stylenanda.com/web/upload6/150519_02_hy.jpg",
            "InsertDateTime": 1432534920
        },
        ...
    ]
}
```

- Response: 200
```json
{
	"result" : {
    	"success" : 10,
        "fail" : 2
    }
}
```

- Fail : 401 with error message
```json
{
	"error" : "error message"
}
```

# CoClub API v1.01

[TOC]

## /*
- Request: GET, POST, PUT, DELETE
- Response, Success : 200 (OK with contents), 201 (created), 204 (OK with no contents)
- Response, Fail : 400(Bad Request), 401(Unauthorized), 403(Forbidden), 404(Not Found), 409(Conflict with errmsg)

## /corps

회사 리스트를 반환한다.	`Done`
- Request: GET
- Response: 200
```json
{
	"corps": [
    	{
      		"corp_domain": "kt.com",
      		"corp_id": 11,
      		"corp_name": "KT"
    	},
    	{
      		"corp_domain": "kt.com",
      		"corp_id": 12,
      		"corp_name": "KTH"
    	}
    ]
}
```

## /health

서버 상태를 반환한다.	`Done`
- Request: GET
- Response: 200
```json
{
	"status": "healthy"
}
```

## /emails
{email}로 등록된 사용자가 있다면, 등록된 사용자 정보를 반환한다.
- Request: GET **/emails/{email}**
- Response: 200(OK) or 404(Not Found):{email}에 해당하는 사용자가 없을경우
```json
{
	"name": "강소라",
    "nickname": "안영이"
}
```
- Fail: 400(Bad Request)


passcode를 생성하여, 사용자 이메일로 발송한다
- Request: POST **/emails/{email}/passcodes**
- Response: 201(Created)
- Fail: 4xx

사용자가 입력한 passcode의 유효성을 검증한다.
- Request: GET **/emails/{email}/passcodes/{passcode}**
- Response: 204(No Content)
- Fail: 409(Conflict) with errmsg
```json
{
	"errmsg": "Invalid passcode"
}
```

## /users
사용자를 추가한다. 추가가 되면 user ID를 반환한다.	`Done`
- Request: POST
```json
{
	"email": "sora@navercorp.com",
    "corp_id": 11,
    "password": "encrypted_string",
    "name": "강소라",
	"nickname": "안영이",
    "device_token": "abcdef101010101zcdefd3839"
}
```
- Response: 201
```json
{
	"user_id": 1001,
	"lounge_club_id": 44,
    "onedayclass_club_id": 45
}
```
- Fail: 409 with errmsg

내 정보를 수정하거나 추가한다. (my_id는 cookie를 통해 전달된다)
- Request: PUT (수정될 항목만 key:value쌍으로 전달한다.)
```json
{
	"email": "sora@navercorp.com",
    "password": "encrypted_string",
    "name": "강소라",
	"nickname": "안영이",
    "device_token": "abcdef101010101zcdefd3839"
}
```
- Response: 204
- Fail: 401(Unauthorized) or 409 with errmsg

사용자 정보를 반환한다.
- Request: GET **/users/{user_id}**
- Response: 200
```json
{
	"user_id": 224,
	"name": "강소라",
    "nickname": "안영이",
	"email": "sora@navercorp.com",
    "corp_id": 11,
	"corp_name": "네이버",
	"lounge_club_id": 44,
    "onedayclass_club_id": 45
}
```
- Fail: 404

User가 가입한 club과 가입 가능한 club들을 반환한다.
가입 가능한 club들의 경우, role_type이 'guest'로 표시된다.	`Done`
- Request: GET **/users/{user_id}/clubs?start=1&display=10**
- Response: 200
```json
{
	"club_cnt": 1,
	"clubs": [
    	{
        	"club_id": 222,
       		"club_name": "우크렐레 초급반",
      		"club_description": "목요일 점심, 2층 커넥트홀에서 우크렐레 배워요",
          	"member_cnt": 25,
         	"max_member_cnt": "30 or null",
         	"role_type": "member or leader or founder or guest",
        	"founder_id": 225,
       		"founder_name": "임시완",
      		"founder_nickname": "장그래",
			"create_time": "UNIXTIMESTAMP of 20141231010102",
			"start_date": "UNIXTIMESTAMP of 20150101000000 or null",
            "end_date": "UNIXTIMESTAMP of 20150630235959 or null"
        }
	]
}
```


## /clubs
내가 속한 회사의 클럽을 생성한다.	`Done`
- Request: GET
- Response: 200
```json
{
  "club_id": 1,
  "club_name": "네이버 보드게임 동호회",
  "club_description": "한달에 한번 오프라인 모임에서 다 함께 보드게임",
  "club_type": 1,
  "member_cnt": 3,
  "max_member_cnt": 3 or null,
  "start_date": "unixtimestamp or null",
  "end_date": "timestamp or null"
}
```

내가 속한 회사의 클럽을 생성한다.	`Done`
- Request: POST
```json
{
	"club_name": "네이버 보드게임 동호회",
    "club_description": "한달에 한번 오프라인 모임에서 다 함께 보드게임",
  	"start_date": "20150101 or null",
 	"end_date": "20150401 or null",
	"max_member_cnt": 3 or null,
}
```
- Response: 201
```json
{
	"club_id": 224
}
```

내가 운영진인 회사의 클럽 정보를 수정한다.
- Request: PUT **/clubs/{club_id}** (수정이 필요한 항목만 key:value쌍으로 전달한다)
```json
{
	"club_id": 224,
	"club_name": "nhn 보드게임 동호회",
    "club_description": "네이버/라인/nhn엔터 보드게임 동호회",
  	"start_date": "20150101 or null",
 	"end_date": "20150401 or null",
	"max_member_cnt": 3 or null,
}
```
- Response: 204
- Fail: 403(Forbidden)

클럽 정보 수정 권한이 있는지 조회한다.
- Request: GET **/clubs/{club_id}/leader**
- Response: 200
```json
{
  "result": true
}
```

클럽에 가입한다.	`Done`
- Request: POST **/clubs/{club_id}/members**
- Response: 201
- Fail: 409 with errmsg

클럽에 소속된 멤버리스트를 조회한다.	`Done`
- Request: GET **/clubs/{club_id}/members?start=1&display=10**
- Response: 200
```json
{
	"member_cnt": 1,
	"members":	[
    	{
   			"user_id": 224,
			"name": "강소라",
    		"nickname": "안영이",
			"email": "sora@navercorp.com",
    		"corp_id": 11,
			"corp_name": "네이버",
            "role_type": "member or leader or founder"
        }
    ],
}
```

클럽에서 탈퇴한다.
(단, 리더이고 클럽에 리더가 1명만 존재하는 경우 탈퇴 불가)	`Done`
- Request: DELETE **/clubs/{club_id}/members**
- Response: 200

포스트를 생성한다.	`Done`
- Request: POST **/clubs/{club_id}/posts**
```json
{
	"title": "야유회 가요",
    "body": "같이 갑시다",
	"post_type": "normal or top",
    "open_type": "club or club_intra",
}
```
- Response: 201
```json
{
	"post_id": 8888
}
```


포스트를 수정한다.
- Request: PUT **/clubs/{club_id}/posts/{post_id}** (수정이 필요한 항목만 key:value쌍으로 전달한다)
```json
{
	"title": "야유회 가요2",
    "body": "같이 갑시다2",
	"post_type": "normal or top",
    "open_type": "club or club_intra",
}
```
- Response: 204

포스트를 삭제한다.
- Request: DELETE **/clubs/{club_id}/posts/{post_id}**
- Response: 200


지정된 클럽의 포스트 목록을 읽어온다.	`Done`
- Request: GET **/clubs/{club_id}/posts?start=1&display=10&comment_display=1**
- Response: 200
```json
{
	"post_cnt": 1,
    "posts": [
    	{
			"post_id": 888,
   			"poster_id": 224,
			"poster_name": "강소라",
            "poster_nickname": "안영이",
          	"poster_corp_id": 1,
          	"poster_corp_name": "네이버",
        	"title": "야유회 가요",
       		"body": "같이 갑시다",
      		"post_type": "normal or top",
     		"open_type": "club or club_intra",
    		"view_cnt": 10,
			"like_cnt": 3,
			"create_time": "20150303112233",
            "comment_cnt": 3,
			"comments": [
				{
    				"comment_id": 777,
					"commenter_id": 225,
            		"commenter_name": "임시완",
   					"commenter_nickname": "장그래",
					"commenter_corp_id": 1,
            		"commenter_corp_name": "네이버",
  					"body": "좋아요",
 					"like_cnt": 3,
					"create_time": "20150303223344"
				}
            ]
        }
    ]
}
```

지정된 포스트와 커멘트를 읽어온다.	`Done`
- Request: GET **/clubs/{club_id}/posts/{post_id}**
- Response: 200
```json
{
	"post_id": 888,
	"poster_id": 224,
    "poster_name": "강소라",
    "poster_nickname": "안영이",
  	"poster_corp_id": 1,
	"poster_corp_name": "네이버",
  	"title": "야유회 가요",
	"body": "같이 갑시다",
	"post_type": "normal or top",
    "open_type": "club or club_intra",
	"view_cnt": 10,
    "like_cnt": 3,
	"comment_cnt": 1,
    "create_time": "20150303112233",
  	"comments": [
		{
    		"comment_id": 777,
			"commenter_id": 225,
            "commenter_name": "임시완",
   			"commenter_nickname": "장그래",
			"commenter_corp_id": 1,
            "commenter_corp_name": "네이버",
  			"body": "좋아요",
 			"like_cnt": 3,
			"create_time": "20150303223344"
		}
    ]
}
```

포스트의 커멘트를 작성한다.	`Done`
- Request: POST **/clubs/{club_id}/posts/{post_id}/comments**
```json
{
	"body": "저도 좋아요, 일요일에 보기로 해요"
}
```
- Response: 201
```json
{
	"comment_id": 8887
}
```

포스트의 커멘트를 삭제한다.
- Request: DELETE **/clubs/{club_id}/posts/{post_id}/comments/{comment_id}**
- Response: 200

포스트를 좋아하는 사람 목록을 반환한다.
- Request: GET **/clubs/{club_id}/posts/{post_id}/likers?start=1&display=10**
- Response: 200
```json
{
	"liker_cnt": 1,
	"likers": [
    	{
        	"liker_id": 224,
       		"liker_name": "강소라",
       		"liker_nickname": "안영이",
        }
    ]
}
```


포스트의 커멘트를 좋아하는 사람 목록을 반환한다.
- Request: GET **/clubs/{club_id}/posts/{post_id}/comments/{comment_id}/likers?start=1&display=10**
- Response: 200
```json
{
	"liker_cnt": 1,
	"likers": [
    	{
        	"liker_id": 224,
       		"liker_name": "강소라",
       		"liker_nickname": "안영이",
        }
    ]
}
```

# [Mybatis + Springboot + MySQL]

# 1. 라이브러리 추가

```dbn-psql
implementation 'org.mybatis.spring.boot:mybatis-spring-boot-starter:3.0.3'
```

---

# 2. project 셋팅 (application.yml)
* 0뎁스로 추가해야됨(들여쓰기 하나도 없이 제일 왼쪽으로 붙여서 추가)
```dbn-psql
mybatis:
  mapper-locations: classpath:/mapper/**/*.xml #쿼리위치
  type-aliases-package: com.example.hotel_back #xml에서의 파라미터, resultType 찾는 패키지 
  configuration: #카멜케이스
    map-underscore-to-camel-case: true
```

# 2-1. 매퍼 생성 디렉토리 만들기(xml파일)

예시

```
resources/mapper/HotelMapper.xml
```

---

# 3. mapper 인터페이스를 스프링이 찾을 수 있도록 설정(1번으로 설정.왜냐 매번 어노테이션 선언할 필요가 없음)

```dbn-psql
@MapperScan("com.example.mapper")
@SpringBootApplication
public class Application {}
```

혹은

```dbn-psql
@Mapper
public interface UserMapper {
    User findById(Long id);
}
```

---

# 4. 예시

### 1. 컨트롤러생성

```dbn-psql
@RestController
@RequestMapping("/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/{id}")
    public User getUser(@PathVariable Long id) {
        return userService.getUser(id);
    }
}
```

### 2. 서비스 생성

```dbn-psql
@Service
public class UserService {

    private final UserMapper userMapper;

    public UserService(UserMapper userMapper) {
        this.userMapper = userMapper;
    }

    public User getUser(Long id) {
        return userMapper.findById(id);
    }
}
```

### 3. 매퍼생성

```dbn-psql
public interface UserMapper {

    User findById(Long id);
}
```

### 4. 쿼리생성

```dbn-psql
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">

<mapper namespace="com.example.hotel_back.ownhotel.mapper.OwnHotelMapper">

    <!--소유숙소 객실개수-->
    <select id="getAvailableNumber"
            parameterType="long"
            resultType="int">
        select count_room
        from own_hotel
        where own_hotel_id = #{value}
    </select>


</mapper>
```
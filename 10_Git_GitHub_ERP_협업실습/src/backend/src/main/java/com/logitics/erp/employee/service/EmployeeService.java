package com.logitics.erp.employee.service;

import com.logitics.erp.common.util.JwtProvider;
import com.logitics.erp.department.entity.Department;
import com.logitics.erp.department.repository.DepartmentRepository;
import com.logitics.erp.employee.dto.*;
import com.logitics.erp.employee.entity.Employee;
import com.logitics.erp.employee.mapper.EmployeeMapper;
import com.logitics.erp.employee.repository.EmployeeRepository;
import com.logitics.erp.position.entity.Position;
import com.logitics.erp.position.repository.PositionRepository;
import io.micrometer.common.util.StringUtils;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class EmployeeService {

	private final EmployeeRepository employeeRepository;
	private final DepartmentRepository departmentRepository;
    private final PositionRepository positionRepository;
	private final EmployeeMapper employeeMapper;
	private final JwtProvider jwtProvider;
	private final PasswordEncoder passwordEncoder;

	public void createEmployeeTest() {
		Department d = departmentRepository.findById(1L).orElseThrow();

		Employee e = Employee.builder()
						.employeeNo("L001")
						.name("tomhoon")
						.birthDate(LocalDate.of(1995, 7, 7))
						.email("gnsdl@naver.com")
						.department(d)
						.build();

		employeeRepository.save(e);
	}

	@Transactional
	public CreateEmployeeResponse createEmployee(CreateEmployeeRequest request) {
		Department department = departmentRepository.findByDepartmentName(request.getDepartmentName()).orElseThrow();

		String employeeNumber = "L" + String.format("%04d", employeeRepository.count() + 1);

		Employee e = Employee.builder()
						.employeeNo(employeeNumber)
						.name(request.getName())
						.birthDate(request.getBirthDate())
						.email(request.getEmail())
						.phone(request.getPhone())
						.address(request.getAddress())
						.employeeStatusCode(request.getEmployeeStatusCode())
						.department(department)
						.build();

		Employee createdEntity = employeeRepository.save(e);
		return new CreateEmployeeResponse(createdEntity);
	}


	public List<EmployeeListResponse> getEmployees(SearchEmployeeRequest request) {

		int offset = (request.getPage() - 1) * 10;
		List<EmployeeListResponse> list = employeeMapper.getEmployees(request.getSize(), offset, request);

		return list;
	}

	public List<Employee> getTest() {
		return employeeMapper.getTest();
	}

	public LoginResponse login(LoginRequest loginRequest) throws Exception {
		Employee loginEmployee = employeeRepository.findByEmail(loginRequest.getEmail()).orElseThrow();
		String encryptedPassword = loginEmployee.getPassword();
		Boolean isSamePassword = passwordEncoder.matches(loginRequest.getPassword(), encryptedPassword);

		if (isSamePassword) {
			String accessToken = jwtProvider.createToken(loginRequest.getEmail());
			long expireIn = 1000 * 60 * 30;
			String name = loginEmployee.getName();
			String email = loginEmployee.getEmail();
			String employeeNo = loginEmployee.getEmployeeNo();
			String departmentName = loginEmployee.getDepartment().getDepartmentName();
			String positionName = loginEmployee.getPosition().getPositionName();

			return LoginResponse.builder()
							.accessToken(accessToken)
							.name(name)
							.expireIn(expireIn)
							.email(email)
							.employeeNo(employeeNo)
							.position(positionName)
							.departmentName(departmentName)
							.build();
		}

		throw new Exception("올바른 회원 정보가 아닙니다.");
	}

    public Boolean registerEmployee(RegisterEmployeeRequest registerEmployeeRequest) {
        // 1. 존재하는 부서인지 확인
        String recievedDepartmentName = registerEmployeeRequest.getDepartmentName();
        Department department = departmentRepository
                .findByDepartmentName(recievedDepartmentName)
                .orElseThrow(() -> new IllegalArgumentException("존재하지 않는 부서입니다."));

        // 2. 존재하는 직급인지 확인
        String receivedPositionName = registerEmployeeRequest.getPositionName();
        Position position = positionRepository
                .findByPositionName(receivedPositionName)
                .orElseThrow(() -> new IllegalArgumentException("존재하지 않는 직위입니다."));

        // 3. 이메일 중복 체크
        Optional<Employee> duplicateEmployee = employeeRepository.findByEmail(registerEmployeeRequest.getEmail());
        if (duplicateEmployee.isPresent()) {
            throw new IllegalArgumentException("이메일이 중복됩니다. 다른 이메일을 사용해주세요.");
        }

        // 4. 나머지 처리
        Long lastEmployeeNo = employeeRepository.findAll().getLast().getEmployeeId();
        Employee newEmployee = Employee
                .builder()
                .employeeNo("T" + String.format("%04d", lastEmployeeNo + 1))
                .name(registerEmployeeRequest.getName())
                .hireDate(LocalDate.parse(registerEmployeeRequest.getHireDate()))
                .email(registerEmployeeRequest.getEmail())
                .phone(registerEmployeeRequest.getPhone())
                .postCode(registerEmployeeRequest.getPostCode())
                .detailedAddress(registerEmployeeRequest.getDetailedAddress())
                .address(registerEmployeeRequest.getAddress())
                .employeeStatusCode(registerEmployeeRequest.getEmploymentStatus())
                .department(department)
                .position(position)
                .build();

        Employee registeredEmployee = employeeRepository.save(newEmployee);

        return registeredEmployee.getEmployeeId() > 0;
    }

    public Boolean joinErp(JoinErpRequest joinErpRequest) {
        String receivedEmployeeNo = joinErpRequest.getEmployeeNo();
        String receivedPositionName = joinErpRequest.getPositionName();

        Employee e = employeeRepository
                .findByEmployeeNo(receivedEmployeeNo)
                .orElseThrow(() -> new IllegalArgumentException("존재하지 않는 사원번호입니다."));

        Position p = positionRepository
                .findByPositionName(receivedPositionName)
                .orElseThrow(() -> new IllegalArgumentException("존재하지 않는 직급입니다."));


        String originPositionName = e.getPosition().getPositionName();
        if (!originPositionName.equals(receivedPositionName)) {
            throw new IllegalArgumentException("등록된 부서와 일치하지 않습니다.");
        }

        String pw = joinErpRequest.getPassword();
        String chkPw = joinErpRequest.getCheckPassword();
        if (!pw.equals(chkPw)) {
            throw new IllegalArgumentException("비밀번호가 일치하지 않습니다.");
        }

        if (StringUtils.isNotBlank(e.getPassword())) {
            throw new IllegalArgumentException("이미 회원가입된 유저입니다. 고객센터에 문의하세요.");
        }

        e.setEmail(joinErpRequest.getEmail());

        String encryptedPassword = passwordEncoder.encode(joinErpRequest.getPassword());

        e.setPassword(encryptedPassword);

        Employee joinedEmployee = employeeRepository.save(e);
        return joinedEmployee.getEmployeeId() > 0;
    }


    // 존재하던 사원 정보 수정
    public Boolean modifyEmployee(RegisterEmployeeRequest modifyEmployeeRequest) {
        // 1. 존재하는 부서인지 확인
        String receivedDepartmentName = modifyEmployeeRequest.getDepartmentName();
        Department department = departmentRepository
                .findByDepartmentName(receivedDepartmentName)
                .orElseThrow(() -> new IllegalArgumentException("존재하지 않는 부서입니다."));

        // 2. 존재하는 직급인지 확인
        String receivedPositionName = modifyEmployeeRequest.getPositionName();
        Position position = positionRepository
                .findByPositionName(receivedPositionName)
                .orElseThrow(() -> new IllegalArgumentException("존재하지 않는 직위입니다."));


        // 4. 나머지 처리
        Employee modifyEmployee = employeeRepository
                .findByEmployeeNo(modifyEmployeeRequest.getEmployeeNo())
                .orElseThrow(() -> new IllegalArgumentException("존재하지 않는 사원번호입니다."));

        // 5. 수정할 부서/직급 찾기
        String changePositionName = modifyEmployeeRequest.getPositionName();
        String changeDepartmentName = modifyEmployeeRequest.getDepartmentName();

        Position changePosition = positionRepository
                .findByPositionName(changePositionName)
                .orElseThrow(() -> new IllegalArgumentException("수정할 직급이 존재하지 않습니다."));

        Department changeDepartment = departmentRepository
                .findByDepartmentName(changeDepartmentName)
                .orElseThrow(() -> new IllegalArgumentException("수정할 부서가 존재하지 않습니다."));

        modifyEmployee.setName(modifyEmployeeRequest.getName());
        modifyEmployee.setHireDate(LocalDate.parse(modifyEmployeeRequest.getHireDate()));
        modifyEmployee.setEmail(modifyEmployeeRequest.getEmail());
        modifyEmployee.setPhone(modifyEmployeeRequest.getPhone());
        modifyEmployee.setAddress(modifyEmployeeRequest.getAddress());
        modifyEmployee.setPostCode(modifyEmployeeRequest.getPostCode());
        modifyEmployee.setDetailedAddress(modifyEmployeeRequest.getDetailedAddress());
        modifyEmployee.setEmployeeStatusCode(modifyEmployeeRequest.getEmploymentStatus());
        modifyEmployee.setPosition(changePosition);
        modifyEmployee.setDepartment(changeDepartment);

        Employee changedEmployeeEntity = employeeRepository.save(modifyEmployee);

        return changedEmployeeEntity.getEmployeeId() > 0;
    }
}

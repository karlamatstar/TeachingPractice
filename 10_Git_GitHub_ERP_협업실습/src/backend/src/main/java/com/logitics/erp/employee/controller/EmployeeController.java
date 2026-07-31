package com.logitics.erp.employee.controller;

import com.logitics.erp.employee.dto.*;
import com.logitics.erp.employee.entity.Employee;
import com.logitics.erp.employee.service.EmployeeService;
import io.micrometer.common.util.StringUtils;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1/employees")
public class EmployeeController {

	private final EmployeeService employeeService;

	@PostMapping("/login")
	public LoginResponse login(@RequestBody LoginRequest loginRequest) throws Exception{
		return employeeService.login(loginRequest);
	}

	@GetMapping("/createTest")
	public void createTest() {
		employeeService.createEmployeeTest();
	}

	@GetMapping("/getTest")
	public List<Employee> getTest() {
		return employeeService.getTest();
	}

    @PostMapping("/joinErp")
    @Tag(name = "Employee", description = "사원 ERP 가입 API")
    @Operation(summary = "ERP 사이트 가입", description = "입사한 사원만 사이트 가입 가능")
    public Boolean joinErp(@RequestBody JoinErpRequest joinErpRequest) {
        return employeeService.joinErp(joinErpRequest);
    }

    @PostMapping("/registerEmployee")
    @Tag(name = "Employee", description = "사원 등록 API")
    @Operation(summary = "입사한 사원 등록(회원가입 아님)", description = "입사한 사원을 등록합니다. (회원가입은 따로 진행) 사원번호를 함께 넣는 경우 수정으로 판단합니다.")
    public Boolean registerEmployee(@RequestBody RegisterEmployeeRequest registerEmployeeRequest) {
        String employeeNo = registerEmployeeRequest.getEmployeeNo();
        if (StringUtils.isNotBlank(employeeNo)) {
            return employeeService.modifyEmployee(registerEmployeeRequest);
        }
        return employeeService.registerEmployee(registerEmployeeRequest);
    }

	@GetMapping
	@Tag(name = "Employee", description = "사원 관리 API")
	@Operation(summary = "사원 조회", description = "사원 목록을 조회합니다.")
	public List<EmployeeListResponse> getEmployees(
					@Parameter(
									description = "사번/사원명으로조회",
									example = "이채리1"
					)
					SearchEmployeeRequest request,
                    Authentication authentication
	) {
        String name = authentication.getName();
		return employeeService.getEmployees(request);
	}

	@PostMapping
	public CreateEmployeeResponse createEmployee(
					@RequestBody @Valid CreateEmployeeRequest request
	) {
		return employeeService.createEmployee(request);
	}

}

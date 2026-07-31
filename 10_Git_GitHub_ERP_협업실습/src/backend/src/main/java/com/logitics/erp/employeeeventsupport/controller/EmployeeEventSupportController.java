package com.logitics.erp.employeeeventsupport.controller;

import com.logitics.erp.employee.entity.Employee;
import com.logitics.erp.employee.repository.EmployeeRepository;
import com.logitics.erp.employee.service.EmployeeService;
import com.logitics.erp.employeeappointment.service.EmployeeAppointmentService;
import com.logitics.erp.employeeeventsupport.dto.EmployeeEventSupportRegisterRequest;
import com.logitics.erp.employeeeventsupport.dto.EmployeeEventSupportResponse;
import com.logitics.erp.employeeeventsupport.service.EmployeeEventSupportService;
import io.swagger.v3.oas.annotations.Operation;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1/support")
public class EmployeeEventSupportController {

	private final EmployeeEventSupportService employeeEventSupportService;
	private final EmployeeRepository employeeRepository;

    @GetMapping("/detail/{eventSupportId}")
    @Operation(summary = "경조비 상세조회", description = "상세 버튼 클릭시 모달 상세내용")
    public EmployeeEventSupportResponse getEventSupportDetail(@PathVariable Long eventSupportId) {
        return employeeEventSupportService.getEventSupportDetail(eventSupportId);
    }

	@GetMapping
	@Operation(summary = "경조비 신청 조회")
	public List<EmployeeEventSupportResponse> getEventSupportList(
					@RequestParam(defaultValue = "1") int page,
					@RequestParam(defaultValue = "10") int size,
					@RequestParam(required = false) String keyword,
					Authentication authentication
	) {
		String email = authentication.getName();
		Employee employee = employeeRepository.findByEmail(email).orElseThrow();
		Long employeeId = employee.getEmployeeId();
		return employeeEventSupportService.getSupportList(page, size, keyword, employeeId);
	}

	@PostMapping
	@Operation(summary = "경조비 신청", description = "경조비 신청합니다.")
	public boolean registerEventSupport(
			@RequestBody EmployeeEventSupportRegisterRequest registerRequest,
			Authentication authentication
	) {

		String email = authentication.getName();
		Employee employee = employeeRepository.findByEmail(email).orElseThrow();
		Long employeeId = employee.getEmployeeId();

		registerRequest.setEmployeeId(employeeId);

		return employeeEventSupportService.registerEventSupport(registerRequest);
	}

	@DeleteMapping("/{eventSupportId}")
	@Operation(summary = "경조비 삭제", description = "경조비 신청 내역 삭제합니다.")
	public boolean deleteEventSupport(@PathVariable Long eventSupportId) {
		return employeeEventSupportService.deleteEventSupport(eventSupportId);
	}

}
